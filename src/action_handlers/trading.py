from dataclasses import dataclass
from return_types.results import Result, ResultType
from return_types.action import Trade

class TradeHandler:
    """Manages the trade round"""
    def __init__(self, cow_type, cow_amount, challenger, contender):
        self.cow_type = cow_type
        self.cow_amount = cow_amount
        self.challenger = challenger
        self.contender = contender
        self.challenger_bid: Trade
        self.challenger_bid: Trade

    def set_challenger_bid(self, trade: Trade):
        """Challenger bids first"""
        self.challenger_bid = trade
    
    def set_contender_bid(self, trade: Trade):
        """Contender bids second. Getting information about amount of cards of challenger"""
        self.contender_bid = trade

    def get_winner_and_loser(self) -> int | None:
        """Determine the winner, based on the trade offers. Return None if its a draw"""
        ch = self._calculate_value(self.challenger_bid)
        con = self._calculate_value(self.contender_bid)

        if ch > con:
            return self.challenger, self.contender
        elif ch < con:
            return self.contender, self.challenger
        else:
            return None

    def _calculate_value(self, trade: Trade) -> int:
        values = [0, 10, 50, 100, 200, 500, 1000]
        return sum(value * values[i] for i, value in enumerate(trade.amount))