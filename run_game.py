from Results.results import Result, ResultType
from Commands.commands import BidCommand, TradeCommand, ShowStatsCommand

from Inputs.inputs import ConsoleInputHandler
from Game.game import Game



if __name__ == "__main__":
    io_handler = ConsoleInputHandler()

    game = Game()
    game.start_game()

    while game.game_is_ongoing:
    
        command = io_handler.get_command(current_player=game.current_player)
        match command:
            case BidCommand():  
                game.draw_cow_from_stack()
                game.is_donkey_cow()

        res = ResultType.FAILURE
        while res == ResultType.FAILURE:
            params = io_handler.get_inputs_for_command(command)
            command.fill(params)
            res = command.validate_command_values(game)
            if res.type == ResultType.FAILURE:
                print(res.meassage)

        if res.type == ResultType.SUCCESS:
            command.execute(game)

            match command:
                case ShowStatsCommand():
                    io_handler.print_player_stats(game.get_player_stats())
                case _:
                    game.end_turn()
        else:
            print(res.meassage)
        
        print(game.have_players_cows())

        game.is_game_over()
            
