from abc import ABC, abstractmethod
from commands.commands import BidCommand, TradeCommand, ShowStatsCommand, Command


class InputHandler(ABC):
    @abstractmethod
    def get_command(self, current_player: int) -> Command:
        pass

    @abstractmethod
    def get_inputs_for_command(self, command: Command):
        pass

    def check_input_format(self):
        pass

    @abstractmethod
    def get_number_of_players(self) -> int:
        pass


class ConsoleInputHandler(InputHandler):
    def get_command(self, current_player: int) -> Command:
        while True:
            try:
                print(f"Player {current_player}! Its your turn!")

                action = input(f"Choose an action: bid/trade/stats ").strip().lower()

                match action:
                    case "bid" | "b":
                        return BidCommand()
                    case "trade" | "t":
                        return TradeCommand()
                    case "stats" | "s":
                        return ShowStatsCommand()
            except KeyboardInterrupt:
                print("Keyboard interrupt!")
                break
            except:
                print("Wrong input, try again!")

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

    def get_inputs_for_command(self, command: Command):
        params = {}
        if command.input_specs == None:  # catch commands with no required inputs
            return None
        for spec in command.input_specs:

            while True:
                try:
                    raw_input = input(spec.prompt).strip()

                    if raw_input.strip().lower() in ["q", "quit"]:  # exit loop at user request
                        params['quit'] = True
                        return params
                    
                    try:
                        parsed_input = spec.parser(raw_input)
                    except ValueError as e:
                        print(f"Wrong format.")
                        continue

                    if not spec.validator(parsed_input):
                        print("Wrong input format!")
                        continue

                    params[spec.name] = parsed_input

                    break

                except KeyboardInterrupt:
                    print("Keyboard interrupt!")
                    break

        return params

            
            # except:
            #     print("Wrong input, try again!")

    def print_donkey(self):
        print("It's a donkey! Inflation time.")
