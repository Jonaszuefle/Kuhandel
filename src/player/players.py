from game_config.game_config import GameConfig


class Player:
    def __init__(self, player_idx):
        self.__player_idx = player_idx
        self.__player_name = None  # optional -> future

        self.money_cards_obj = MoneyCards()
        self.cow_cards_obj = CowCards()
        self.__score = 0

    # Player stuff
    def get_player_idx(self):
        return self.__player_idx

    def get_player_name(self):
        return self.__player_name

    # Money stuff
    def get_money_value(self):
        return self.money_cards_obj.return_money_value()

    def has_enough_money(self, sub_money_list):
        return self.money_cards_obj.has_enough_money(sub_money_list)

    def add_money(self, add_money_list):
        self.money_cards_obj.add_money(add_money_list)

    def remove_money(self, sub_money_list):
        self.money_cards_obj.remove_money(sub_money_list)

    # Cow stuff
    def has_cow(self, cow_card, cow_card_amount):
        has_cow = self.cow_cards_obj.has_cow(cow_card, cow_card_amount)
        return has_cow

    def add_cow(self, cow_card, cow_card_amount):
        self.cow_cards_obj.add_cow_to_inventory(cow_card, cow_card_amount)

    def remove_cow(self, cow_card, cow_card_amount):
        self.cow_cards_obj.remove_cows(cow_card, cow_card_amount)

    # Score stuff
    def update_score(self):
        self.cow_cards_obj.check_for_four_cows()
        self.__score = (
            sum(self.cow_cards_obj.cow_finished)
            * 4
            * len(self.cow_cards_obj.cow_finished)
        )

    def get_score(self):
        return self.__score


class MoneyCards:
    def __init__(self):
        self.__money_inventory = (
            GameConfig.STARTING_MONEY
        )  # amount of 0, 10, 50, 100, 200, 500

    def get_money_inventory(self):
        return self.__money_inventory

    def add_money(self, money_list: list[int]):
        self.__money_inventory = [
            x + y for x, y in zip(self.__money_inventory, money_list)
        ]

    def has_enough_money(self, money_list: list[int]):
        new_amount_money = [x - y for x, y in zip(self.__money_inventory, money_list)]
        negative_money_idx = []
        for i in range(len(money_list)):
            if new_amount_money[i] < 0:
                negative_money_idx.append(i)

        if any(negative_money_idx):
            return False
        else:
            return True

    def remove_money(self, money_list):
        new_amount_money = [x - y for x, y in zip(self.__money_inventory, money_list)]
        self.__money_inventory = new_amount_money

    def return_money_value(self):
        return sum(
            [
                a * b
                for a, b in zip(self.__money_inventory, GameConfig.MONEY_CARD_VALUES)
            ]
        )


class CowCards:
    def __init__(self):
        self.__cow_inventory = []  # list of current cows (unsorted)
        self.cow_finished = []

    def get_cow_inventory(self):
        return self.__cow_inventory

    def add_cow_to_inventory(self, cow_card, cow_card_amount):
        for i in range(cow_card_amount):
            self.__cow_inventory.append(cow_card)

    def has_cow(self, cow_card: int, cow_card_amount: int):
        if self.__cow_inventory.count(cow_card) == cow_card_amount:
            return True
        else:
            return False

    def remove_cows(self, cow_card, cow_card_amount):
        for i in range(cow_card_amount):
            self.__cow_inventory.remove(cow_card)

    def check_for_four_cows(self):
        diff_cow_cards = list(set(self.__cow_inventory))
        for i in range(len(diff_cow_cards)):
            if self.has_cow(diff_cow_cards[i], 4):
                self.remove_cows(diff_cow_cards[i], 4)
                self.cow_finished.append(diff_cow_cards[i])
