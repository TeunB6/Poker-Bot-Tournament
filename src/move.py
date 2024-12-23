from general import MoveType
from typing import Optional
    
class Move:
    def __init__(self, type: MoveType, amount: Optional[int] = None):
        self.type : MoveType = type
        
        if type == MoveType.RAISE:
            if not isinstance(amount, int): raise ValueError(f"type is {self.type} yet amount is not provided: {amount}")
            self.amount : int = amount
        
    