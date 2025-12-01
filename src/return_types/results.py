from enum import Enum
from dataclasses import dataclass


class ResultType(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    CANCEL = "CANCEL"


@dataclass
class Result:
    type: ResultType
    message: str = None
