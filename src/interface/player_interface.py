from abc import ABC, abstractmethod

from action_handlers.bidding import BidHandler
from return_types.action import ActionType, Bid, Trade
from game.player_view import PlayerView


class PlayerInterface(ABC):
    # General
    @abstractmethod
    def choose_action(self, view: PlayerView) -> ActionType:
        """Choose a game action (bid/trade/show stats)"""
        pass

    # Bidding
    @abstractmethod
    def make_bid_decision(
        self, view: PlayerView, bid_handler: BidHandler
    ) -> Bid | None:
        """Decision making during the bidding process. Return Bid(idx, amount), if player wants to place bid, else Bid(idx, None)"""
        pass

    @abstractmethod
    def make_buy_back_decision(self, highest_bid: Bid) -> bool:
        """Ask bid master weather to buy the current cow using the highest bid."""
        pass

    @abstractmethod
    def choose_money_cards(self, highest: Bid, buyer_idx: int) -> list[int]:
        """Player must choose the money cards to pay the bid value"""
        pass

    # Trading
    @abstractmethod
    def make_trade_decision(self, joint_cows: list[int], view: PlayerView) -> int:
        """Decide which player to challenge, and how many and which cow(s). Return int,int,int"""
        pass

    @abstractmethod
    def make_trade_offer(self, view: PlayerView, card_count: int = None) -> Trade:
        """Decide how much to bid for the trade"""
        pass
