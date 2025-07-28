import uuid
from dataclasses import dataclass

from ..schemas import FileReadSchema
from ..services import FileService


@dataclass
class FileInfoUseCase:
    file_service: FileService

    async def __call__(self, file_id: uuid.UUID) -> FileReadSchema:
        return await self.file_service.get(file_id)
