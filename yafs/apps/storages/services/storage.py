from dataclasses import dataclass
from typing import Self

from fast_clean.repositories.storage.schemas import S3StorageParamsSchema
from fast_clean.services.cryptography import CryptographyServiceProtocol

from ..enums import FileStorageTypeEnum
from ..exceptions import StorageTypeNotFoundError
from ..repositories import StorageDbRepository
from ..schemas import StorageCreateRequestSchema, StorageCreateSchema, StorageReadSchema


@dataclass
class StorageService:
    storage_repository: StorageDbRepository
    crypto_service: CryptographyServiceProtocol

    async def add_storage(self: Self, storage_create_schema: StorageCreateRequestSchema) -> StorageReadSchema:
        match storage_create_schema.type:
            case FileStorageTypeEnum.S3:
                validate_params = S3StorageParamsSchema.model_validate(storage_create_schema.params)
            case _:
                raise StorageTypeNotFoundError()
        params = validate_params.model_dump_json()
        e_params = self.crypto_service.encrypt(params)
        return await self.storage_repository.create(
            StorageCreateSchema(type=storage_create_schema.type, params=e_params)
        )
