from interface.player_interface import PlayerInterface
from game.player_view import PlayerView


class HumanPlayer(PlayerInterface):
    # Input
    def __init__(self, player_idx: int, io_handler):
        self.player_idx = player_idx
        self.io_handler = io_handler

    def choose_action(self, view):
        return self.io_handler.ask_for_action(self.player_idx)

    # Bid
    def make_bid_decision(self, view, bid_handler):
        return self.io_handler.ask_for_bid(
            self.player_idx, bid_handler.get_highest_bid()
        )

    def make_buy_back_decision(self, highest_bid):
        return self.io_handler.ask_for_buy_back(self.player_idx, highest_bid)

    def choose_money_cards(self, highest_bid, buyer_idx):
        return self.io_handler.ask_for_money_cards(highest_bid, buyer_idx)

    # Trade
    def make_trade_decision(self, joint_cows, view):
        return self.io_handler.ask_for_trade(joint_cows)

    def make_trade_offer(self, view, card_count=None):
        return self.io_handler.ask_for_trade_offer(self.player_idx, card_count)
