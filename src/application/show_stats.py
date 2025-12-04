from return_types.results import Result, ResultType
from io_handler.console_outputs import OutputHandler
from game.game import Game

class StatsHandler():
    def __init__(self, output_handler: OutputHandler, game: Game):
        self.game = game
        self.output_handler = output_handler

    def execute(self):
        player_view = self.game.get_player_view(self.game.get_current_player_idx())

        card_stack_count = self.game.card_stack.get_num_cards()

        self.output_handler.show_stats(player_view, card_stack_count)

        return Result(ResultType.SUCCESS)
