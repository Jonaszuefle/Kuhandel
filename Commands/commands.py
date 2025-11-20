from abc import ABC, abstractmethod
from Results.results import Result, ResultType
from enum import Enum
from Game.game import Game

# class CommandType(Enum):
#      TRADE = 0,
#      BID = 1,
#      SHOWSTATS = 2

class Command(ABC):
     @abstractmethod
     def execute(self):
         pass
    
     @abstractmethod
     def fill(self):
         pass

     def validate_command_values(self):
          pass
         
class TradeCommand(Command):
     required_params = ['cow_type', 'cow_amount', 'player_who_gets_cow', 'player_who_gets_money', 'money_amount']

     def fill(self, param_dict: dict[int, list[int]]):
          self.param_dict = param_dict

     def validate_command_values(self, game: Game) -> Result:
          if not game.players[self.param_dict['player_who_gets_cow']].has_enough_money(self.param_dict['money_amount']):
               return Result(ResultType.FAILURE, f"Player has not enough money")
          elif not game.players[self.param_dict['player_who_gets_money']].has_cow(self.param_dict['cow_type'], self.param_dict['cow_amount']):
               return Result(ResultType.FAILURE, f"Player has not enough cow")
          else:
               return Result(ResultType.SUCCESS)

     def execute(self, game):
          game.handle_trade(**self.param_dict)

class BidCommand(Command):
     required_params = ['player_who_gets_cow', 'player_who_gets_money', 'money_amount']

     def fill(self, param_dict: dict[int, list[int]]):
          self.param_dict = param_dict

     def execute(self, game: Game) -> Result:
          game.handle_bid(**self.param_dict)
     
     def validate_command_values(self, game: Game) -> Result:
          if game.players[self.param_dict['player_who_gets_cow']].has_enough_money(self.param_dict['money_amount']):
               return Result(ResultType.SUCCESS)
          else:
               return Result(ResultType.FAILURE, f"Player {self.param_dict['player_who_gets_cow']} has not enough money!")
     
class ShowStatsCommand(Command):
     required_params = None

     def execute(self, game):
          pass

     def validate_command_values(self, game:Game) -> Result:
          return Result(ResultType.SUCCESS)
     
     def fill(self, params: dict[int, list[int]]):
         pass