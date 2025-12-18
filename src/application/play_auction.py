from action_handlers.bidding import BidHandler
from interface.player_interface import PlayerInterface
from io_handler.console_outputs import OutputHandler
from return_types.results import ResultType, Result
from return_types.action import Bid
from game_config.game_config import GameConfig

from game.game import Game


class PlayBidTurn:
    def __init__(
        self,
        player_interfaces: list[PlayerInterface],
        output_handler: OutputHandler,
        game: Game,
    ):
        self.player_interfaces = player_interfaces
        self.output_handler = output_handler
        self.game = game

    def execute(self):
        if self.game.card_stack.is_empty():
            return Result(ResultType.FAILURE, "Card stack is empty")

        auctioneer_idx = self.game.get_current_player_idx()

        cow_draw = self._draw_and_reveal_card()

        bid_handler = BidHandler(
            auctioneer_idx, self.game.num_players
        )  # TODO write getter

        self._run_auction_loop(bid_handler)

        winner_bid = bid_handler.get_winner_bid()

        buyer, seller = self._determine_buyer_and_seller(winner_bid)

        if GameConfig.AUTOMATIC_MONEY_CARD_CHOICE:
            money_cards = self.game.get_player(buyer).get_optimal_payment(
                winner_bid.value
            )
        else:
            money_cards = self.player_interfaces[buyer].choose_money_cards(
                self.game.get_player_view(buyer), winner_bid, buyer
            )

        self.game.handle_bid(cow_draw, buyer, seller, money_cards)

        self.game.end_turn()

        return Result(ResultType.SUCCESS)

    def _draw_and_reveal_card(self) -> int:
        """Draws and reveals a cow card from the stack, handling donkey events if necessary"""
        cow_draw = self.game.card_stack.draw_card()
        self.output_handler.show_cow_draw(cow_draw)

        if self.game.card_stack.is_donkey_cow(cow_draw):
            self.game.bank.inflate_player_money(self.game.get_all_players())
            self.output_handler.show_donkey_event(self.game.bank.get_inflation_value())
        return cow_draw

    def _run_auction_loop(self, bid_handler: BidHandler):
        """Runs the auction loop until a winner is found"""
        while not bid_handler.is_complete():
            active_bidders = list(bid_handler.remaining_players)

            for pl_idx in active_bidders:
                self._handle_single_player_bid(pl_idx, bid_handler)

                if bid_handler.is_complete():  # earlie break
                    break

    def _handle_single_player_bid(self, player_idx: int, bid_handler: BidHandler):
        """Handles the case where only one player is bidding"""
        interface = self.player_interfaces[player_idx]
        view = self.game.get_player_view(player_idx)

        bid = interface.make_bid_decision(view, bid_handler)

        if bid.value is None:  # player wants to pass
            bid_handler.pass_bid(player_idx)
        else:
            result = bid_handler.place_bid(self.game.get_player(player_idx), bid.value)

            if result.type == ResultType.FAILURE:
                self.output_handler.show_message(result.message)
                bid_handler.pass_bid(bid.player_idx)

    def _determine_buyer_and_seller(self, winner_bid: Bid) -> tuple[int, int]:
        """Determines the winner and seller based on the bid results and possible buy-back"""
        auctioneer_idx = self.game.get_current_player_idx()

        if winner_bid.value < self.game.get_current_player().get_money_value():
            wants_buy_back = self.player_interfaces[
                auctioneer_idx
            ].make_buy_back_decision(
                self.game.get_player_view(auctioneer_idx), winner_bid
            )
        else:
            wants_buy_back = False

        if wants_buy_back:
            return auctioneer_idx, winner_bid.player_idx
        else:
            return winner_bid.player_idx, auctioneer_idx
