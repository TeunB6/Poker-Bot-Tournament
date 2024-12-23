import unittest
from src.game import PlayerJudge, Judge
from src.player_abc import PlayerABC
from src.move import Move, MoveType
from poker import Hand, Card
from src.general import Blind, PlayerState, HandPhase

class MockPlayer(PlayerABC):
    def __init__(self):
        self._chips = 100
        self._hand = Hand()
        self._blind_type = Blind.DEFAULT

    def choose_move(self, community_cards: list[Card], ante: int, pot: int) -> Move:
        return Move(MoveType.CHECK)

class TestPlayerJudge(unittest.TestCase):
    def setUp(self):
        self.mock_player = MockPlayer()
        self.player_judge = PlayerJudge(self.mock_player)

    def test_chips_property(self):
        self.assertEqual(self.player_judge.chips, 100)
        self.player_judge.chips = 50
        self.assertEqual(self.player_judge.chips, 50)
        self.assertEqual(self.mock_player.chips, 50)

    def test_hand_property(self):
        hand = Hand.from_cards(Card('2H'), Card('3D'))
        self.player_judge.hand = hand
        self.assertEqual(self.player_judge.hand, hand)
        self.assertEqual(self.mock_player.hand, hand)

    def test_choose_move(self):
        move = self.player_judge.choose_move([], 0, 0)
        self.assertEqual(move.type, MoveType.CHECK)

class TestJudge(unittest.TestCase):
    def setUp(self):
        self.mock_players = [MockPlayer() for _ in range(8)]
        self.judge = Judge(*self.mock_players)

    def test_initialization(self):
        self.assertEqual(len(self.judge.players), 8)
        self.assertEqual(self.judge.max_players, 8)

    def test_run_game(self):
        self.judge.run_game(num_rounds=1)
        self.assertTrue(self.judge.sb_loc >= 0)
        self.assertTrue(self.judge.bb_loc >= 0)

    def test_bet(self):
        player = self.judge.players[0]
        self.judge._bet(player, 10)
        self.assertEqual(player.chips, 90)
        self.assertEqual(self.judge.pot, 10)

    def test_execute_move(self):
        player = self.judge.players[0]
        move = Move(MoveType.RAISE, 10)
        self.judge._execute_move(move, player)
        self.assertEqual(player.chips, 90)
        self.assertEqual(self.judge.pot, 10)

if __name__ == '__main__':
    unittest.main()
