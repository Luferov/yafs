import asyncio
import io
import uuid
from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path
from typing import Self, cast

from fast_clean.repositories.storage import AsyncStreamReaderProtocol
from fast_clean.repositories.storage.reader import StreamReadAsyncProtocol
from fast_clean.services.transaction import TransactionService

from ..repositories import FileDbRepository, FileStorageRepositoryProtocol
from ..schemas import FileCreateSchema, FileReadSchema, FileUploadSchema


@dataclass
class FileService:
    file_repository: FileDbRepository
    file_storage_repository: FileStorageRepositoryProtocol
    transaction_service: TransactionService

    async def upload_file(
        self: Self,
        storage_id: uuid.UUID,
        name: str,
        size: int,
        content_type: str | None,
        reader: AsyncStreamReaderProtocol,
    ) -> FileReadSchema:
        """
        Загружаем файл на провайдер и возвращаем идентификатор создаваемой записи.

        - не проверяем storage_id, потому что если дошли сюда, значит FileStorageRepository инициализирован.
        """
        async with self.transaction_service.begin():
            file = await self.file_repository.create(
                FileCreateSchema(
                    name=name,
                    size=size,
                    content_type=content_type,
                    storage_id=storage_id,
                )
            )
            await self.upload_file_storage(
                self.get_path(file.id),
                cast(StreamReadAsyncProtocol, reader),
                semaphore=asyncio.BoundedSemaphore(1),
            )
            return file

    async def upload_files(
        self: Self,
        storage_id: uuid.UUID,
        files: list[FileUploadSchema],
    ) -> list[FileReadSchema]:
        async with self.transaction_service.begin():
            created_files = await self.file_repository.bulk_create(
                [
                    FileCreateSchema(
                        name=file.name,
                        size=file.size,
                        content_type=file.content_type,
                        storage_id=storage_id,
                    )
                    for file in files
                ]
            )

            semaphore = asyncio.BoundedSemaphore(4)
            await asyncio.gather(
                *[
                    self.upload_file_storage(
                        self.get_path(created_file.id),
                        file.reader,
                        semaphore=semaphore,
                    )
                    for file, created_file in zip(files, created_files, strict=True)
                ]
            )
            return created_files

    async def get(self: Self, file_id: uuid.UUID) -> FileReadSchema:
        file = await self.file_repository.get_or_none(file_id)
        if file is None:
            raise FileNotFoundError(file_id)
        return file

    async def stream_reader(self: Self, file_schema: FileReadSchema) -> AsyncIterator[bytes]:
        """
        Возвраащем для него поток на чтение.
        """
        async for chunk in self.file_storage_repository.straming_read(
            self.get_path(file_schema.id)
        ):
            yield chunk

    async def delete(self: Self, files_id: list[uuid.UUID]) -> bool:
        """
        Удаление файла, который привязан к customer_code.
        """
        files = await self.file_repository.get_by_ids(files_id)

        async with self.transaction_service.begin():
            await self.file_repository.delete([file.id for file in files])
            semaphore = asyncio.BoundedSemaphore(4)
            await asyncio.gather(
                *[
                    self.file_storage_delete(self.get_path(file.id), semaphore=semaphore)
                    for file in files
                ]
            )
            return True

    async def file_storage_delete(self: Self, path: str, *, semaphore: asyncio.BoundedSemaphore) -> None:
        async with semaphore:
            await self.file_storage_repository.delete(path)

    async def upload_file_storage(
        self: Self, path: str | Path, reader: StreamReadAsyncProtocol, *, semaphore: asyncio.BoundedSemaphore
    ) -> None:
        async with semaphore:
            # Приходится оборачивать в io.BytesIO
            # потому что метод UploadFile из FastAPI
            # не содержит метод tell
            content = io.BytesIO(await reader.read())
            content.seek(0)
            await self.file_storage_repository.stream_write(path, content)  # type: ignore[reportArgumentType]

    @classmethod
    def get_path(cls, file_id: uuid.UUID) -> str:
        """
        Формиурем путь для файла.
        """
        return f'/files/{file_id}'

    @classmethod
    def get_download_path(cls, file: FileReadSchema) -> str:
        """
        Формируем путь для скачивания файла.
        """
        return f'/storage/{file.storage_id}/files/{file.id}/download'
