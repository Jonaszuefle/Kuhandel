from interface.player_interface import PlayerInterface
from return_types.action import ActionType
from game.player_view import PlayerView


class BotPlayer(PlayerInterface):  # TODO finish
    def __init__(self, player_idx: int):
        self.player_idx = player_idx

    def choose_action(self, view):
        if not view.private.joint_cows:
            return ActionType.BID

    # Bid
    def make_bid_decision(self, view, bid_handler):
        pass

    # if somone has small money and same cows as me -> trade
    # normaly just go for bid
    # depending on the money stage

    # never choose stats

    def make_buy_back_decision(self, view, highest_bid):
        if view.private.money_value * 0.9 < highest_bid.value:
            return False

        bidder_idx = highest_bid.player_idx
        bidder_info = view.public.player_infos[bidder_idx]

        if bidder_info.cow_cards.count(highest_bid.cow_type) >= 3:
            return True

    def choose_money_cards(self, view, highest_bid, buyer_idx):
        pass

    # use the implemented money alg

    # Trade
    def make_trade_decision(self, view, joint_cows):
        pass

    # take somone who has many cows and no money
    # take somone who has the same cow as me and i am close to finishing the set

    def make_trade_offer(self, view, card_count=None):
        pass

    # depending on how many cow cards the other one has set money
    # depending on the other players money cards set money
    # depending on the money stage

    def win_bid_probability(self, player_view) -> float:
        pass

    def win_trade_probability(self, player_view: PlayerView) -> float:
        for pl_idx, cows in player_view.private.joint_cows.items():
            if pl_idx == self.player_idx:
                continue
