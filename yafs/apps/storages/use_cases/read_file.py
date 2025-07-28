import uuid
from dataclasses import dataclass
from typing import AsyncIterator, Self

from ..services import FileService


@dataclass
class ReadFileUseCase:
    """
    Потоковое чтение файла из S3.
    """

    file_service: FileService

    async def __call__(self: Self, file_id: uuid.UUID) -> AsyncIterator[bytes]:
        file = await self.file_service.get(file_id)
        return self.file_service.stream_reader(file)
