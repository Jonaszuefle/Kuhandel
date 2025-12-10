from action_handlers.trading import TradeHandler
from interface.player_interface import PlayerInterface
from io_handler.outputs import OutputHandler
from return_types.results import ResultType, Result

from game.game import Game


class PlayTradeTurn:
    def __init__(
        self,
        player_interfaces: list[PlayerInterface],
        output_handler: OutputHandler,
        game: Game,
    ):
        self.player_interfaces = player_interfaces
        self.game = game

    def execute(self):
        current_player_idx = self.game.get_current_player_idx()

        joint_cows = self.game.get_possible_cow_trades()

        if not joint_cows:
            return Result(ResultType.FAILURE, "There are no joint cows.")

        # decide which player to challenge, plus which and how many cows
        enemy_idx, cow_type, cow_amount = self.player_interfaces[
            current_player_idx
        ].make_trade_decision(joint_cows, self.game.get_player_view(current_player_idx))

        if not self.game.get_player(enemy_idx).has_cow(cow_type, cow_amount):
            return Result(
                ResultType.FAILURE,
                f"Challenged player does not have {cow_amount} of cow {cow_type}",
            )

        if not self.game.get_current_player().has_cow(cow_type, cow_amount):
            return Result(
                ResultType.FAILURE,
                f"Current player does not have {cow_amount} of cow {cow_type}",
            )

        self.trade_handler = TradeHandler(
            cow_type, cow_amount, current_player_idx, enemy_idx
        )

        trade_challenger = self.player_interfaces[current_player_idx].make_trade_offer(
            self.game.get_player_view(current_player_idx)
        )
        if not self.game.get_player(enemy_idx).has_enough_money(
            trade_challenger.amount
        ):
            return Result(
                ResultType.FAILURE, f"Current player does not have enough money"
            )

        self.trade_handler.set_challenger_bid(trade_challenger)

        trade_contender = self.player_interfaces[enemy_idx].make_trade_offer(
            self.game.get_player_view(current_player_idx), trade_challenger.card_count
        )
        if not self.game.get_current_player().has_enough_money(trade_contender.amount):
            return Result(
                ResultType.FAILURE, f"Challenged player does not have enough money"
            )

        self.trade_handler.set_contender_bid(trade_contender)

        winner, looser = self.trade_handler.get_winner_and_loser()

        self.game.handle_trade(
            cow_type,
            cow_amount,
            enemy_idx,
            trade_challenger.amount,
            trade_contender.amount,
            winner,
            looser,
        )  # TODO
        self.game.end_turn()

        return Result(ResultType.SUCCESS)
