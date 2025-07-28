from enum import StrEnum, auto


class TriggerTypeEnum(StrEnum):
    INTERVAL = auto()
    CRON = auto()
