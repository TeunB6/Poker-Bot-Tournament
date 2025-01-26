import unittest
from src.judge import Judge, TimeoutException, time_limit
from src.poker_agent import CallAgent, RandomAgent
from time import sleep


class TestJudge(unittest.TestCase):

    def setUp(self):
        self.judge = Judge(*[CallAgent() for _ in range(5)], time_limit=2)

    def test_initialization(self):
        self.assertEqual(len(self.judge.players), 5)
        self.assertEqual(len(self.judge.rewards), 5)
        self.assertEqual(self.judge.time_limit, 2)

    def test_run_hand(self):
        history = self.judge.run_hand()
        self.assertIsInstance(history, list)
        self.assertTrue(len(history) > 0)

    def test_run_hand_n_times(self):
        histories = self.judge.run_hand_n_times(num_rounds=10)
        self.assertEqual(len(histories), 10)
        for history in histories:
            self.assertIsInstance(history, list)
            self.assertTrue(len(history) > 0)

    def test_run_game(self):
        history, winner_id, winner_chips = self.judge.run_game(hand_limit=5)
        self.assertIsInstance(history, list)
        self.assertIsInstance(winner_id, int)
        self.assertIsInstance(winner_chips, int)

    def test_run_game_n_times(self):
        histories, win_cnt, chips_cnt = self.judge.run_game_n_times(num_rounds=10, hand_limit=5)
        self.assertEqual(len(histories), 10)
        self.assertEqual(len(win_cnt), 5)
        self.assertEqual(len(chips_cnt), 5)
        self.assertEqual(sum(win_cnt), 10)

    def test_timeout_exception(self):
        with self.assertRaises(TimeoutException):
            with time_limit(seconds=0.1, msg='test'):
                sleep(0.2)

if __name__ == '__main__':
    unittest.main()
