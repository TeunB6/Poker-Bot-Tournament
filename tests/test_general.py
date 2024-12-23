import unittest
from src.general import Blind, MoveType, PlayerState, HandPhase

class TestGeneral(unittest.TestCase):
    def test_blind_enum(self):
        self.assertEqual(Blind.DEFAULT.name, "DEFAULT")
        self.assertEqual(Blind.SMALL.name, "SMALL")
        self.assertEqual(Blind.BIG.name, "BIG")

    def test_move_type_enum(self):
        self.assertEqual(MoveType.RAISE.name, "RAISE")
        self.assertEqual(MoveType.CALL.name, "CALL")
        self.assertEqual(MoveType.CHECK.name, "CHECK")
        self.assertEqual(MoveType.FOLD.name, "FOLD")

    def test_player_state_enum(self):
        self.assertEqual(PlayerState.OUT.name, "OUT")
        self.assertEqual(PlayerState.IN.name, "IN")
        self.assertEqual(PlayerState.TO_CALL.name, "TO_CALL")
        self.assertEqual(PlayerState.ALL_IN.name, "ALL_IN")

    def test_hand_phase_enum(self):
        self.assertEqual(HandPhase.PREHAND.name, "PREHAND")
        self.assertEqual(HandPhase.PREFLOP.name, "PREFLOP")
        self.assertEqual(HandPhase.FLOP.name, "FLOP")
        self.assertEqual(HandPhase.TURN.name, "TURN")
        self.assertEqual(HandPhase.RIVER.name, "RIVER")
        self.assertEqual(HandPhase.SETTLE.name, "SETTLE")

    def test_hand_phase_next_phase(self):
        self.assertEqual(HandPhase.PREHAND.next_phase(), HandPhase.PREFLOP)
        self.assertEqual(HandPhase.PREFLOP.next_phase(), HandPhase.FLOP)
        self.assertEqual(HandPhase.FLOP.next_phase(), HandPhase.TURN)
        self.assertEqual(HandPhase.TURN.next_phase(), HandPhase.RIVER)
        self.assertEqual(HandPhase.RIVER.next_phase(), HandPhase.SETTLE)
        self.assertEqual(HandPhase.SETTLE.next_phase(), HandPhase.PREHAND)

    def test_hand_phase_new_cards(self):
        self.assertEqual(HandPhase.PREHAND.new_cards(), 0)
        self.assertEqual(HandPhase.PREFLOP.new_cards(), 0)
        self.assertEqual(HandPhase.FLOP.new_cards(), 3)
        self.assertEqual(HandPhase.TURN.new_cards(), 1)
        self.assertEqual(HandPhase.RIVER.new_cards(), 1)
        self.assertEqual(HandPhase.SETTLE.new_cards(), 0)

if __name__ == '__main__':
    unittest.main()
