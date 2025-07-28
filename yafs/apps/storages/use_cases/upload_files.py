import uuid
from dataclasses import dataclass
from typing import Self, cast

from fast_clean.repositories.storage.reader import StreamReadAsyncProtocol
from fastapi import UploadFile

from ..schemas import FileReadSchema, FileUploadSchema
from ..services import FileService


@dataclass
class UploadFilesUseCase:
    file_service: FileService

    async def __call__(
        self: Self, storage_id: uuid.UUID, files: list[UploadFile]
    ) -> list[FileReadSchema]:
        files_schema = [
            FileUploadSchema(
                name=file.filename,
                size=file.size,
                content_type=file.content_type,
                reader=cast(StreamReadAsyncProtocol, file),
            )
            for file in files
            if file.filename and file.size
        ]
        return await self.file_service.upload_files(storage_id, files_schema)
