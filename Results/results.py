from enum import Enum
from dataclasses import dataclass

class ResultType(Enum):
        SUCCESS = 'SUCCESS'
        FAILURE = 'FAILURE'

@dataclass
class Result:
    type: ResultType
    meassage: str = None
