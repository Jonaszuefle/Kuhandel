import random
from player.players import Player
from game.player_view import PlayerView, PublicView, PrivateView
from game_config.game_config import GameConfig

#TODO public game info. kuh karten, wie viele geld karten, game view? 


class Game:
    _money_inflation_stage = 2
    __player_limit = [2, 5]  # TODO optional
    game_is_ongoing = True

    def __init__(self, num_players):
        self.num_players = num_players

    def start_game(self):
        self._card_stack = self.get_random_starting_stack(GameConfig.COW_CARD_VALUES)
        self._is_card_stack_empty = False

        self._players = self.get_list_of_players()
        self._current_player = self.get_random_starting_player()
        self._current_turn = 0
        self._active_players = list(range(self.num_players))

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
    
    def get_player(self, idx: int):
        return self._players[idx]
    
    def get_current_player(self) -> Player:
        """Returns the current player"""
        return self._players[self._current_player]
    
    def get_other_players(self) -> list[Player]:
        """Return all players expect the current player"""
        current = self.get_current_player_idx()
        return [self.get_player(i) for i in range(self.num_players) if i != current]

    def get_current_player_idx(self) -> int:
        """Returns the index of the current player"""
        return self._current_player

    def set_current_player(self, idx: int):
        """Sets the new index of the current player"""
        self._current_player = idx

    def get_current_turn(self):
        """Get the current count of turns"""
        return self._current_turn

    def set_current_turn(self):
        """Increment turn index by one"""
        self._current_turn = self._current_turn + 1

    def get_money_value(self, money_amount: list[int]) -> int:
        """Retrun the sum of money cards"""
        return sum([a * b for a, b in zip(money_amount, GameConfig.MONEY_CARD_VALUES)])
    
    def remove_active_player(self, idx):
        """Remove an player if he is not active anymore"""
        self._active_players.remove(idx)
    
    def get_player_view(self, player_idx: int) -> PlayerView:
        """Return the player view for the given player index"""
        player = self.get_player(player_idx)
        other_players = [p for p in self.get_list_of_players() if p.get_player_idx() != player_idx]

        public_player_view = []
        for player in other_players:
            public_player_view.append(PublicView(player.get_player_idx(), player.get_cow_inventory(), player.get_money_cards_count(), player.get_score()))
        
        private_view = PrivateView(player.get_money_inventory())

        return PlayerView(player.get_player_idx(), public_player_view, private_view)

    ### Game Logik ###
    def draw_cow_from_stack(self):
        self.current_cow_draw = self._card_stack[0]
        print(f"Bid for COW {self.current_cow_draw}!")
        if len(self._card_stack) == 1:
            print("Last card was drawn.")
            self._is_card_stack_empty = True

        self._card_stack.pop(0)

    def is_card_stack_empty(self) -> bool:
        return self._is_card_stack_empty

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
            if any(self._players[i]._cow_cards.get_cow_inventory()):
                has_cow = True
                break
        return has_cow
    
    def is_any_player_finished(self):
        """Check if a player has no cows and the deck is empty"""
        if self.is_card_stack_empty():
            for pl_idx in self._active_players:
                if not any(self.get_player(pl_idx).get_cow_inventory()):
                    self.remove_active_player(pl_idx)

    # Turn based
    def process_command(self):  # method for future use
        is_command_valid = True
        if is_command_valid:
            pass

    def end_turn(self):
        """Check if players have 4 cows, update the score and change to the next player"""
        for i in range(self.num_players):
            self._players[i].update_score()

        self.is_any_player_finished()
        self.set_current_turn()

        if len(self._active_players) <= 1:
            return

        current_idx_in_active = self._active_players.index(self.get_current_player_idx()) 
        next_in_active = (current_idx_in_active + 1) % len(self._active_players)

        next_pl_idx = self._active_players[next_in_active]

        print(f"Debug: {next_pl_idx}, {self._active_players}")

        self.set_current_player(next_pl_idx)

    # Bid specific
    def handle_bid(self, player_who_gets_cow: int, player_who_gets_money: int, money_amount: list[int]):
        self._players[player_who_gets_cow].add_cow(self.current_cow_draw, 1)
        self._players[player_who_gets_money].add_money(money_amount)
        self._players[player_who_gets_cow].remove_money(money_amount)

    # Trade specific
    def handle_trade(
        self,
        cow_type: int,
        cow_amount: int,
        challenged_player: int,
        money_amount_challenger: list[int],
        money_amount_contender: list[int],
        winner_idx: int,
        looser_idx: int,
    ):
        self._players[winner_idx].add_cow(cow_type, cow_amount)
        self._players[looser_idx].remove_cow(cow_type, cow_amount)

        self._players[challenged_player].add_money(money_amount_challenger)
        self._players[challenged_player].remove_money(money_amount_contender)

        self._players[self.get_current_player_idx()].add_money(money_amount_contender)
        self._players[self.get_current_player_idx()].remove_money(money_amount_challenger)

    def get_possible_cow_trades(self) -> dict[int, list[int]] :
        """Returns a dict with player indices and the joint cows with respect the current player."""
        curr_pl = self._players[self._current_player]
        curr_cows = list(set(curr_pl._cow_cards.get_cow_inventory())) 
        
        ret = {}

        for pl in self._players:
            if pl.get_player_idx() == curr_pl.get_player_idx():
                continue
            cows = list(set(pl._cow_cards.get_cow_inventory()))
            joint_cows = []

            for cow in cows:
                if cow in curr_cows:
                    joint_cows.append(cow)
            if any(joint_cows): 
                ret[pl.get_player_idx()] = joint_cows

        if ret:
            return ret
        else:
            return None


    # Value 
    def get_player_stats(self) -> list[dict[int, list[int]]]:
        stats = []
        for i in range(self.num_players):
            stats.append(
                {
                    "player_idx": self._players[i].get_player_idx(),
                    "money": self._players[i].get_money_inventory(),
                    "cows": self._players[i]._cow_cards.get_cow_inventory(),
                    "score": self._players[i].get_score(),
                }
            )
        return stats
