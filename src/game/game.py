import random
from player.players import Player

from game_config.game_config import GameConfig


class Game:
    _money_inflation_stage = 2
    __player_limit = [2, 5]  # for optional input
    game_is_ongoing = True

    def start_game(self):
        self._card_stack = self.get_random_starting_stack(GameConfig.COW_CARD_VALUES)
        self._is_card_stack_empty = False

        self.num_players = 3
        self._players = self.get_list_of_players()
        self._current_player = self.get_random_starting_player()
        self._current_turn = 0

    def get_list_of_players(self) -> list[Player]:
        players = []
        for i in range(self.num_players):
            players.append(Player(i))
        return players

    def get_random_starting_player(self) -> int:
        return random.randint(0, self.num_players - 1)

    def get_random_starting_stack(self, cow_cards: list[int]) -> list[int]:
        card_stack = []
        for i in range(len(cow_cards)):
            for j in range(4):
                card_stack.append(cow_cards[i])
        random_cow_cards = random.sample(card_stack, len(card_stack))

        return random_cow_cards

    def get_current_player(self):
        return self._current_player

    def set_current_player(self, idx: int):
        self._current_player = idx

    def get_current_turn(self):
        return self._current_turn

    def set_current_turn(self):
        """Increment turn index by one"""
        self._current_turn = self._current_turn + 1

    ### Game Logik ###

    def draw_cow_from_stack(self):
        self.current_cow_draw = self._card_stack[0]
        print(f"Bid for COW {self.current_cow_draw}!")
        if len(self._card_stack) == 1:
            print("Last card was drawn.")
            self._is_card_stack_empty = True

        self._card_stack.pop(0)

    def undo_cow_card_craw(self):
        self._card_stack.insert(0, self.current_cow_draw)

    def is_donkey_cow(self):  # increase inflation
        if self.current_cow_draw == GameConfig.DONKEY_COW:
            print("It's a donkey!")
            return True
        else:
            return False
        
    def inflate_player_money(self):
        money = [0, 0, 0, 0, 0, 0]
        money[self._money_inflation_stage] = 1
        for player in self._players:
            player.add_money(money)
        self._money_inflation_stage += 1

    def undo_inflation(self):
        money = [0, 0, 0, 0, 0, 0]
        self._money_inflation_stage -= 1

        money[self._money_inflation_stage] = 1
        for player in self._players:
            player.remove_money(money)

    def is_game_over(self):
        if self._is_card_stack_empty and not self.have_players_cows():
            self.game_is_ongoing = False

            scores = []
            for i in range(self.num_players):
                scores.append(self._players[i].get_score())
            print(f"Game OVER -- Scores: {scores}")

    def have_players_cows(self):
        has_cow = False
        for i in range(self.num_players):
            if any(self._players[i].cow_cards_obj.get_cow_inventory()):
                has_cow = True
                break
        return has_cow
        

    # Turn based

    def process_command(self):  # method for future use
        is_command_valid = True
        if is_command_valid:
            pass

    def end_turn(self):
        for i in range(self.num_players):
            self._players[i].update_score()

        self.set_current_turn()
        self.set_current_player(
            (self.get_current_turn() + self.get_current_player()) % self.num_players
        )

    def handle_bid(self, player_who_gets_cow: int, player_who_gets_money: int, money_amount: list[int]):
        self._players[player_who_gets_cow].add_cow(self.current_cow_draw, 1)
        self._players[player_who_gets_money].add_money(money_amount)
        self._players[player_who_gets_cow].remove_money(money_amount)

    def handle_trade(
        self,
        cow_type: int,
        cow_amount: int,
        challenged_player: int,
        money_amount_current: list[int],
        money_amount_challenged: list[int],
        winner_idx: int,
        looser_idx: int,
    ):
        self._players[winner_idx].add_cow(cow_type, cow_amount)
        self._players[looser_idx].remove_cow(cow_type, cow_amount)

        self._players[challenged_player].add_money(money_amount_current)
        self._players[challenged_player].remove_money(money_amount_challenged)

        self._players[self.get_current_player()].add_money(money_amount_challenged)
        self._players[self.get_current_player()].remove_money(money_amount_current)

    def get_money_value(self, money_amount: list[int]) -> int:
        return sum([a * b for a, b in zip(money_amount, GameConfig.MONEY_CARD_VALUES)])

    def get_player_stats(self) -> list[dict[int, list[int]]]:
        stats = []
        for i in range(self.num_players):
            stats.append(
                {
                    "player_idx": self._players[i].get_player_idx(),
                    "money": self._players[i].money_cards_obj.get_money_inventory(),
                    "cows": self._players[i].cow_cards_obj.get_cow_inventory(),
                    "score": self._players[i].get_score(),
                }
            )
        return stats
