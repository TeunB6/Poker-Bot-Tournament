from player_abc import PlayerABC
from move import Move, MoveType
import random

class SaveRandomAgent(PlayerABC):
    def __init__(self):
        pass
    
    def choose_move(self, community_cards, ante, pot):
        move_type = random.choices(list(MoveType), [0.3, 0.2, 0.5])
        value = 0
        if move_type == MoveType.RAISE:
            value = random.randint(ante + 1, ante + self.chips / 2)
        return Move(move_type, value)
    
class FullRandomAgent(PlayerABC):
    def __init__(self):
        pass

    def choose_move(self, community_cards, ante, pot):
        move_type = random.choice(list(MoveType))
        value = 0
        if move_type == MoveType.RAISE:
            value = random.randint(ante + 1, self.chips)
        return Move(move_type, value)
