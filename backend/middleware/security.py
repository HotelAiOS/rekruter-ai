import logging

logger = logging.getLogger(__name__)

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from config import settings
import time

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"]
)

async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", f"req-{int(time.time()*1000)}")
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}

async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response
