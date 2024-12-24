from abc import ABC, abstractmethod
from texasholdem import ActionType, MoveIterator, PlayerState
from typing import Union


class PokerAgentABC(ABC):
    def __init__(self):
        pass
    
    def set_id(self, id):
        self._id = id
    
    @abstractmethod
    def choose_action(self, game_state: str, available_moves: MoveIterator) -> Union[tuple[ActionType, int], ActionType]:
        pass
    
class RandomAgent(PokerAgentABC):
    def __init__(self):
        pass
    
    def choose_action(self, game_state: str, available_moves: MoveIterator) -> Union[tuple[ActionType, int], ActionType]:
        return available_moves.sample()

class CallAgent(PokerAgentABC):
    def __init__(self):
        pass
    
    def choose_action(self, game_state: str, available_moves: MoveIterator) -> Union[tuple[ActionType, int], ActionType]:
        state = int(game_state[0])
        if state == PlayerState.TO_CALL.value:
            return ActionType.CALL, None
        return ActionType.CHECK, None