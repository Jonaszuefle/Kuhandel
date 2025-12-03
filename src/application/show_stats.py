from return_types.results import Result, ResultType
from io_handler.outputs import OutputHandler

class StatsHandler():
    def __init__(self, output_handler: OutputHandler, game):
        self.game = game
        self.output_handler = output_handler

    def execute(self):
        stats = self.game.get_player_stats()

        card_stack_count = self.game.card_stack.get_num_cards()

        self.output_handler.show_stats(stats, card_stack_count)

        return Result(ResultType.SUCCESS)
