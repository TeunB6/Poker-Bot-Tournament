import unittest
from texasholdem.card import Card
from texasholdem import PlayerState, TexasHoldEm, ActionType
from src.formatting import format_game_state_dict, format_move

class TestFormatting(unittest.TestCase):

    def setUp(self):
        self.game = TexasHoldEm(max_players=2, buyin=500, small_blind=5, big_blind=10)
        self.game.start_hand()
        self.history = "0:CALL|1:RAISE:100|"

    def test_format_game_state_dict(self):
        game_state = format_game_state_dict(self.game, self.history)
        self.assertIsInstance(game_state, dict)
        self.assertIn("player_states", game_state)
        self.assertIn("hand", game_state)
        self.assertIn("board", game_state)
        self.assertIn("chips", game_state)
        self.assertIn("at_stake", game_state)
        self.assertIn("move_history", game_state)

    def test_format_move(self):
        move = (ActionType.CALL, None)
        formatted_move = format_move(0, move)
        self.assertEqual(formatted_move, "0:CALL:|")

if __name__ == '__main__':
    unittest.main()
