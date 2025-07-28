from fast_clean.repositories import DbCrudRepository

from ..models import File
from ..schemas import FileCreateSchema, FileReadSchema, FileUpdateSchema


class FileDbRepository(DbCrudRepository[File, FileReadSchema, FileCreateSchema, FileUpdateSchema]):
    """
    Репозиторий для работы с файлами.
    """

    ...
