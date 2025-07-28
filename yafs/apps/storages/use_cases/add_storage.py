from dataclasses import dataclass
from typing import Self

from ..schemas import StorageCreateRequestSchema, StorageResponseSchema
from ..services import StorageService


@dataclass
class AddStorageUseCase:
    storage_service: StorageService

    async def __call__(self: Self, storage_schema: StorageCreateRequestSchema) -> StorageResponseSchema:
        storage = await self.storage_service.add_storage(storage_schema)
        return StorageResponseSchema(id=storage.id)
