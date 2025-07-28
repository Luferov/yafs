import uuid
from functools import partial
from typing import Self

from fast_clean.exceptions import BusinessLogicException
from fast_clean.settings import CoreSettingsSchema
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler


class StoragePathNotFoundError(BusinessLogicException):
    @property
    def msg(self: Self) -> str:
        return 'Запрашиваемся внешнее хранилище без идентификатора'


class StorageTypeNotFoundError(BusinessLogicException):
    @property
    def msg(self: Self) -> str:
        return 'Передан не поддерживаемый тип репозитория'


class FileNotFoundError(BusinessLogicException):
    def __init__(self, file_id: uuid.UUID) -> None:
        self.file_id = file_id

    @property
    def msg(self: Self) -> str:
        return f'Файл {self.file_id} не найден'


class BadUploadFileError(BusinessLogicException):
    @property
    def msg(self: Self) -> str:
        return 'Файл должен содержать название и размер'


async def storage_found_exception_handler(
    settings: CoreSettingsSchema, request: Request, error: StoragePathNotFoundError | StorageTypeNotFoundError
) -> Response:
    """
    Обработчик ошибок, связанный с тем, что идентификатор хранилища не найден
    """
    return await http_exception_handler(
        request,
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[error.get_schema(settings.debug).model_dump()],
        ),
    )


async def bad_upload_file_exception_handler(
    settings: CoreSettingsSchema, request: Request, error: BadUploadFileError
) -> Response:
    """
    Обработчик ошибок, связанный с тем, что идентификатор хранилища не найден
    """
    return await http_exception_handler(
        request,
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[error.get_schema(settings.debug).model_dump()],
        ),
    )


async def file_not_found_exception_handler(
    settings: CoreSettingsSchema, request: Request, error: FileNotFoundError
) -> Response:
    """
    Обработчик ошибок, связанный с тем, что идентификатор хранилища не найден
    """
    return await http_exception_handler(
        request,
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[error.get_schema(settings.debug).model_dump()],
        ),
    )


def use_exceptions_handlers(app: FastAPI, settings: CoreSettingsSchema) -> None:
    app.exception_handler(StoragePathNotFoundError)(partial(storage_found_exception_handler, settings))
    app.exception_handler(StorageTypeNotFoundError)(partial(storage_found_exception_handler, settings))
    app.exception_handler(BadUploadFileError)(partial(bad_upload_file_exception_handler, settings))
    app.exception_handler(FileNotFoundError)(partial(file_not_found_exception_handler, settings))
