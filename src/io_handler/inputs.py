from abc import ABC, abstractmethod
from return_types.action import ActionType, Bid, Trade


class InputHandler(ABC):
    def __init__(self, player_names: dict[int:str]):
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

                action = input(f"Choose an action: bid/trade/stats ").strip().lower()

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
            except:
                print("Wrong input, try again!")

    def ask_for_bid(self, player_idx: int, highest_bid: int) -> Bid | None:
        while True:
            raw_input = (
                input(
                    f"{self.player_names[player_idx]} bid higher than {highest_bid} or pass (p): "
                )
                .strip()
                .lower()
            )

            if raw_input in ["p", "pass"]:
                return Bid(player_idx, None)
            try:
                parsed_input = int(raw_input)  # TODO write parser

                # if not spec.validator(parsed_input):      # TODO validator
                #         print("Wrong input format!")
                #         continue

                return Bid(player_idx, parsed_input)

            except ValueError as e:
                print(f"Wrong format.")
                continue
            except KeyboardInterrupt:
                raise

    def ask_for_buy_back(self, player_idx: int, highest_bid: Bid) -> bool:
        while True:
            try:
                raw_input = (
                    input(
                        f"{self.player_names[player_idx]} do you want to take the buy-back action from {self.player_names[highest_bid.player_idx]} of {highest_bid.value}? y/n: "
                    )
                    .strip()
                    .lower()
                )
                if raw_input in ["yes", "y"]:
                    return True
                elif raw_input in ["no", "n"]:
                    return False
                else:
                    continue

            except Exception as e:
                print("Error {e}")
                continue
            except KeyboardInterrupt:
                break

    def ask_for_money_cards(self, highest_bid: Bid, buyer: int) -> list[int]:
        while True:
            try:
                raw_input = (
                    input(
                        f'{self.player_names[buyer]} choose your money cards to pay {highest_bid.value}? Separate with ",": '
                    )
                    .strip()
                    .split(",")
                )

                parsed = list(map(int, raw_input))

                return parsed

            except Exception as e:
                print("Error {e}")
                continue
            except KeyboardInterrupt:
                break

    def ask_for_trade(self, joint_cows: dict[int:int]):
        for idx in joint_cows:
            print(f"{self.player_names[idx]} has {joint_cows[idx]}")

        while True:
            try:
                raw_contender = input(f"Choose contender: ")

                parsed_contender = int(raw_contender)

                raw_cow = input("Choose cow type: ")

                parsed_cow = int(raw_cow)

                raw_amount = input("Choose amount of cows: ")

                parsed_amount = int(raw_amount)

                return parsed_contender, parsed_cow, parsed_amount

            except Exception as e:
                print("Error {e}")
                continue
            except KeyboardInterrupt:
                break

    def ask_for_trade_offer(self, player_idx: int, card_count: int) -> Trade:
        if card_count is None:
            msg = f"{self.player_names[player_idx]}, how much do you want to bid? "
        else:
            msg = f"{self.player_names[player_idx]}, {card_count} cards were bidden, what do you want to bid? "

        while True:
            try:
                raw_input = input(msg).strip().split(",")

                parsed_input = list(map(int, raw_input))

                return Trade(player_idx, parsed_input)

            # except Exception as e:
            #     print("Error {e}")
            #     continue
            except KeyboardInterrupt:
                break

    # Outputs
    def print_donkey(self):
        print("It's a donkey! Inflation time.")
