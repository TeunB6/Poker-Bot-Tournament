from general import MoveType

    
class Move:
    def __init__(self, type: MoveType, amount: int =0):
        self.type : MoveType = type
        self.amount : int = amount
        
    