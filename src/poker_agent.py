from abc import ABC, abstractmethod
from texasholdem import ActionType, MoveIterator
from texasholdem.agents import random_agent
from typing import Union


class PokerAgentABC(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def choose_action(self, game_stat, available_moves: MoveIterator) -> Union[tuple[ActionType, int], ActionType]:
        pass
    
class RandomAgent(PokerAgentABC):
    def __init__(self):
        pass
    
    def choose_action(self, game_state) -> Union[tuple[ActionType, int], ActionType]:
        return random_agent(game=game_state, no_fold=True)