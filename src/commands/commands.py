from abc import ABC, abstractmethod
from enum import Enum
from results.results import Result, ResultType
from inputs.parser import InputSpec, parse_command_str, parse_id, parse_money_list, validate_money_list
from game.game import Game


class CommandState(Enum):
    CREATED = 0
    PREPARED = 1
    FILLED = 2
    VALIDATED = 3
    EXECUTED = 4


class Command(ABC):
    def __init__(self):
        self.command_state = CommandState.CREATED

    def prepare(self, game: Game) -> Result:
        """Method to handel game logik (e.g. card draw) which has to be done prior to command execution."""
        self.command_state = CommandState.PREPARED
        return (
            Result(ResultType.SUCCESS)
            if self.command_state == CommandState.PREPARED
            else Result(ResultType.FAILURE, "Command is in the wrong state! 1")
        )

    def fill(self, params: dict[int, list[int]]):
        """Fill the commands with the user input."""
        self.command_state = CommandState.FILLED

    def validate_command_values(self, game: Game):
        """Validate user inputs."""
        self.command_state = CommandState.VALIDATED
        return (
            Result(ResultType.SUCCESS)
            if self.command_state == CommandState.VALIDATED
            else Result(ResultType.FAILURE, "Command is in the wrong state! 3")
        )

    @abstractmethod
    def execute(self, game: Game):
        """ "Execute user commands using game logic."""
        pass


class TradeCommand(Command):
    input_specs = [
        InputSpec("cow_type", "What type of cow? ", parse_id),
        InputSpec("cow_amount", "How many cows? ", parse_id),
        InputSpec("challenged_player", "Who was challenged? ", parse_id),
        InputSpec("money_amount_current", "How much money -- current? ", parse_money_list, validate_money_list),
        InputSpec("money_amount_challenged", "How much money -- challenged? ", parse_money_list, validate_money_list),
    ]

    def fill(self, param_dict: dict[int, list[int]]):
        self.param_dict = param_dict
        self.command_state = CommandState.FILLED

    def validate_command_values(self, game: Game) -> Result:
        try: 
            if self.param_dict["quit"]:
                return Result(ResultType.CANCEL)
        except:
            pass

        current_player = game.get_current_player()
        challanged_player = self.param_dict["challenged_player"]

        msg = ""
        res = True

        if not game._players[challanged_player].has_cow(
            self.param_dict["cow_type"], self.param_dict["cow_amount"]
        ):
            msg += f"Player {challanged_player} has not enough cow! \n"
            res = False

        if not game._players[current_player].has_cow(
            self.param_dict["cow_type"], self.param_dict["cow_amount"]
        ):
            msg += f"Player {current_player} has not enough cow! \n"
            res = False

        if not game._players[challanged_player].has_enough_money(
            self.param_dict["money_amount_challenged"]
        ):
            msg += f"Player {challanged_player} has not enough money! \n"
            res = False

        if not game._players[current_player].has_enough_money(
            self.param_dict["money_amount_current"]
        ):
            msg += f"Player {current_player} has not enough money! \n"
            res = False

        if not res:
            return Result(ResultType.FAILURE, msg)

        else:
            return Result(ResultType.SUCCESS)

    def execute(self, game: Game):
        current_player = game.get_current_player()
        challanged_player = self.param_dict["challenged_player"]

        winner_idx = (
            current_player
            if game.get_money_value(self.param_dict["money_amount_current"])
            > game.get_money_value(self.param_dict["money_amount_challenged"])
            else challanged_player
        )
        looser_idx = (
            current_player if winner_idx != current_player else challanged_player
        )

        self.param_dict["winnder_idx"] = winner_idx
        self.param_dict["looser_idx"] = looser_idx

        game.handle_trade(**self.param_dict)
        self.command_state = CommandState.EXECUTED

        game.end_turn()

        if (
            self.param_dict["money_amount_current"]
            == self.param_dict["money_amount_challenged"]
        ):
            return Result(Result.SUCCESS, meassage="It's a draw!")
        else:
            return Result(ResultType.SUCCESS, f"Player {winner_idx} won!")


class BidCommand(Command):
    input_specs = [
        InputSpec("player_who_gets_cow", "Who gets the cow? ", parse_id),
        InputSpec("player_who_gets_money", "Who gets the money? ", parse_id),
        InputSpec("money_amount", "How much money? ", parse_money_list, validate_money_list),
    ]

    def fill(self, param_dict: dict[int, list[int]]):
        self.param_dict = param_dict
        self.command_state = CommandState.FILLED

    def prepare(self, game: Game) -> Result:
        """ "Draw a card bevore getting player inputs"""
        game.draw_cow_from_stack()
        if game.is_donkey_cow():
            game.inflate_player_money()

        self.command_state = CommandState.PREPARED
        return Result(ResultType.SUCCESS)

    def execute(self, game: Game) -> Result:
        game.handle_bid(**self.param_dict)
        self.command_state = CommandState.EXECUTED

        game.end_turn()

        return Result(ResultType.SUCCESS)

    def validate_command_values(self, game: Game) -> Result:
        try: 
            if self.param_dict["quit"]:
                game.undo_cow_card_craw()
                if game.is_donkey_cow:
                    game.undo_inflation()
                return Result(ResultType.CANCEL)
        except:
            pass
    
        if game._players[self.param_dict["player_who_gets_cow"]].has_enough_money(
            self.param_dict["money_amount"]
        ):
            return Result(ResultType.SUCCESS)
        else:
            self.command_state = CommandState.VALIDATED
            return Result(
                ResultType.FAILURE,
                f"Player {self.param_dict['player_who_gets_cow']} has not enough money!",
            )


class ShowStatsCommand(Command):
    input_specs = None

    def execute(self, game: Game) -> Result:
        stats = game.get_player_stats()
        msg = self.get_player_stats_msg(stats)

        self.command_state = CommandState.EXECUTED

        return Result(ResultType.SUCCESS, msg)

    def get_player_stats_msg(self, stats: list[dict[int, list[int]]]):
        msg = ""
        for i in range(len(stats)):
            msg += f"Player {stats[i]['player_idx']} has -- {stats[i]['money']} money -- {stats[i]['cows']} cows -- {stats[i]['score']} score. \n"
        return msg
