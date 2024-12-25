from abc import ABC, abstractmethod
from texasholdem import ActionType, MoveIterator, PlayerState
from typing import Union
from time import sleep


class PokerAgentABC(ABC):
    def __init__(self):
        self._id = None
    
    def set_id(self, id):
        self._id = id
    
    @abstractmethod
    def choose_action(self, game_state: dict, available_moves: MoveIterator) -> Union[tuple[ActionType, int], ActionType]:
        pass
    
class RandomAgent(PokerAgentABC):
    def __init__(self):
        super().__init__()  
    
    def choose_action(self, game_state: dict, available_moves: MoveIterator) -> Union[tuple[ActionType, int], ActionType]:
        return available_moves.sample()

class CallAgent(PokerAgentABC):
    def __init__(self):
        super().__init__()  
    
    def choose_action(self, game_state: dict, available_moves: MoveIterator) -> Union[tuple[ActionType, int], ActionType]:
        state = game_state["player_states"][self._id].value
        if state == PlayerState.TO_CALL.value:
            return ActionType.CALL, None
        return ActionType.CHECK, None

class SleeperAgent(PokerAgentABC):
    def __init__(self):
        super().__init__()  
    
    def choose_action(self, game_state: dict, available_moves: MoveIterator) -> Union[tuple[ActionType, int], ActionType]:
        sleep(1) 