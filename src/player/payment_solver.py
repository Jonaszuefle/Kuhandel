from game_config.game_config import GameConfig


class MoneyPay:     # TODO add cost function -> tradeoff amount of money cards vs overpay
    def optimal_pay(
        self, target_value: int, money_cards_amount: list[int]
    ) -> list[int]:
        """Recursive solver for finding the best minimal payment for a given target_value"""
        self.best_solution = []
        self.min_overpay = float("inf")

        money_cards_list = self.amount_to_list(money_cards_amount)

        total_money = sum(money_cards_list)
        if (
            total_money < target_value
        ):  # This should not be possible, as payment is checked during bidding
            return None

        self._find_subset(money_cards_list, target_value, 0, [])

        return self.list_to_amount(self.best_solution)

    def _find_subset(self, cards, target, current_idx, current_selection):
        """Checks the current selected path and adds or skipps the next card"""
        current_sum = sum(current_selection)
        if current_sum >= target:
            overpay = current_sum - target

            if overpay < self.min_overpay:
                self.min_overpay = overpay
                self.best_solution = current_selection.copy()
            elif overpay == self.min_overpay:
                if len(current_selection) < len(self.best_solution):
                    self.best_solution = current_selection.copy()

            return  # node is finished

        if current_idx >= len(cards):
            return

        # Add the current card
        current_card = cards[current_idx]
        current_selection.append(current_card)
        self._find_subset(cards, target, current_idx + 1, current_selection)

        # Do not add the card
        current_selection.pop()
        self._find_subset(cards, target, current_idx + 1, current_selection)

    def list_to_amount(self, money_list: list[int]) -> list[int]:
        """List of sorted money, from highest to lowest. Returns money amounts [0s, 10s, 50s, ...]"""
        money_amount = []
        for money_val in GameConfig.MONEY_CARD_VALUES:
            money_amount.append(money_list.count(money_val))
        return money_amount

    def amount_to_list(self, money_amount: list[int]) -> list[int]:
        """Takes the money amounts and lists them from highest to lowest value"""
        res = []
        for i in range(len(money_amount)):
            for _ in range(money_amount[i]):
                res.append(GameConfig.MONEY_CARD_VALUES[i])

        return list(reversed(res))
