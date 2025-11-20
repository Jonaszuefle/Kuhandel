import random
from Player.players import Player

from GameConfig.gameConfig import GameConfig

class Game():
    __money_inflation_stage = 2
    __player_limit = [2,5]      # for optional input
    game_is_ongoing = True

    def start_game(self):
        self.__card_stack = self.get_random_starting_stack(GameConfig.COW_CARD_VALUES)
        self.__is_card_stack_empty = False    

        self.num_players = 3
        self.players = self.get_list_of_players()
        self.current_player = self.get_random_starting_player()

    def get_list_of_players(self) -> list[Player]:
        players = []
        for i in range(self.num_players):
            players.append(Player(i))
        return players
    
    def get_random_starting_player(self) -> int:
        return random.randint(0, self.num_players-1)


    def get_random_starting_stack(self, cow_cards: list[int]) -> list[int]:
        card_stack = []
        for i in range(len(cow_cards)):
            for j in range(4):
                card_stack.append(cow_cards[i])
        random_cow_cards = random.sample(card_stack, len(card_stack))

        return random_cow_cards

    ### Game Logik ###

    def draw_cow_from_stack(self):
        self.current_cow_draw = self.__card_stack[0]
        print(f"Bid for COW {self.current_cow_draw}!")
        if len(self.__card_stack) == 1:
            print("Last card was drawn.")
            self.__is_card_stack_empty = True
        
        self.__card_stack.pop(0)

    def is_donkey_cow(self):    # increase inflation
        if self.current_cow_draw == GameConfig.DONKEY_COW:
            self.inflate_player_money()

    def is_game_over(self):
        if self.__is_card_stack_empty and not self.have_players_cows():
            self.game_is_ongoing = False
            
            scores = []
            for i in range(self.num_players):
                scores.append(self.players[i].get_score())
            print(f"Game OVER -- Scores: {scores}")

    def have_players_cows(self):
        has_cow = False
        for i in range(self.num_players):
            if any(self.players[i].cow_cards_obj.get_cow_inventory()):
                has_cow = True
                break
        return has_cow
        
    def inflate_player_money(self):
        money = [0,0,0,0,0,0]
        money[self.__money_inflation_stage] = 1
        for player in self.players:
            player.add_money(money)
        self.__money_inflation_stage += 1

    # Turn based

    def process_command(self):      # method for future use
        is_command_valid = True
        if is_command_valid:
            pass

    def end_turn(self):
        for i in range(self.num_players):
            self.players[i].update_score()

        self.current_player += 1
        if self.current_player >= self.num_players:
            self.current_player = 0

    def handle_bid(self, player_who_gets_cow, player_who_gets_money, money_amount):
        
        self.players[player_who_gets_cow].add_cow(self.current_cow_draw, 1)
        self.players[player_who_gets_money].add_money(money_amount)
        self.players[player_who_gets_cow].remove_money(money_amount)

    def handle_trade(self, cow_type: int, cow_amount: int, player_who_gets_cow: int, player_who_gets_money: int, money_amount: list[int]):

        self.players[player_who_gets_cow].add_cow(cow_type, cow_amount)
        self.players[player_who_gets_money].remove_cow(cow_type, cow_amount)
        self.players[player_who_gets_money].add_money(money_amount)
        self.players[player_who_gets_cow].remove_money(money_amount)

    # score

    def get_player_stats(self) -> list[dict[int, list[int]]]:
        stats = []
        for i in range(self.num_players):
            stats.append({'player_idx': self.players[i].get_player_idx(),
                          'money': self.players[i].money_cards_obj.get_money_inventory(),
                          'cows': self.players[i].cow_cards_obj.get_cow_inventory(),
                          'score': self.players[i].get_score()}) 
        return stats