from return_types.results import Result, ResultType
from return_types.action import ActionType
from interface.human_interface import HumanPlayer

from io_handler.inputs import ConsoleInputHandler
from io_handler.outputs import ConsoleOutputHandler

from application.play_auction import PlayBidTurn
from application.play_trade import PlayTradeTurn
from application.show_stats import StatsHandler
from game.game import Game


if __name__ == "__main__":
    input_handler = ConsoleInputHandler()
    output_handler = ConsoleOutputHandler()

    input_interfaces = [HumanPlayer(0, input_handler),
                  HumanPlayer(1, input_handler),
                  HumanPlayer(2, input_handler)]

    game = Game(len(input_interfaces))
    game.start_game()

    while game.game_is_ongoing:
    
        action = input_interfaces[game.get_current_player_idx()].choose_action(game)

        match action:
            case ActionType.BID:
                auction_handler = PlayBidTurn(input_interfaces, output_handler, game)      # TODO where to add input check?
                res = auction_handler.execute()
            case ActionType.TRADE:
                trade_handler = PlayTradeTurn(input_interfaces, output_handler, game)
                res = trade_handler.execute()
            case ActionType.STATS:
                stats_handler = StatsHandler(output_handler, game)
                res = stats_handler.execute()
        
        if res.type == ResultType.FAILURE:
            output_handler.show_message(res.message)

        scores = game.is_game_over()

    output_handler.show_final_score(scores)
            
