from player.players import Player
from return_types.results import Result, ResultType
from return_types.action import Bid

class BidHandler:
    """Manages the auction round"""
    def __init__(self, bid_master: int, num_players: int) -> None:
        self.bid_master = bid_master
        self.num_players = num_players
        self.bids: list[Bid] = []
        self.remaining_players: list[int] = [idx%num_players for idx in range(bid_master + 1, bid_master + num_players)]

    def place_bid(self, player: Player, value: int) -> Result:
        """Place a bid. Returns Result"""   
        if value <= self.get_highest_bid():
            return Result(ResultType.FAILURE, "Bid is too low.")
        elif player.get_money_value() < value:
            return Result(ResultType.FAILURE, "Player has not enough money.")
        
        self.bids.append(Bid(player.get_player_idx(), value))
        return Result(ResultType.SUCCESS)

    def get_highest_bid(self) -> int:
        """Return the highest bid"""
        if not self.bids:
            return 0
        else:
            return max(b.value for b in self.bids)
        
    def pass_bid(self, player_idx: int):
        self.remaining_players.remove(player_idx)

    def get_winner_bid(self) -> Bid:
        if not self.bids:
            return Bid(self.bid_master, 0)
        return max(self.bids, key=lambda b: b.value)
    
    def is_complete(self) -> bool:
        return len(self.remaining_players) <= 1
        
