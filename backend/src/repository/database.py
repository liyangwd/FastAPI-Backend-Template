import pydantic
from sqlalchemy.ext.asyncio import AsyncEngine as SQLAlchemyAsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as create_sqlalchemy_async_engine
from sqlalchemy.pool import NullPool
from src.config.manager import settings


class AsyncDatabase:
    def __init__(self):
        self.postgres_uri: pydantic.PostgresDsn = pydantic.PostgresDsn(
            url=f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:"
            f"{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:"
            f"{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}",
        )
        self.async_engine: SQLAlchemyAsyncEngine = create_sqlalchemy_async_engine(
            url=self.set_async_db_uri,
            echo=settings.IS_DB_ECHO_LOG,
            poolclass=NullPool,
        )
        self.async_session: SQLAlchemyAsyncSession = SQLAlchemyAsyncSession(
            bind=self.async_engine
        )

    @property
    def set_async_db_uri(self) -> str:
        """
        Convert the synchronous database URI to its asynchronous version using AsyncPG:

        `postgresql://` => `postgresql+asyncpg://`
        """
        if self.postgres_uri:
            # Convert the PostgresDsn object to a string and replace the scheme
            uri_str = str(self.postgres_uri)
            return uri_str.replace("postgresql://", "postgresql+asyncpg://")
        return ""


async_db: AsyncDatabase = AsyncDatabase()
