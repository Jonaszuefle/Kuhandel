from return_types.results import Result, ResultType

class StatsHandler():
    def __init__(self, game):
        self.game = game

    def execute(self):
        stats = self.game.get_player_stats()
        msg = self.get_player_stats_msg(stats)
        print(msg)

        return Result(ResultType.SUCCESS)

    def get_player_stats_msg(self, stats: list[dict[int, list[int]]]):
        msg = ""
        for i in range(len(stats)):
            msg += f"Player {stats[i]['player_idx']} has -- {stats[i]['money']} money -- {stats[i]['cows']} cows -- {stats[i]['score']} score. \n"
        return msg