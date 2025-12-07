import pytest
from unittest.mock import Mock
from game.game import Game, CardStack
from player.players import Player
from action_handlers.bidding import BidHandler
from application.play_auction import PlayBidTurn
from return_types.action import Bid
from return_types.results import Result, ResultType
from game_config.game_config import GameConfig


@pytest.fixture
def game_3_players():
    """Create a game with 3 players for testing."""
    GameConfig.AUTOMATIC_MONEY_CARD_CHOICE = True
    GameConfig.STARTING_MONEY_CARDS = [0, 3, 2, 0, 0, 0]  # 120
    GameConfig.DONKEY_COW = 20

    game = Game(3, ["Alice", "Bob", "Charlie"])
    game.start_game()
    game.set_current_player(0)
    game.card_stack._card_stack = ([10, 20, 30, 40, 50])  # Simplified stack for testing
    return game


@pytest.fixture
def game_2_players():
    """Create a game with 2 players."""
    game = Game(2, ["Alice", "Bob"])
    game.start_game()
    game.set_current_player(0)
    game.card_stack._card_stack = ([10, 20, 30, 40, 50]) 
    return game


class TestBidding:
    """Integration tests for bidding logic."""

    def test_place_bid_success(self, game_3_players):
        """Test placing a bid successfully."""
        game = game_3_players
        bid_handler = BidHandler(0, 3)
        
        player = game.get_player(1)
        initial_money = player.get_money_value()
        
        # Place a valid bid
        result = bid_handler.place_bid(player, 100)
        
        assert result.type == ResultType.SUCCESS
        assert bid_handler.get_highest_bid() == 100
        assert len(bid_handler.bids) == 1
        assert bid_handler.bids[0].value == 100
        # Money should not be deducted yet (only tracked)
        assert player.get_money_value() == initial_money

    def test_place_bid_insufficient_funds(self, game_3_players):
        """Test placing a bid with insufficient funds."""
        game = game_3_players
        bid_handler = BidHandler(0, 3)
        
        player = game.get_player(1)
        player_money = player.get_money_value()
        
        # Try to bid more than player has
        result = bid_handler.place_bid(player, player_money + 1000)
        
        assert result.type == ResultType.FAILURE
        assert "not enough money" in result.message.lower()
        assert bid_handler.get_highest_bid() == 0  # No bid placed

    def test_place_bid_too_low(self, game_3_players):
        """Test placing a bid lower than current highest."""
        game = game_3_players
        bid_handler = BidHandler(0, 3)
        
        player1 = game.get_player(1)
        player2 = game.get_player(2)
        
        # First bid: 100
        bid_handler.place_bid(player1, 100)
        
        # Second bid: 50 (too low)
        result = bid_handler.place_bid(player2, 50)
        
        assert result.type == ResultType.FAILURE
        assert "too low" in result.message.lower()
        assert bid_handler.get_highest_bid() == 100

    def test_get_highest_bid(self, game_3_players):
        """Test retrieving the highest bid."""
        game = game_3_players
        bid_handler = BidHandler(0, 3)
        
        assert bid_handler.get_highest_bid() == 0  # No bids yet
        
        bid_handler.bids.append(Bid(0, 100))
        bid_handler.bids.append(Bid(1, 200))
        bid_handler.bids.append(Bid(2, 150))
        
        assert bid_handler.get_highest_bid() == 200

    def test_get_winner_bid(self, game_3_players):
        """Test retrieving the winner of the auction."""
        game = game_3_players
        bid_handler = BidHandler(0, 3)
        
        bid_handler.bids.append(Bid(1, 100))
        bid_handler.bids.append(Bid(2, 250))
        bid_handler.bids.append(Bid(0, 150))
        
        winner = bid_handler.get_winner_bid()
        
        assert winner.player_idx == 2
        assert winner.value == 250

    def test_auction_complete_when_one_player_remains(self, game_3_players):
        """Test that auction completes when only one player remains."""
        game = game_3_players
        bid_handler = BidHandler(0, 3)
        
        assert not bid_handler.is_complete()
        
        # Two players pass
        bid_handler.pass_bid(1)
        bid_handler.pass_bid(2)
        
        assert bid_handler.is_complete()

    def test_money_transfer_after_bid(self, game_3_players):
        """Test that money is correctly transferred after a bid is completed."""
        game = game_3_players
        
        buyer_idx = 1
        seller_idx = 0
        cow_type = 10
        bid_amount = [0, 2, 0, 0, 0, 0]  # 2 cards of value 10 = 20 total
        
        buyer_initial_money = game.get_player(buyer_idx).get_money_inventory().copy()
        seller_initial_money = game.get_player(seller_idx).get_money_inventory().copy()
        
        # Execute bid
        game.handle_bid(cow_type, buyer_idx, seller_idx, bid_amount)
        
        buyer_after = game.get_player(buyer_idx).get_money_inventory()
        seller_after = game.get_player(seller_idx).get_money_inventory()
        
        # Buyer should have less money
        assert buyer_after[1] == buyer_initial_money[1] - 2
        # Seller should have more money
        assert seller_after[1] == seller_initial_money[1] + 2
        # Buyer should have the cow
        assert cow_type in game.get_player(buyer_idx).get_cow_inventory()

    def test_buy_back_action(self, game_3_players):
        """Test buy-back action in bidding."""
        game = game_3_players
        
        # Simulate: bid_master (player 0) loses auction but wants to buy back
        bid_master = 0
        buyer = 1
        cow_type = 10
        bid_amount = [0, 2, 0, 0, 0, 0]
        
        buyer_initial_cows = len(game.get_player(buyer).get_cow_inventory())
        bid_master_initial_cows = len(game.get_player(bid_master).get_cow_inventory())
        
        # With buy-back: roles reversed
        game.handle_bid(cow_type, bid_master, buyer, bid_amount)
        
        # bid_master should have the cow
        assert len(game.get_player(bid_master).get_cow_inventory()) == bid_master_initial_cows + 1
        assert cow_type in game.get_player(bid_master).get_cow_inventory()


