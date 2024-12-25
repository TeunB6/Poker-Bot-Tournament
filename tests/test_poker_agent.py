import unittest
from src.poker_agent import PokerAgentABC, RandomAgent, CallAgent
from texasholdem import ActionType, MoveIterator, PlayerState

class TestPokerAgentABC(unittest.TestCase):

    def test_set_id(self):
        agent = RandomAgent()
        agent.set_id(1)
        self.assertEqual(agent._id, 1)

class TestRandomAgent(unittest.TestCase):

    def test_choose_action(self):
        agent = RandomAgent()
        available_moves = MoveIterator({ActionType.CALL: None, ActionType.FOLD: None})
        action = agent.choose_action("", available_moves)
        self.assertIn(action, {ActionType.CALL: None, ActionType.FOLD: None}.items())

class TestCallAgent(unittest.TestCase):

    def test_choose_action_to_call(self):
        agent = CallAgent()
        agent.set_id(0)
        game_state ={"player_states": [PlayerState.TO_CALL]}
        available_moves = MoveIterator({ActionType.CALL: None, ActionType.FOLD: None})
        action = agent.choose_action(game_state, available_moves)
        self.assertEqual(action, (ActionType.CALL, None))

    def test_choose_action_to_check(self):
        agent = CallAgent()
        agent.set_id(0)
        game_state ={"player_states": [PlayerState.IN]}
        available_moves = MoveIterator({ActionType.CHECK: None, ActionType.FOLD: None})
        action = agent.choose_action(game_state, available_moves)
        self.assertEqual(action, (ActionType.CHECK, None))

if __name__ == '__main__':
    unittest.main()
