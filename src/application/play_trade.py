from action_handlers.trading import TradeHandler
from interface.general_interface import PlayerInterface
from return_types.results import ResultType, Result

from game.game import Game

class PlayTradeTurn:

    def __init__(self, player_interfaces: list[PlayerInterface], game: Game):
        self.player_interfaces = player_interfaces
        self.game = game

    def execute(self):

        current_player_idx = self.game.get_current_player_idx()
        
        joint_cows = self.game.get_possible_cow_trades()

        if joint_cows is None:
            return Result(ResultType.FAILURE, "There are no joint cows.")

        # decide which player to challenge, plus which and how many cows
        enemy_idx, cow_type, cow_amount = self.player_interfaces[current_player_idx].make_trade_decision(joint_cows, self.game.get_player_view(current_player_idx))

        self.trade_handler = TradeHandler(cow_type, cow_amount, current_player_idx, enemy_idx) 

        trade_challenger = self.player_interfaces[current_player_idx].make_trade_offer(self.game.get_player_view(current_player_idx))
        self.trade_handler.set_challenger_bid(trade_challenger)

        trade_contender = self.player_interfaces[enemy_idx].make_trade_offer(self.game.get_player_view(current_player_idx), trade_challenger.card_count)
        self.trade_handler.set_contender_bid(trade_contender)
        
        winner, looser = self.trade_handler.get_winner_and_loser()

        self.game.handle_trade(cow_type, cow_amount, enemy_idx, trade_challenger.amount, trade_contender.amount, winner, looser)  # TODO
        self.game.end_turn()


        return Result(ResultType.FAILURE)

        

        