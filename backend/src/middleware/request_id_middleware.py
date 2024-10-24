# app/middleware/request_id_middleware.py
import contextvars
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# 创建一个上下文变量用于存储 request_id
request_id_context = contextvars.ContextVar("request_id", default="N/A")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_id_context.set(request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
