from collections.abc import Callable, Iterable, AsyncIterator
from contextlib import asynccontextmanager

from fast_clean.container import ContainerManager
from fast_clean.exceptions import use_exceptions_handlers
from fast_clean.middleware import use_middleware
from fast_clean.utils.toml import use_toml_info
from fast_clean.loggers import use_logging
from fast_clean.contrib.logging.sentry import use_sentry
from fastapi import FastAPI

from yafs.apps.storages.exceptions import use_exceptions_handlers as use_storage_exception_handlers

from .settings import SettingsSchema


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Предварительная инициализация приложения.

    - устанавливаем настройки логгирования
    - устанавливаем настройки кеширования
    - устанавливаем настройки стриминга
    """

    yield

    await ContainerManager.close()


def create_app(use_routes: Iterable[Callable[[FastAPI], None]]) -> FastAPI:
    settings = SettingsSchema()  # type: ignore
    project_info = use_toml_info(settings.base_dir)
    app = FastAPI(
        title=project_info.name,
        debug=settings.debug,
        description=project_info.description or '',
        lifespan=lifespan,
        docs_url='/docs',
        openapi_url='/docs.json',
        version=project_info.version,
    )

    ContainerManager.init_for_fastapi(app)

    use_logging(settings.base_dir)
    use_sentry(settings.sentry_dsn)

    use_middleware(app, project_info.name, settings.cors_origins)
    use_exceptions_handlers(app, settings)
    use_storage_exception_handlers(app, settings)

    for use_route in use_routes:
        use_route(app)

    return app
