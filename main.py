from fastapi import FastAPI
from api import auth, demography, schools, forecast, reports, gis_integration
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from core.config import settings

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.RATE_LIMIT_REQUESTS}/{settings.RATE_LIMIT_PERIOD}second"])

app = FastAPI(title="BilimHeat")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(HTTP_429_TOO_MANY_REQUESTS)
async def rate_limit_handler(request: Request, exc):
    return JSONResponse(
        status_code=HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Too Many Requests"},
        headers={"Retry-After": str(exc.detail)},
    )

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(demography.router, prefix="/api/demography", tags=["demography"])
app.include_router(schools.router, prefix="/api/schools", tags=["schools"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["forecast"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(gis_integration.router, prefix="/api/gis", tags=["gis"])
