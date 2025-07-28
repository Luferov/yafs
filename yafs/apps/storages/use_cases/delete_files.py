import uuid
from dataclasses import dataclass
from typing import Self

from ..services import FileService


@dataclass
class DeleteFilesUseCase:
    """
    Удаляем файл.
    """

    file_service: FileService

    async def __call__(self: Self, file_ids: list[uuid.UUID]) -> bool:
        return await self.file_service.delete(file_ids)
