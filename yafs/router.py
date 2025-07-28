"""
Основной модуль для роутов приложения.
"""

from fast_clean.contrib.healthcheck.router import router as healthcheck_router
from fast_clean.contrib.monitoring.router import router as monitoring_router
from fastapi import FastAPI

from yafs.apps.storages.router import router as storage_router


def apply_routes(app: FastAPI) -> None:
    """
    Применяем роуты приложения.
    """

    app.include_router(healthcheck_router, include_in_schema=True)
    app.include_router(storage_router)
    app.include_router(monitoring_router)
