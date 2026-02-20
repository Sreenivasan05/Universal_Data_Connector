from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import chat
from app.routers import health, data
from app.utils.logging import configure_logging
from app.utils.request_logger import RequestLoggingMiddleware
from app.config import settings
import uvicorn
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):

    configure_logging(
        log_level=settings.LOG_LEVEL, 
        use_json=settings.LOG_JSON, 
    )
    logger = logging.getLogger("app.startup")
    logger.info(
        "Application starting",
        extra={
            "environment": settings.ENVIRONMENT,
            "log_level": settings.LOG_LEVEL,
            "max_results": settings.MAX_RESULTS,
        },
    )
    yield
    logger.info("Application shutting down")

app = FastAPI(title=settings.APP_NAME,lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(health.router)
app.include_router(data.router)
app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)