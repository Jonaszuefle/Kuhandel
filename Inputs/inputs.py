from abc import ABC, abstractmethod
from Commands.commands import BidCommand, TradeCommand, ShowStatsCommand, Command
from Results.results import Result, ResultType


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
                    case 'bid' | 'b':
                        return BidCommand()
                    case 'trade' | 't':
                        return TradeCommand()
                    case 'stats' | 's':
                        return ShowStatsCommand()
            except KeyboardInterrupt:
                print("Keyboard interrupt!")
                break
            except:
                print("Wrong input, try again!")
            

    def get_number_of_players(self, player_limit: list[int]):
        while True:
            try:
                num_players = int(input("Input the number of players, between 2 and 4: "))
                if (num_players >= player_limit[0]) and (num_players < player_limit[1]):
                        return num_players
            except KeyboardInterrupt:
                print("Keyboard interrupt!")
                break
            except:
                print("Wrong input, try again!")
    
    def get_inputs_for_command(self, command: Command):
        params = {}
        if command.required_params == None:     # catch commands with no required inputs
            return params
        while True:
            try:
                for field in command.required_params:
                    match field:
                        case 'cow_type':
                            params['cow_type'] = int(input('Which cow type? '))
                        case 'cow_amount':
                            params['cow_amount'] = int(input('How many cows? '))
                        case 'player_who_gets_cow':
                            params['player_who_gets_cow'] = int(input('Who gets the cow? '))
                        case 'player_who_gets_money':
                            params['player_who_gets_money'] = int(input('Who gets the money? '))
                        case 'money_amount':
                            params['money_amount'] = list(map(int, input("How much money? Splitted by \',\': ").split(',')))
                return params
            except KeyboardInterrupt:
                print("Keyboard interrupt!")
                break
            # except:
            #     print("Wrong input, try again!")


    def print_player_stats(self, stats: dict[int, list[int]]):
        for i in range(len(stats)):
            print(f"Player {stats[i]['player_idx']} has -- {stats[i]['money']} money -- {stats[i]['cows']} cows -- {stats[i]['score']} score.")
    
