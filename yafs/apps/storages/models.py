from __future__ import annotations

import uuid

import sqlalchemy as sa
from fast_clean.db import BaseUUID
from fast_clean.models import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy_utils.types import UUIDType

from .enums import FileStorageTypeEnum


class Storage(BaseUUID, TimestampMixin):
    """
    Подключаемые хранилища файлов.
    """

    __tablename__ = 'storages'

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )
    type: Mapped[FileStorageTypeEnum] = mapped_column(
        sa.Enum(FileStorageTypeEnum, native_enum=False, create_type=False),
        default=FileStorageTypeEnum.S3,
        server_default=FileStorageTypeEnum.S3,
        nullable=False,
    )
    params: Mapped[str] = mapped_column(sa.String(length=2048), nullable=False)
    """
    Зашифрованная строка с параметрами подключения к хранилищу.
    """
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True, server_default=sa.sql.true())

    files: Mapped[list[File]] = relationship('File', back_populates='storage', passive_deletes=True)


class File(BaseUUID, TimestampMixin):
    """
    Модель для хранения списка файлов.
    """

    __tablename__ = 'files'

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.gen_random_uuid(),
    )

    name: Mapped[str] = mapped_column(sa.String(length=1024), nullable=False)
    size: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0, server_default='0')
    content_type: Mapped[str] = mapped_column(sa.String(length=1024), nullable=True)

    storage_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey(f'{Storage.__tablename__}.id', ondelete='cascade'),
        nullable=False,
    )
    storage: Mapped[Storage] = relationship('Storage', back_populates='files')
