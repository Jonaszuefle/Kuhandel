from return_types.results import Result, ResultType
from return_types.action import ActionType
from interface.player_interface import HumanPlayer

from io_handler.inputs import ConsoleInputHandler
from application.play_auction import PlayBidTurn
from application.play_trade import PlayTradeTurn
from application.show_stats import StatsHandler
from game.game import Game


if __name__ == "__main__":
    io_handler = ConsoleInputHandler()

    interfaces = [HumanPlayer(0, io_handler),
                  HumanPlayer(1, io_handler),
                  HumanPlayer(2, io_handler)]

    game = Game(len(interfaces))
    game.start_game()

    while game.game_is_ongoing:
    
        action = interfaces[game.get_current_player_idx()].choose_action(game)

        match action:
            case ActionType.BID:
                auction_handler = PlayBidTurn(interfaces, game)      # TODO where to add input check?
                res = auction_handler.execute()
            case ActionType.TRADE:
                trade_handler = PlayTradeTurn(interfaces, game)
                res = trade_handler.execute()
            case ActionType.STATS:
                stats_handler = StatsHandler(game)
                res = stats_handler.execute()
        
        if res.type == ResultType.FAILURE:
            print(res.message)
        
        game.is_game_over()

        # command = io_handler.get_command(current_player=game.get_current_player_idx())
        
        # command.prepare(game)

        # res = Result(ResultType.FAILURE)        # bid/trade logic
        # while res.type == ResultType.FAILURE:
        #     params = io_handler.get_inputs_for_command(command)

        #     command.fill(params)
        #     res = command.validate_command_values(game)

        #     if res.type == ResultType.FAILURE:
        #         print(res.message)
        #     elif res.type == ResultType.CANCEL:
        #         break    

        # if res.type == ResultType.CANCEL:
        #     continue  
        
        # res = command.execute(game)

        # if not res.message is None:
        #     print(res.message)


        game.is_game_over()
            
