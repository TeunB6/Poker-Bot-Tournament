from __future__ import annotations
from texasholdem import TexasHoldEm, ActionType
from texasholdem.gui import TextGUI
from poker_agent import PokerAgentABC, RandomAgent
import threading
from warnings import warn
import _thread
from contextlib import contextmanager

USE_GUI_ANIMATIONS = False


class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg

@contextmanager
def time_limit(seconds, msg=''):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()


class Judge():
    def __init__(self, *players: PokerAgentABC, time_limit: int = 2, # 2s per player move, otherwise fold
                 max_players: int = 9, buyin: int= 500, 
                 small_blind: int = 5, big_blind: int = 10): 
        self.players = players + [RandomAgent() for _ in range(max_players - len(players))]
        self.game = TexasHoldEm(max_players=max_players, buyin=buyin, 
                                small_blind=small_blind, big_blind=big_blind)
        self.time_limit = time_limit        

    def run_hand(self, verbose: bool = False, display: bool = False):
        self.game.start_hand()
        
        if display:
            gui = TextGUI(self.game, enable_animations=USE_GUI_ANIMATIONS)
        
        while self.game.is_hand_running():
            player: PokerAgentABC = self.players[self.game.current_player]
            try:
                with time_limit(seconds=self.time_limit, msg=f'{self.game.current_player}: FOLD action performed instead'):
                    move = player.choose_action()
            except TimeoutException:
                move = ActionType.FOLD

            if not self.game.validate_move(self.game.current_player, *move):
                move = ActionType.FOLD
                warn(f'Invalid move {move} by {self.game.current_player}. Defaulting to FOLD.')
            
            if display:
                gui.display_state()
                gui.wait_until_prompted()

            self.game.take_action(*move)
            
            if display:
                gui.display_action()
        
        if display:
            gui.display_win()