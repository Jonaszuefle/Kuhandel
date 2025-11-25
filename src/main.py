from results.results import Result, ResultType
from inputs.inputs import ConsoleInputHandler
from game.game import Game


if __name__ == "__main__":
    io_handler = ConsoleInputHandler()

    game = Game()
    game.start_game()

    while game.game_is_ongoing:
    
        command = io_handler.get_command(current_player=game.get_current_player())
        
        command.prepare(game)

        res = Result(ResultType.FAILURE)        # bid/trade logic
        while res.type == ResultType.FAILURE:
            params = io_handler.get_inputs_for_command(command)

            command.fill(params)
            res = command.validate_command_values(game)

            if res.type == ResultType.FAILURE:
                print(res.message)
            elif res.type == ResultType.CANCEL:
                break    

        if res.type == ResultType.CANCEL:
            continue  
        
        res = command.execute(game)

        if not res.message is None:
            print(res.message)


        game.is_game_over()
            
