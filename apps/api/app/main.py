from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.api.routes import router
from app.core.config import settings

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.api_rate_limit])
app = FastAPI(title="Tourism Intelligence API", version="0.2.0")
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def _rate_limit_handler(_request: Request, _exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})


app.add_middleware(SlowAPIMiddleware)
app.include_router(router, prefix="/api")
