import contextlib
from typing import Any, Awaitable, Callable, Self

from apscheduler.job import Job as ApsJob
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fast_clean.settings import CoreDbSettingsSchema
from sqlalchemy import create_engine

from ..enums import TriggerTypeEnum


class SchedulerRepository:
    def __init__(self, settings: CoreDbSettingsSchema) -> None:
        dsn = (
            f'postgresql+psycopg://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.name}'
        )
        engine = create_engine(dsn)
        self.scheduler = AsyncIOScheduler(jobstores={'default': SQLAlchemyJobStore(engine=engine)})

    def start(self: Self) -> None:
        """
        Запускаем планировщик.
        """
        self.scheduler.start()

    def shutdown(self: Self, wait: bool = True) -> None:
        """
        Останавливаем планировщик, ожидая завершения всех задач.
        """
        self.scheduler.shutdown(wait)

    def add_job(
        self: Self,
        job_id: str,
        func: Callable[..., Awaitable[None]],
        trigger: TriggerTypeEnum,
        replace_existing: bool,
        args: tuple[Any, ...],
        /,
        **trigger_args,
    ) -> ApsJob:
        return self.scheduler.add_job(
            func, trigger=trigger.lower(), id=job_id, replace_existing=replace_existing, args=args, **trigger_args
        )

    def remove_job(self: Self, job_id: str) -> None:
        with contextlib.suppress(JobLookupError):
            self.scheduler.remove_job(job_id)

    def remove_all_jobs(self: Self) -> None:
        self.scheduler.remove_all_jobs()
