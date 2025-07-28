import uuid
from dataclasses import dataclass
from typing import Protocol, Self

from fast_clean.repositories.storage import StorageRepositoryFactoryProtocol, StorageRepositoryProtocol
from fast_clean.repositories.storage.enums import StorageTypeEnum
from fast_clean.repositories.storage.schemas import S3StorageParamsSchema
from fast_clean.services.cryptography import CryptographyServiceProtocol

from .storage import StorageDbRepository
from ..enums import FileStorageTypeEnum


class FileStorageRepositoryProtocol(StorageRepositoryProtocol, Protocol):
    """
    Является алиасом для StorageRepositoryProtocol.
    """

    ...


@dataclass
class FileStorageProviderRepositoryFactory:
    """
    Фабирка, которая выполняет инициализацию инстанса репозитория
    """

    storage_repository: StorageDbRepository
    storage_repository_factory: StorageRepositoryFactoryProtocol
    crypto_service: CryptographyServiceProtocol
    """
    Несмотря на то, что это сервис, он находится в репозитоии, потому что сервис
    предоставляет функционал по шифрованию и дешифрованию параметров подключения.
    """

    async def make(self: Self, storage_id: uuid.UUID) -> FileStorageRepositoryProtocol:
        """
        Инициализуем для репозитория ин
        """
        storage = await self.storage_repository.get(storage_id)
        d_params = self.crypto_service.decrypt(storage.params)
        if storage.type == FileStorageTypeEnum.S3:
            return await self.storage_repository_factory.make(
                StorageTypeEnum.S3, S3StorageParamsSchema.model_validate_json(d_params)
            )
        raise NotImplementedError
