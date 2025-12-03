from action_handlers.bidding import BidHandler
from interface.player_interface import PlayerInterface
from io_handler.outputs import OutputHandler
from return_types.results import ResultType, Result
from game_config.game_config import GameConfig

from game.game import Game

class PlayBidTurn:

    def __init__(self, player_interfaces: list[PlayerInterface], output_handler: OutputHandler, game: Game):
        self.player_interfaces = player_interfaces
        self.output_handler = output_handler
        self.game = game

    def execute(self):

        if self.game.card_stack.is_empty():
            return Result(ResultType.FAILURE, f"Card stack is empty")

        cow_draw = self.game.card_stack.draw_card()
        self.output_handler.show_cow_draw(cow_draw)

        if self.game.card_stack.is_donkey_cow(cow_draw):
            self.game.bank.inflate_player_money(self.game.get_list_of_players())
            self.output_handler.show_donkey_event(self.game.bank.get_inflation_value())

        self.bid_handler = BidHandler(self.game.get_current_player_idx(), self.game.num_players) #TODO write getter

        # Auction loop
        while True:
            for pl_idx in self.bid_handler.remaining_players:
                bid = self.player_interfaces[pl_idx].make_bid_decision(self.game.get_player_view(pl_idx), self.bid_handler)

                if bid.value is None:   # player wants to pass
                    self.bid_handler.pass_bid(bid.player_idx)
                else:
                    result = self.bid_handler.place_bid(self.game.get_player(pl_idx), bid.value)

                    if result.type == ResultType.FAILURE:
                        self.bid_handler.pass_bid(bid.player_idx)
                        self.output_handler.show_message(result.message)

            if self.bid_handler.is_complete():
                break

        winner_bid = self.bid_handler.get_winner_bid()
        if winner_bid.value < self.game.get_current_player().get_money_value():
            wants_buy_back = self.player_interfaces[self.bid_handler.bid_master].make_buy_back_decision(winner_bid)
        else:
            wants_buy_back = False

        if wants_buy_back:
            buyer = self.bid_handler.bid_master
            seller = winner_bid.player_idx
        else:
            buyer = winner_bid.player_idx
            seller = self.bid_handler.bid_master

        if GameConfig.AUTOMATIC_MONEY_CARD_CHOICE:
            money_cards = self.game.get_player(buyer).get_optimal_payment(winner_bid.value)
        else:
            money_cards = self.player_interfaces[buyer].choose_money_cards(winner_bid, buyer)

        self.game.handle_bid(cow_draw, buyer, seller, money_cards)

        self.game.end_turn()

        return Result(ResultType.SUCCESS)