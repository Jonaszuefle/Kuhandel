import pytest
from unittest.mock import MagicMock, patch

from game.game import Game

@pytest.fixture
def mock_config():
    """Simuliert die GameConfig"""
    with patch('game.game.GameConfig') as MockConfig:
        MockConfig.COW_CARD_VALUES = [10, 20, 30, 40] # Beispielwerte
        MockConfig.DONKEY_COW = 20                     # Der Esel
        MockConfig.MONEY_CARD_VALUES = [0, 10, 50, 100, 200, 500]
        yield MockConfig

@pytest.fixture
def mock_player_class():
    """Simuliert die Player Klasse"""
    with patch('game.game.Player') as MockPlayer:
        # Wenn ein Player() erstellt wird, geben wir ein Mock-Objekt zurück
        player_instance = MagicMock()
        player_instance.get_score.return_value = 100
        player_instance._cow_cards.get_cow_inventory.return_value = [10, 20]
        MockPlayer.return_value = player_instance
        yield MockPlayer

@pytest.fixture
def game(mock_config, mock_player_class):
    """Get new game instance for each test"""
    game = Game()
    game.start_game()
    return game

#-- Tests --

def test_game_start(game):
    assert game.num_players == 3
    assert len(game._players) == 3

    assert 0 <= game._current_player <= 2
    assert len(game._card_stack) > 0

def test_cow_draw(game):
    init_size_deck = len(game._card_stack)
    game.draw_cow_from_stack()

    assert game.current_cow_draw is not None
    assert game._is_card_stack_empty == False
    assert len(game._card_stack) == init_size_deck - 1

def test_last_cow_draw(game):
    game._card_stack = [10]
    game.draw_cow_from_stack()

    assert game.current_cow_draw == 10
    assert game._is_card_stack_empty == True
    assert len(game._card_stack) == 0

def test_undo_cow_draw(game):
    game.draw_cow_from_stack()
    current_size_deck = len(game._card_stack)
    current_card = game.current_cow_draw

    game.undo_cow_card_craw()

    assert game._card_stack[0] == current_card
    assert len(game._card_stack) == current_size_deck + 1

def test_donkey_cow_draw(game, mock_config):
    game.current_cow_draw = mock_config.DONKEY_COW
    assert game.is_donkey_cow() is True

    game.current_cow_draw = 99
    assert game.is_donkey_cow() is False

def test_player_inflation(game):
    game._money_inflation_stage = 3
    game.inflate_player_money()

    for player in game._players:
        player.add_money.assert_called_with([0,0,0,1,0,0])
    assert game._money_inflation_stage == 4


def test_handle_bid(game):
    """Test if cow and money is handeled correctly"""
    winner_idx = 0
    money_receiver_idx = 1
    money_amount = [10, 0, 0, 0, 0, 0]
    game.current_cow_draw = 50

    # Zugriff auf die Mock-Player Objekte
    winner = game._players[winner_idx]
    receiver = game._players[money_receiver_idx]

    game.handle_bid(winner_idx, money_receiver_idx, money_amount)

    # Assertions auf den Mock-Objekten: Wurden die Methoden richtig aufgerufen?
    winner.add_cow.assert_called_with(50, 1)
    winner.remove_money.assert_called_with(money_amount)
    receiver.add_money.assert_called_with(money_amount)

def test_handle_trade(game):
    """Test if cow and money is handeled correctly"""
    cow_type = 20
    cow_amount = 1
    game._current_player = 0
    challenged_player = 1
    money_amount_current = [0,0,1,0,0,0]
    money_amount_challenged = [0,1,0,0,0,0]
    winner_idx = 0
    looser_idx = 1

    winner = game._players[winner_idx]
    looser = game._players[looser_idx]

    game.handle_trade(cow_type, cow_amount, 1, money_amount_current, money_amount_challenged, winner_idx, looser_idx)

    winner.add_cow.assert_called_with(cow_type, cow_amount)
    looser.remove_cow.assert_called_with(cow_type, cow_amount)
    # and so on

    