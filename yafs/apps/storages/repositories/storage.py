from typing import Self

from fast_clean.repositories import DbCrudRepository

from ..models import Storage
from ..schemas import StorageCreateSchema, StorageReadSchema, StorageUpdateSchema


class StorageDbRepository(DbCrudRepository[Storage, StorageReadSchema, StorageCreateSchema, StorageUpdateSchema]):
    """
    Репозиторий для работы с хранилищами.
    """

    async def get_by_active(self: Self, *, is_active: bool | None = None) -> list[StorageReadSchema]:
        """
        Выбираем список доступных хранилищ.
        """

        async with self.session_manager.get_session() as s:
            statement = self.select()
            if is_active is not None:
                statement.where(self.model_type.is_active == is_active)
            models = (await s.execute(statement)).scalars()
            return [self.model_validate(model) for model in models]
