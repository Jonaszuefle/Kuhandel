from dataclasses import dataclass
from enum import Enum
from game_config.game_config import GameConfig

class ActionType(Enum):
    BID = 'BID'
    BUY_BACK = 'BUY_BACK'
    TRADE = 'TRADE'
    STATS = 'STATS'

@dataclass
class BaseAction:
    player_idx: int 

@dataclass
class Bid(BaseAction):
    value: int
    amount: list[int] = None

@dataclass 
class Trade(BaseAction):
    amount: list[int]
    card_count: int = None
    value: int = None

    def __post_init__(self):
        if self.card_count is None:
            self.card_count = self._calculate_count()
        if self.value is None:
            self.value = self._calculate_value()

    def _calculate_count(self) -> int:  
        return sum(self.amount)
    
    def _calculate_value(self) -> int:
        return [x * y for x, y in zip(self.amount, GameConfig.MONEY_CARD_VALUES)]

@dataclass
class Stats(BaseAction):
    pass

# TODO add further actions