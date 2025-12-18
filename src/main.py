from return_types.results import ResultType
from return_types.action import ActionType
from interface.human_interface import HumanPlayer
# from interface.bot_interface import BotPlayer

from io_handler.console_inputs import ConsoleInputHandler
from io_handler.console_outputs import ConsoleOutputHandler

from application.play_auction import PlayBidTurn
from application.play_trade import PlayTradeTurn
from application.show_stats import StatsHandler
from game.game import Game


if __name__ == "__main__":
    player_names = ["Alice", "Bob", "Charlie", "David"]

    input_handler = ConsoleInputHandler(player_names)
    output_handler = ConsoleOutputHandler()

    input_interfaces = [HumanPlayer(i, input_handler) for i in range(3)]
    # input_interfaces.append(BotPlayer(3))

    game = Game(len(input_interfaces), list(player_names[: len(input_interfaces)]))
    game.start_game()

    while game.game_is_ongoing:
        current_player_idx = game.get_current_player_idx()
        game_view = game.get_player_view(current_player_idx)

        action = input_interfaces[current_player_idx].choose_action(game_view)

        match action:
            case ActionType.BID:
                auction_handler = PlayBidTurn(input_interfaces, output_handler, game)
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
