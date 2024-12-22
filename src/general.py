from enum import Enum
class Blind(Enum):
    DEFAULT : 0
    SMALL : 1
    BIG : 2

class MoveType(Enum):
    RAISE = 1
    HIT = 2
    FOLD = 3
    
