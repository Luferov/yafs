from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from fastapi import Request

from .exceptions import StoragePathNotFoundError
from .repositories import (
    FileDbRepository,
    FileStorageProviderRepositoryFactory,
    FileStorageRepositoryProtocol,
    StorageDbRepository,
)
from .services import FileService, StorageService
from .use_cases import AddStorageUseCase, DeleteFilesUseCase, ReadFileUseCase, UploadFilesUseCase

__all__ = ('provider',)


class FileProvider(Provider):
    """
    Собираем файловый провайдер.
    """

    scope = Scope.APP

    file_db_repository = provide(FileDbRepository)
    storage_db_repository = provide(StorageDbRepository)
    file_storage_repository_factory = provide(FileStorageProviderRepositoryFactory)

    storage_service = provide(StorageService)
    file_service = provide(FileService, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def provide_file_storage_repository(
        file_storage_repository_factory: FileStorageProviderRepositoryFactory,
        request: Request,
    ) -> AsyncIterator[FileStorageRepositoryProtocol]:
        storage_id = request.path_params.get('storageId', None)
        if storage_id is None:
            raise StoragePathNotFoundError()
        file_storage_repository = await file_storage_repository_factory.make(storage_id)
        async with file_storage_repository:
            yield file_storage_repository

    add_storage_use_case = provide(AddStorageUseCase, scope=Scope.REQUEST)
    read_file_use_case = provide(ReadFileUseCase, scope=Scope.REQUEST)
    delete_files_use_case = provide(DeleteFilesUseCase, scope=Scope.REQUEST)
    upload_files_use_case = provide(UploadFilesUseCase, scope=Scope.REQUEST)


provider = FileProvider()
