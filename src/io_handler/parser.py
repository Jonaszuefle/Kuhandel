from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class InputSpec:
    name: str
    prompt: str
    parser: Callable[[str], Any]
    validator: Callable[[Any], bool] = lambda x: True
    error_msg: str = "Invalid input."


def parse_id(input_str: str) -> int:
    return int(input_str)


def parse_money_list(input_str: str) -> int:
    return list(map(int, input_str.split(",")))


def parse_command_str(input_str: str) -> str:
    return input_str.strip().lower()


def validate_player_index(value: int) -> bool:
    """Validate player index is in valid range."""
    return 0 <= value < 5


def validate_money_list(value: list[int]) -> bool:
    """Validate money list format."""
    return len(value) == 6 and all(v >= 0 for v in value)


def validate_positive(value: int) -> bool:
    """Validate value is positive."""
    return value > 0
