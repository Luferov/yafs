from typing import Annotated

import typer
from fast_clean.container import get_container
from fast_clean.repositories.storage.schemas import S3StorageParamsSchema
from fast_clean.utils import typer_async
from rich import print

from .enums import FileStorageTypeEnum
from .schemas import StorageCreateRequestSchema
from .use_cases import AddStorageUseCase


@typer_async
async def add_s3_storage(
    endpoint: Annotated[str, typer.Option(prompt=True)],
    aws_secret_access_key: Annotated[str, typer.Option(prompt=True)],
    aws_access_key_id: Annotated[str, typer.Option(prompt=True)],
    bucket: Annotated[str, typer.Option(prompt=True)],
    port: Annotated[int, typer.Option(prompt=True)] = 443,
    secure: Annotated[bool, typer.Option(prompt=True)] = True,
) -> None:
    """
    Добавляяем новое хранилище.
    """
    async with get_container() as container:
        add_storage_use_case = await container.get(AddStorageUseCase)
        storage = await add_storage_use_case(
            StorageCreateRequestSchema(
                type=FileStorageTypeEnum.S3,
                params=S3StorageParamsSchema(
                    endpoint=endpoint,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    bucket=bucket,
                    port=port,
                    secure=secure,
                ).model_dump(),
            )
        )
        print(f'Хранилище успешно добавлено: {storage.id}')
