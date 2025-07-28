from enum import StrEnum, auto


class FileStorageTypeEnum(StrEnum):
    """
    Типы локальных подключений.
    """

    S3 = auto()
