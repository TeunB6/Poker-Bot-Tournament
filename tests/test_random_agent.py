import unittest
from src.agents.random_agent import SaveRandomAgent, FullRandomAgent
from src.move import MoveType

class TestSaveRandomAgent(unittest.TestCase):
    def setUp(self):
        self.agent = SaveRandomAgent()
        self.agent._chips = 100

    def test_choose_move(self):
        move = self.agent.choose_move([], 0, 0)
        self.assertIn(move.type, MoveType)
        if move.type == MoveType.RAISE:
            self.assertTrue(0 < move.amount <= self.agent.chips / 2)

class TestFullRandomAgent(unittest.TestCase):
    def setUp(self):
        self.agent = FullRandomAgent()
        self.agent._chips = 100

    def test_choose_move(self):
        move = self.agent.choose_move([], 0, 0)
        self.assertIn(move.type, MoveType)
        if move.type == MoveType.RAISE:
            self.assertTrue(0 < move.amount <= self.agent.chips)

if __name__ == '__main__':
    unittest.main()
