from abc import ABC, abstractmethod
from move import Move
from typing import List
from poker import Hand, Card
from general import Blind


class PlayerABC(ABC):
    @property
    def hand(self) -> Hand:
        return self._hand
    
    @hand.setter
    def hand(self, new: Hand) -> Hand:
        self._hand = new
    
    @property
    def blind_type(self) -> Blind:
        return self._blind_type
    
    @blind_type.setter
    def blind_type(self, new: Blind) -> Blind:
        if not isinstance(new, Blind):
            raise TypeError(f"{new} not of type Blind but of type {type(new)}")
        self._blind_type = new
    
    @property
    def chips(self) -> int:
        return self._chips
    
    @chips.setter
    def chips(self, new: int) -> int:
        if not isinstance(new, int):
            raise TypeError(f"{new} not of type int but of type {type(new)}")
        self._chips = new
    
    @abstractmethod
    def choose_move(self, community_cards: list[Card], ante: int, pot: int) -> Move:
        pass
    
    
         
    