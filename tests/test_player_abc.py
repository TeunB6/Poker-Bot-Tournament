import unittest
from src.player_abc import PlayerABC
from src.move import Move, MoveType
from poker import Hand, Card
from src.general import Blind

class TestPlayerABC(unittest.TestCase):
    class ConcretePlayer(PlayerABC):
        def choose_move(self, community_cards: list[Card], ante: int, pot: int) -> Move:
            return Move(MoveType.CHECK)

    def setUp(self):
        self.player = self.ConcretePlayer()
        self.player._chips = 100
        self.player._hand = Hand()
        self.player._blind_type = Blind.DEFAULT

    def test_hand_property(self):
        hand = Hand.from_cards(Card('2H'), Card('3D'))
        self.player.hand = hand
        self.assertEqual(self.player.hand, hand)

    def test_blind_type_property(self):
        self.player.blind_type = Blind.SMALL
        self.assertEqual(self.player.blind_type, Blind.SMALL)
        with self.assertRaises(TypeError):
            self.player.blind_type = "Not a Blind"

    def test_chips_property(self):
        self.player.chips = 50
        self.assertEqual(self.player.chips, 50)
        with self.assertRaises(TypeError):
            self.player.chips = "Not an int"

    def test_choose_move(self):
        move = self.player.choose_move([], 0, 0)
        self.assertEqual(move.type, MoveType.CHECK)

if __name__ == '__main__':
    unittest.main()
