import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette_prometheus import PrometheusMiddleware, metrics

from core.settings import settings
from pedometer import api

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _life_span(application: FastAPI) -> AsyncIterator[None]:  # pragma: no cover  # noqa: ARG001
    """Контекстный менеджер для жизненного цикла приложения.

    Args:
        application: FastAPI приложение.

    """
    logger.info("Инициализация приложения ...")

    try:
        yield
    finally:
        logger.info("Завершение работы приложения")


app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.project_version,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
    default_response_class=ORJSONResponse,
    lifespan=_life_span,
)

app.add_middleware(PrometheusMiddleware)

app.include_router(api.router)
app.add_route(settings.metrics_endpoint, metrics)

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(
        settings.start_command,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
