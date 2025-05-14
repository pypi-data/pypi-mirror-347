from enum import Enum


class FinishedStatus(str, Enum):
    FINISHED = "finished"

    def __str__(self) -> str:
        return str(self.value)
