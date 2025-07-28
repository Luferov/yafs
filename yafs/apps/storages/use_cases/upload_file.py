import uuid
from dataclasses import dataclass
from typing import Self

from fastapi import UploadFile

from ..exceptions import BadUploadFileError
from ..schemas import FileReadSchema
from ..services import FileService


@dataclass
class UploadFileUseCase:
    file_service: FileService

    async def __call__(self: Self, storage_id: uuid.UUID, file: UploadFile) -> FileReadSchema:
        if not (file.filename and file.size):
            raise BadUploadFileError()
        return await self.file_service.upload_file(storage_id, file.filename, file.size, file.content_type, file)
