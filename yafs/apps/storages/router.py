import uuid
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Path, Query, UploadFile, status
from fastapi.responses import StreamingResponse

from .schemas import FileReadSchema, StorageCreateRequestSchema, StorageResponseSchema
from .use_cases import AddStorageUseCase, DeleteFilesUseCase, FileInfoUseCase, ReadFileUseCase, UploadFilesUseCase

router = APIRouter(prefix='/storage', tags=['Storages'])


@router.post('', status_code=status.HTTP_201_CREATED)
@inject
async def add_storage(
    storage_schema: StorageCreateRequestSchema,
    add_storage_use_case: FromDishka[AddStorageUseCase],
) -> StorageResponseSchema:
    return await add_storage_use_case(storage_schema)


@router.post('/{storageId}/files', status_code=status.HTTP_201_CREATED)
@inject
async def upload_file(
    storage_id: Annotated[uuid.UUID, Path(alias='storageId')],
    files: list[UploadFile],
    upload_files_use_case: FromDishka[UploadFilesUseCase],
) -> list[FileReadSchema]:
    return await upload_files_use_case(storage_id, files)


@router.get('/{storageId}/files/{fileId}')
@inject
async def get_file_info(
    storage_id: Annotated[uuid.UUID, Path(alias='storageId')],
    file_id: Annotated[uuid.UUID, Path(alias='fileId')],
    file_info_use_case: FromDishka[FileInfoUseCase],
) -> FileReadSchema:
    return await file_info_use_case(file_id)


@router.get('/{storageId}/files/{fileId}/download')
@inject
async def get_file_streaming_response(
    storage_id: Annotated[uuid.UUID, Path(alias='storageId')],
    file_id: Annotated[uuid.UUID, Path(alias='fileId')],
    read_file_use_case: FromDishka[ReadFileUseCase],
) -> StreamingResponse:
    return StreamingResponse(await read_file_use_case(file_id))


@router.delete('/{storageId}/files', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_file(
    storage_id: Annotated[uuid.UUID, Path(alias='storageId')],
    file_ids: Annotated[list[uuid.UUID], Query(alias='fileIds')],
    delete_files_use_case: FromDishka[DeleteFilesUseCase],
) -> None:
    await delete_files_use_case(file_ids)
