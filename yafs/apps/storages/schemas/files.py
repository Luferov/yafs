import uuid
from dataclasses import dataclass

from fast_clean.repositories.storage.reader import StreamReadAsyncProtocol
from fast_clean.schemas import CreateSchema, ReadSchema, UpdateSchema
from pydantic import ConfigDict


class FileReadSchema(ReadSchema):
    model_config = ConfigDict(from_attributes=True)

    name: str
    size: int
    content_type: str | None = None
    storage_id: uuid.UUID


class FileCreateSchema(CreateSchema):
    model_config = ConfigDict(from_attributes=True)

    name: str
    size: int
    content_type: str | None = None
    storage_id: uuid.UUID


class FileUpdateSchema(UpdateSchema):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    size: int | None = None
    content_type: str | None = None
    storage_id: uuid.UUID | None = None


@dataclass
class FileUploadSchema:
    name: str
    size: int

    reader: StreamReadAsyncProtocol

    content_type: str | None = None
