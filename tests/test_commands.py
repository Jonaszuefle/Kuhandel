"""Unit tests for command pattern using unittest.

Tests the command lifecycle: prepare -> fill -> validate -> execute
"""

import unittest
from unittest.mock import Mock

from commands.commands import BidCommand, TradeCommand, ShowStatsCommand, CommandState
from results.results import Result, ResultType
from game_config.game_config import GameConfig

class TestBidCommand(unittest.TestCase):
    """Tests for BidCommand lifecycle."""

    def test_prepare_draws_card_successfully(self):
        """Test that prepare phase draws a card."""
        # Arrange
        game = Mock()
        game.draw_cow_from_stack.return_value = (
            None  # Dein BidCommand gibt nichts zurück
        )
        game.current_cow_draw = 10  # Karte wird als Attribut gesetzt

        command = BidCommand()

        # Act
        result = command.prepare(game)

        # Assert
        self.assertEqual(result.type, ResultType.SUCCESS)
        self.assertEqual(command.command_state, CommandState.PREPARED)
        game.draw_cow_from_stack.assert_called_once()

    def test_fill_stores_parameters(self):
        """Test that fill phase stores parameters correctly."""
        # Arrange
        command = BidCommand()
        params = {
            "player_who_gets_cow": 0,
            "player_who_gets_money": 1,
            "money_amount": [0, 1, 0, 0, 0, 0],
        }

        # Act
        command.fill(params)

        # Assert
        self.assertEqual(command.param_dict, params)
        self.assertEqual(command.command_state, CommandState.FILLED)

    def test_validate_succeeds_when_player_has_money(self):
        """Test validation succeeds when player can afford bid."""
        # Arrange
        game = Mock()
        player = Mock()
        player.has_enough_money.return_value = True
        game._players = [player, Mock()]

        command = BidCommand()
        command.param_dict = {
            "player_who_gets_cow": 0,
            "player_who_gets_money": 1,
            "money_amount": [0, 1, 0, 0, 0, 0],
        }

        # Act
        result = command.validate_command_values(game)

        # Assert
        self.assertEqual(result.type, ResultType.SUCCESS)
        player.has_enough_money.assert_called_once_with([0, 1, 0, 0, 0, 0])

    def test_validate_fails_when_player_lacks_money(self):
        """Test validation fails when player can't afford bid."""
        # Arrange
        game = Mock()
        player = Mock()
        player.has_enough_money.return_value = False
        game._players = [player, Mock()]

        command = BidCommand()
        command.param_dict = {
            "player_who_gets_cow": 0,
            "player_who_gets_money": 1,
            "money_amount": [0, 0, 5, 0, 0, 0],
        }

        # Act
        result = command.validate_command_values(game)

        # Assert
        self.assertEqual(result.type, ResultType.FAILURE)
        #self.assertIn("money", result.message.lower())

    def test_execute_calls_game_handle_bid(self):
        """Test execute phase calls game's handle_bid method."""
        # Arrange
        game = Mock()
        command = BidCommand()
        command.param_dict = {
            "player_who_gets_cow": 0,
            "player_who_gets_money": 1,
            "money_amount": [0, 1, 0, 0, 0, 0],
        }

        # Act
        command.execute(game)

        # Assert
        self.assertEqual(command.command_state, CommandState.EXECUTED)
        game.handle_bid.assert_called_once_with(
            player_who_gets_cow=0,
            player_who_gets_money=1,
            money_amount=[0, 1, 0, 0, 0, 0],
        )
        game.end_turn.assert_called_once()


class TestTradeCommand(unittest.TestCase):
    """Tests for TradeCommand lifecycle."""

    def test_prepare_does_nothing(self):
        """Test that trade command's prepare phase is a no-op."""
        # Arrange
        game = Mock()
        command = TradeCommand()

        # Act
        result = command.prepare(game)

        # Assert
        self.assertEqual(result.type, ResultType.SUCCESS)
        self.assertEqual(command.command_state, CommandState.PREPARED)

    def test_validate_checks_both_players(self):
        """Test validation checks both current_player and challenged_player resources."""
        # Arrange
        game = Mock()
        game.get_current_player_idx.return_value = 0
        current_player = Mock()
        current_player.has_cow.return_value = True
        current_player.has_enough_money.return_value = True
        challenged_player = Mock()
        challenged_player.has_cow.return_value = True
        challenged_player.has_enough_money.return_value = True
        game._players = [current_player, challenged_player, Mock]

        command = TradeCommand()
        command.param_dict = {
            "cow_type": 10,
            "cow_amount": 1,
            "challenged_player": 1,
            "money_amount_current": [0, 1, 0, 0, 0, 0],
            "money_amount_challenged": [0, 1, 0, 0, 0, 0],
        }

        # Act
        result = command.validate_command_values(game)

        # Assert
        self.assertEqual(result.type, ResultType.SUCCESS)
        current_player.has_enough_money.assert_called_once()
        current_player.has_cow.assert_called_once_with(10, 1)
        challenged_player.has_enough_money.assert_called_once()
        challenged_player.has_cow.assert_called_once_with(10, 1)
        game.get_current_player_idx.assert_called_once()

    def test_validate_checks_both_players_fail_cow(self):
        """Test validation checks both current_player and challenged_player resources."""
        # Arrange
        game = Mock()
        game.get_current_player_idx.return_value = 0
        current_player = Mock()
        current_player.has_cow.return_value = False
        current_player.has_enough_money.return_value = True
        challenged_player = Mock()
        challenged_player.has_cow.return_value = True
        challenged_player.has_enough_money.return_value = False
        game._players = [current_player, challenged_player, Mock]

        command = TradeCommand()
        command.param_dict = {
            "cow_type": 10,
            "cow_amount": 1,
            "challenged_player": 1,
            "money_amount_current": [0, 1, 0, 0, 0, 0],
            "money_amount_challenged": [0, 1, 0, 0, 0, 0],
        }

        # Act
        result = command.validate_command_values(game)

        # Assert
        self.assertEqual(result.type, ResultType.FAILURE)
        current_player.has_enough_money.assert_called_once()
        current_player.has_cow.assert_called_once_with(10, 1)
        challenged_player.has_enough_money.assert_called_once()
        challenged_player.has_cow.assert_called_once_with(10, 1)
        game.get_current_player_idx.assert_called_once()


class TestShowStatsCommand(unittest.TestCase):
    """Tests for ShowStatsCommand."""

    def test_execute_succeeds(self):
        """Test execute phase succeeds."""
        # Arrange
        game = Mock()
        game.get_player_stats.return_value = [
            {"player_idx": 0, "money": [1, 2, 3, 4, 5, 6], "cows": [10], "score": 10}
        ]
        command = ShowStatsCommand()

        # Act
        result = command.execute(game)

        # Assert
        self.assertEqual(result.type, ResultType.SUCCESS)
        self.assertEqual(command.command_state, CommandState.EXECUTED)
        game.get_player_stats.assert_called_once()