class TestScoring:
    """Integration tests for scoring logic."""

    def test_score_update_with_four_cows(self, game_3_players):
        """Test score update when a player has 4 of the same cow."""
        game = game_3_players
        player = game.get_player(0)
        
        # Manually add 4 cows of type 10
        for _ in range(4):
            player.add_cow(10, 1)
        
        initial_score = player.get_score()
        player.update_score()
        
        # Score should be: (count of finished sets) * 4 * (type value)
        assert player.get_score() == 40
        # Cows should be removed
        assert 10 not in player.get_cow_inventory()

    def test_score_with_multiple_sets(self, game_3_players):
        """Test score when player completes multiple sets of 4 cows."""
        game = game_3_players
        player = game.get_player(0)
        
        # Add 4 cows of type 10 and 4 cows of type 20
        for _ in range(4):
            player.add_cow(10, 1)
            player.add_cow(20, 1)
        
        player.update_score()
        
        # Score: 2 sets → 2 * 4 * (10 + 20) = 240
        assert player.get_score() == 240
        assert 10 not in player.get_cow_inventory()
        assert 20 not in player.get_cow_inventory()

    def test_partial_cows_no_score(self, game_3_players):
        """Test that incomplete cow sets don't contribute to score."""
        game = game_3_players
        player = game.get_player(0)
        
        # Add only 3 cows (not enough for a set)
        for _ in range(3):
            player.add_cow(10, 1)
        
        player.update_score()
        
        assert player.get_score() == 0
        assert 10 in player.get_cow_inventory()  # Cows remain


class TestGameFlow:
    """End-to-end game flow tests."""

    def test_bid_flow_end_to_end(self, game_3_players):
        """Test complete bidding flow: draw card → bids → money transfer → score check."""
        game = game_3_players

        assert game.get_current_player_idx() == 0

        #game._players[0]._money_cards._money_inventory = [0, 0, 2, 0, 0, 0]  # 50

        def make_player_interface_mock(idx, bid_value = None, buy_back = False):
            m = Mock()
            m.make_bid_decision.return_value = Bid(idx, bid_value) 
            m.make_buy_back_decision.return_value = buy_back
            return m

        p0 = make_player_interface_mock(0, bid_value=None, buy_back=True)  # passes
        p1 = make_player_interface_mock(1, bid_value=10)  # wins
        p2 = make_player_interface_mock(2, bid_value=40)  # insufficient funds
        player_interfaces = [p0, p1, p2]

        output = Mock()
        play_bid_turn = PlayBidTurn(player_interfaces, output, game)
        
        # prechecks before bidding
        buyer_idx = 0
        seller_idx = 2
        buyer_initial_money = game.get_player(buyer_idx).get_money_inventory()
        seller_initial_money = game.get_player(seller_idx).get_money_inventory()
        buyer_initial_cows = game.get_player(buyer_idx).get_cow_inventory()


        #GameConfig.AUTOMATIC_MONEY_CARD_CHOICE = False

        res = play_bid_turn.execute()

        assert res.type == ResultType.SUCCESS
        assert game.get_player(buyer_idx).get_optimal_payment(40) == [0,0,1,0,0,0]  # overpay as starting money is too low
        assert game.get_player(buyer_idx).get_cow_inventory() == [10]
        assert 10 not in game.get_player(seller_idx).get_cow_inventory()
        assert game.get_player(buyer_idx).get_money_value() < game.get_player(seller_idx).get_money_value()
        assert game.get_player(seller_idx).get_money_value() == game.get_money_value(seller_initial_money) + 50

        assert game.get_current_player_idx() == 1  # test end turn