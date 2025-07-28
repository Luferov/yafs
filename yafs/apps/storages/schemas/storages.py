import uuid

from fast_clean.schemas import CreateSchema, ReadSchema, RequestSchema, ResponseSchema, UpdateSchema
from pydantic import ConfigDict

from ..enums import FileStorageTypeEnum


class StorageReadSchema(ReadSchema):
    """
    Схема для чтения хранилища.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: FileStorageTypeEnum
    params: str
    is_active: bool


class StorageCreateSchema(CreateSchema):
    """
    Схема для создания хранилища.
    """

    model_config = ConfigDict(from_attributes=True)

    type: FileStorageTypeEnum
    params: str
    is_active: bool = True


class StorageUpdateSchema(UpdateSchema):
    """
    Схема для обновления хранилища.
    """

    model_config = ConfigDict(from_attributes=True)

    type: FileStorageTypeEnum | None = None
    params: str | None = None
    is_active: bool | None = None


class StorageCreateRequestSchema(RequestSchema):
    """
    Схема для создания внешнего хранилища.
    """

    type: FileStorageTypeEnum
    """
    Тип хранилища.
    """
    params: dict[str, str | int]
    """
    Параметры строки подключения.
    """


class StorageResponseSchema(ResponseSchema):
    id: uuid.UUID
