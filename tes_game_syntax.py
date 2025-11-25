from results.results import Result
from Commands.commands import BidCommand, TradeCommand, ShowStatsCommand

from Inputs.inputs import ConsoleInputHandler
from Game.game import Game


if __name__ == "__main__":
    inptHandler = ConsoleInputHandler()

    game = Game()
    game.start_game()

    dict = {
        "cow_amount": 1,
        "player_who_gets_cow": 0,
        "player_who_gets_money": 1,
        "money_amount": [0, 0, 1, 0, 0, 0],
    }

    command = BidCommand()
    param = inptHandler.get_inputs_for_command(command)
    print(param)
    command.fill(param)
    res = command.validate_command_values(game)
    print(res)
