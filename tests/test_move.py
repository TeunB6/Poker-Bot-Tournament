import unittest
from src.move import Move, MoveType

class TestMove(unittest.TestCase):
    def test_move_initialization(self):
        move = Move(MoveType.CHECK)
        self.assertEqual(move.type, MoveType.CHECK)
        self.assertIsNone(move.amount)

    def test_raise_move_initialization(self):
        move = Move(MoveType.RAISE, 50)
        self.assertEqual(move.type, MoveType.RAISE)
        self.assertEqual(move.amount, 50)

    def test_raise_move_without_amount(self):
        with self.assertRaises(ValueError):
            Move(MoveType.RAISE)

if __name__ == '__main__':
    unittest.main()
