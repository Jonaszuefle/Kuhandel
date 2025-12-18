from abc import ABC, abstractmethod
from return_types.action import ActionType, Bid, Trade
from return_types.results import Result, ResultType
from typing import Callable, Any


class InputHandler(ABC):
    def __init__(self, player_names: list[str]):
        self.player_names = player_names

    @abstractmethod
    def ask_for_action(self, current_player: int) -> ActionType:
        pass

    @abstractmethod
    def ask_for_bid(self, current_player: int) -> Bid | None:
        pass

    @abstractmethod
    def ask_for_buy_back(self, highest_bid: Bid) -> bool:
        pass

    @abstractmethod
    def get_number_of_players(self) -> int:
        pass


class ConsoleInputHandler(InputHandler):
    def ask_for_action(self, player_idx: int) -> ActionType:
        while True:
            try:
                print(f"\n{self.player_names[player_idx]}! Its your turn!")

                action = input("Choose an action: bid/trade/stats ").strip().lower()

                match action:
                    case "bid" | "b":
                        return ActionType.BID
                    case "trade" | "t":
                        return ActionType.TRADE
                    case "stats" | "s":
                        return ActionType.STATS

            except KeyboardInterrupt:
                raise

    def get_number_of_players(self, player_limit: list[int]):
        while True:
            try:
                num_players = int(
                    input("Input the number of players, between 2 and 4: ")
                )
                if (num_players >= player_limit[0]) and (num_players < player_limit[1]):
                    return num_players
            except KeyboardInterrupt:
                print("Keyboard interrupt!")
                break
            except Exception as e:
                print(f"Wrong input, try again! {e}")

    def ask_for_bid(self, player_idx: int, highest_bid: int) -> Bid:
        bid = self._ask_until_valid(
            f"{self.player_names[player_idx]}, the highest bid is {highest_bid}. Enter your bid or pass (p): ",
            self._parse_bid,
            self._validate_bid,
        )

        if bid:
            return Bid(player_idx, bid)
        else:
            return Bid(player_idx, None)

    def ask_for_buy_back(self, player_idx: int, highest_bid: Bid) -> bool:
        answer = self._ask_until_valid(
            f"{self.player_names[player_idx]}, do you want to buy back the cow for {highest_bid.value}? (y/n): ",
            self._parse_binary_choice,
        )
        return answer

    def ask_for_money_cards(self, highest_bid: Bid, buyer: int) -> list[int]:
        money_cards = self._ask_until_valid(
            f'{self.player_names[buyer]} choose your money cards to pay {highest_bid.value}? Separate with ",": ',
            self._parse_int_list,
            self._validate_money_list,
        )
        return money_cards

    def ask_for_trade(self, joint_cows: dict[int:int]):
        for idx in joint_cows:
            print(f"{self.player_names[idx]} ({idx}) has {joint_cows[idx]}")

        contender = self._ask_until_valid(
            "Choose contender (idx or name): ",
            self._parse_idx_or_name,
            self._validate_player_idx,
        )

        cow_type = self._ask_until_valid(
            "Choose cow type: ", self._parse_int, self._validate_positive_int
        )

        amount = self._ask_until_valid(
            "Choose amount of cows: ", self._parse_int, self._validate_positive_int
        )

        return contender, cow_type, amount

    def ask_for_trade_offer(self, player_idx: int, card_count: int | None) -> Trade:
        if card_count is None:
            msg = f"{self.player_names[player_idx]}, how much do you want to bid? "
        else:
            msg = f"{self.player_names[player_idx]}, {card_count} cards were bidden, what do you want to bid? "

        input = self._ask_until_valid(
            msg, self._parse_int_list, self._validate_money_list
        )

        return Trade(player_idx, input)

    def _ask_until_valid(
        self,
        prompt: str,
        parser: Callable[[str], tuple[Result, Any]],
        validator: Callable[[Any], Result] = None,
        allow_cancel: bool = True,
    ) -> Any:
        """Generic input loop that asks for input until it is valid."""
        while True:
            try:
                raw_input = input(prompt).strip()

                # if allow_cancel and raw_input.lower() in ["cancel", "c", "exit", "e", "quit", "q"]:   # TODO cancel option
                #     return None

                parse_result, parsed_value = parser(raw_input)
                if parse_result.type == ResultType.FAILURE:
                    print(parse_result.message)
                    continue
                if validator:
                    validate_result = validator(parsed_value)
                    if validate_result.type == ResultType.FAILURE:
                        print(validate_result.message)
                        continue

                return parsed_value

            except KeyboardInterrupt:
                raise

    # ----- Parsers -----
    def _parse_int(self, raw: str) -> tuple[Result, int]:
        try:
            return Result(ResultType.SUCCESS), int(raw.strip())
        except Exception as e:
            return Result(ResultType.FAILURE, f"Invalid input. Error {e}"), -1

    def _parse_bid(self, raw: str) -> tuple[Result, int]:
        try:
            if raw.lower() in ["p", "pass"]:
                return Result(ResultType.SUCCESS), None  # TODO player idx
            else:
                parsed = int(raw)
            return Result(ResultType.SUCCESS), parsed  # TODO player idx
        except Exception as e:
            return Result(ResultType.FAILURE, f"Invalid input. Error {e}"), -1

    def _parse_idx_or_name(self, raw: str) -> tuple[Result, int]:
        lower_names = [names.lower() for names in self.player_names]
        try:
            if raw in ["0", "1", "2", "3", "4"]:  # TODO remove hardcode
                return Result(ResultType.SUCCESS), int(raw)
            elif raw.lower() in lower_names:
                return Result(ResultType.SUCCESS), lower_names.index(raw.lower())
            else:
                return Result(ResultType.FAILURE, "Invalid input."), -1
        except Exception as e:
            return Result(ResultType.FAILURE, f"Invalid input. Error {e}"), -1

    def _parse_int_list(self, raw: str) -> tuple[Result, list[int]]:
        try:
            parsed = list(map(int, raw.strip().split(",")))
            return Result(ResultType.SUCCESS), parsed
        except Exception as e:
            return Result(ResultType.FAILURE, f"Invalid input. Error {e}"), []

    def _parse_binary_choice(self, raw: str) -> tuple[Result, bool]:
        try:
            if raw.lower() in ["yes", "y", "1"]:
                return Result(ResultType.SUCCESS), True
            elif raw.lower() in ["no", "n", "0"]:
                return Result(ResultType.SUCCESS), False
            else:
                return Result(ResultType.FAILURE, "Invalid input."), False
        except Exception as e:
            return Result(ResultType.FAILURE, f"Invalid input. Error {e}"), False

    # ----- Validators -----
    def _validate_positive_int(self, value: int) -> Result:
        return (
            Result(ResultType.SUCCESS)
            if value >= 0
            else Result(ResultType.FAILURE, "Value must be positive.")
        )

    def _validate_player_idx(self, idx: int) -> Result:
        if idx < len(self.player_names):
            return Result(ResultType.SUCCESS)
        else:
            return Result(ResultType.FAILURE, f"Player index {idx} is out of range.")

    def _validate_money_list(self, money_list: list[int]) -> Result:
        if len(money_list) != 6:
            return Result(ResultType.FAILURE, "Money list must have 6 values.")
        for val in money_list:
            if val < 0:
                return Result(ResultType.FAILURE, "Money values must be positive.")
        return Result(ResultType.SUCCESS)

    def _validate_bid(self, bid: int) -> Result:
        if bid is None:
            return Result(ResultType.SUCCESS)
        elif bid < 0:
            return Result(ResultType.FAILURE, "Bid must be positive.")
        else:
            return Result(ResultType.SUCCESS)
