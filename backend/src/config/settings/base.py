import logging
import os
import pathlib
import sys

import decouple
import pydantic
from loguru import logger
from pydantic_settings import BaseSettings
from src.config.logging import InterceptHandler
from src.middleware.request_id_middleware import request_id_context

ROOT_DIR: pathlib.Path = pathlib.Path(
    __file__
).parent.parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    TITLE: str = "DAPSQL FARN-Stack Template Application"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    SERVER_HOST: str = decouple.config("BACKEND_SERVER_HOST", cast=str)  # noqa
    SERVER_PORT: int = decouple.config("BACKEND_SERVER_PORT", cast=int)  # noqa
    SERVER_WORKERS: int = decouple.config("BACKEND_SERVER_WORKERS", cast=int)  # noqa
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    DB_POSTGRES_HOST: str = decouple.config("POSTGRES_HOST", cast=str)  # noqa
    DB_MAX_POOL_CON: int = decouple.config("DB_MAX_POOL_CON", cast=int)  # noqa
    DB_POSTGRES_NAME: str = decouple.config("POSTGRES_DB", cast=str)  # noqa
    DB_POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD", cast=str)  # noqa
    DB_POOL_SIZE: int = decouple.config("DB_POOL_SIZE", cast=int)  # noqa
    DB_POOL_OVERFLOW: int = decouple.config("DB_POOL_OVERFLOW", cast=int)  # noqa
    DB_POSTGRES_PORT: int = decouple.config("POSTGRES_PORT", cast=int)  # noqa
    DB_POSTGRES_SCHEMA: str = decouple.config("POSTGRES_SCHEMA", cast=str)  # noqa
    DB_TIMEOUT: int = decouple.config("DB_TIMEOUT", cast=int)  # noqa
    DB_POSTGRES_USERNAME: str = decouple.config("POSTGRES_USERNAME", cast=str)  # noqa

    IS_DB_ECHO_LOG: bool = decouple.config("IS_DB_ECHO_LOG", cast=bool)  # noqa
    IS_DB_FORCE_ROLLBACK: bool = decouple.config(
        "IS_DB_FORCE_ROLLBACK", cast=bool
    )  # noqa
    IS_DB_EXPIRE_ON_COMMIT: bool = decouple.config(
        "IS_DB_EXPIRE_ON_COMMIT", cast=bool
    )  # noqa

    API_TOKEN: str = decouple.config("API_TOKEN", cast=str)  # noqa
    AUTH_TOKEN: str = decouple.config("AUTH_TOKEN", cast=str)  # noqa
    JWT_TOKEN_PREFIX: str = decouple.config("JWT_TOKEN_PREFIX", cast=str)  # noqa
    JWT_SECRET_KEY: str = decouple.config("JWT_SECRET_KEY", cast=str)  # noqa
    JWT_SUBJECT: str = decouple.config("JWT_SUBJECT", cast=str)  # noqa
    JWT_MIN: int = decouple.config("JWT_MIN", cast=int)  # noqa
    JWT_HOUR: int = decouple.config("JWT_HOUR", cast=int)  # noqa
    JWT_DAY: int = decouple.config("JWT_DAY", cast=int)  # noqa
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = JWT_MIN * JWT_HOUR * JWT_DAY

    IS_ALLOWED_CREDENTIALS: bool = decouple.config(
        "IS_ALLOWED_CREDENTIALS", cast=bool
    )  # noqa
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # React default port
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000",  # React docker port
        "http://127.0.0.1:3001",
        "http://localhost:5173",  # Qwik default port
        "http://0.0.0.0:5173",
        "http://127.0.0.1:5173",  # Qwik docker port
        "http://127.0.0.1:5174",
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    HASHING_ALGORITHM_LAYER_1: str = decouple.config(
        "HASHING_ALGORITHM_LAYER_1", cast=str
    )  # noqa
    HASHING_ALGORITHM_LAYER_2: str = decouple.config(
        "HASHING_ALGORITHM_LAYER_2", cast=str
    )  # noqa
    HASHING_SALT: str = decouple.config("HASHING_SALT", cast=str)  # noqa
    JWT_ALGORITHM: str = decouple.config("JWT_ALGORITHM", cast=str)  # noqa

    BACKEND_LOG_PATH: str = decouple.config("BACKEND_LOG_PATH", cast=str)

    class Config(pydantic.BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom
        values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.LOGGERS:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [
                InterceptHandler(level=self.LOGGING_LEVEL)
            ]  # noqa

        log_format = (
            "[<green>{time}</green>: {process.name}/{thread.name}] - <level>"
            "{level: <8}</level> - <blue>{module}:{function}:{line}</blue> - "
            "RequestID: <yellow>{extra[request_id]}</yellow> - "
            "<level>{message}</level>"
        )

        # Ensure the log directory exists
        if not os.path.exists(os.path.dirname(self.BACKEND_LOG_PATH)):
            os.makedirs(os.path.dirname(self.BACKEND_LOG_PATH))

        logger.configure(
            handlers=[
                {
                    "sink": sys.stderr,
                    "level": self.LOGGING_LEVEL,
                    "format": log_format,
                    "filter": self.add_request_id,
                },
                {
                    "sink": self.BACKEND_LOG_PATH,
                    "level": self.LOGGING_LEVEL,
                    "format": log_format,
                    "filter": self.add_request_id,
                    "rotation": "10 MB",  # rotate the log file at 10 MB
                    "compression": "zip",  # compress rotated logs
                    "retention": 5,  # Keep the last 5 log files
                },
            ]
        )

    @staticmethod
    def add_request_id(record):
        # 从上下文变量中获取 request_id
        record["extra"]["request_id"] = request_id_context.get()
        return True
