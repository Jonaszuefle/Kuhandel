from game_config.game_config import GameConfig
from player.payment_solver import MoneyPay


class Player:
    def __init__(self, player_idx):
        self.__player_idx = player_idx
        self.__player_name = None  # optional -> future

        self._money_cards = MoneyCards()
        self._cow_cards = CowCards()
        self._score = 0

        if GameConfig.AUTOMATIC_MONEY_CARD_CHOICE:
            self.pay_solver = MoneyPay()

    # Player stuff
    def get_player_idx(self):
        return self.__player_idx

    def get_player_name(self):
        return self.__player_name

    # Money stuff
    def get_money_value(self):
        return self._money_cards.return_money_value()

    def has_enough_money(self, sub_money_list):
        return self._money_cards.has_enough_money(sub_money_list)

    def add_money(self, add_money_list):
        self._money_cards.add_money(add_money_list)

    def remove_money(self, sub_money_list):
        self._money_cards.remove_money(sub_money_list)

    def get_money_inventory(self) -> list[int]:
        return self._money_cards._money_inventory

    def get_optimal_payment(self, target_value) -> list[int]:
        """From a given target value, get the optimal amount of money cards"""
        return self.pay_solver.optimal_pay(target_value, self.get_money_inventory())

    def get_money_cards_count(self):
        """Returns the number of total cards in the players hand"""
        return sum(self._money_cards._money_inventory)

    # Cow stuff
    def has_cow(self, cow_card, cow_card_amount):
        has_cow = self._cow_cards.has_cow(cow_card, cow_card_amount)
        return has_cow

    def add_cow(self, cow_card, cow_card_amount):
        self._cow_cards.add_cow_to_inventory(cow_card, cow_card_amount)

    def remove_cow(self, cow_card, cow_card_amount):
        self._cow_cards.remove_cows(cow_card, cow_card_amount)

    def get_cow_inventory(self) -> list[int]:
        return self._cow_cards._cow_inventory

    # Score stuff
    def update_score(self):
        self._cow_cards.check_for_four_cows()
        self._score = (
            sum(self._cow_cards.cow_finished) * 4 * len(self._cow_cards.cow_finished)
        )

    def get_score(self):
        return self._score


class MoneyCards:
    def __init__(self):
        self._money_inventory = (
            GameConfig.STARTING_MONEY
        )  # amount of 0, 10, 50, 100, 200, 500

    def get_money_inventory(self):
        return self._money_inventory

    def add_money(self, money_list: list[int]):
        self._money_inventory = [
            x + y for x, y in zip(self._money_inventory, money_list)
        ]

    def has_enough_money(self, money_list: list[int]) -> bool:
        """Checks if the player has enough money"""
        new_amount_money = [x - y for x, y in zip(self._money_inventory, money_list)]
        negative_money_idx = []
        for i in range(len(money_list)):
            if new_amount_money[i] < 0:
                negative_money_idx.append(i)

        if any(negative_money_idx):
            return False
        else:
            return True

    def remove_money(self, money_list):
        """Removes the money from the players inventory"""
        new_amount_money = [x - y for x, y in zip(self._money_inventory, money_list)]
        self._money_inventory = new_amount_money

    def return_money_value(self):
        """Returns the total Fvalue of the players money cards"""
        return sum(
            [a * b for a, b in zip(self._money_inventory, GameConfig.MONEY_CARD_VALUES)]
        )


class CowCards:
    def __init__(self):
        self._cow_inventory = []  # list of current cows (unsorted)
        self.cow_finished = []

    def get_cow_inventory(self):
        return self._cow_inventory

    def add_cow_to_inventory(self, cow_card, cow_card_amount):
        for i in range(cow_card_amount):
            self._cow_inventory.append(cow_card)

    def has_cow(self, cow_card: int, cow_card_amount: int):
        if self._cow_inventory.count(cow_card) >= cow_card_amount:
            return True
        else:
            return False

    def remove_cows(self, cow_card, cow_card_amount):
        for i in range(cow_card_amount):
            self._cow_inventory.remove(cow_card)

    def check_for_four_cows(self):
        diff_cow_cards = list(set(self._cow_inventory))
        for i in range(len(diff_cow_cards)):
            if self.has_cow(diff_cow_cards[i], 4):
                self.remove_cows(diff_cow_cards[i], 4)
                self.cow_finished.append(diff_cow_cards[i])
