"""
This module contains the Judge class which is responsible for managing a game of Texas Hold'em poker.
It handles the initialization of the game, running hands, and managing player actions with a time limit.
"""

from __future__ import annotations
from texasholdem import TexasHoldEm, ActionType
from texasholdem.gui import TextGUI
from poker_agent import PokerAgentABC, RandomAgent, CallAgent
from game_state import format_game_state
import threading
from warnings import warn
import _thread
from contextlib import contextmanager
from time import sleep

USE_GUI_ANIMATIONS = False

class TimeoutException(Exception):
    """
    Exception raised when a player exceeds the allowed time limit for making a move.
    """
    def __init__(self, msg=''):
        self.msg = msg

@contextmanager
def time_limit(seconds, msg=''):
    """
    Context manager to enforce a time limit on a block of code.
    Args:
        seconds (int): The time limit in seconds.
        msg (str): The message to display if the time limit is exceeded.
    """
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()

class Judge:
    """
    The Judge class manages a game of Texas Hold'em poker, including player actions, game state, and enforcing time limits.
    Attributes:
        players (list): List of players participating in the game.
        rewards (list): List of rewards for each player.
        _settings (dict): Dictionary containing game settings.
        game (TexasHoldEm): Instance of the TexasHoldEm game.
        time_limit (int): Time limit for each player's move.
    """
    def __init__(self, *players: PokerAgentABC, time_limit: int = 2, max_players: int = 5, buyin: int = 500, small_blind: int = 5, big_blind: int = 10):
        """
        Initializes the Judge with the given players and game settings.
        Args:
            players (PokerAgentABC): Players participating in the game.
            time_limit (int): Time limit for each player's move.
            max_players (int): Maximum number of players.
            buyin (int): Buy-in amount for each player.
            small_blind (int): Small blind amount.
            big_blind (int): Big blind amount.
        """
        self.players = list(players) + [RandomAgent() for _ in range(max_players - len(players))]
        self.rewards = [0] * len(self.players)
        max_players = len(self.players)
        self._settings = {"max_players": max_players, "buyin": buyin, "small_blind": small_blind, "big_blind": big_blind}
        
        for idx, p in enumerate(self.players):
            p.set_id(idx)
        
        self.game = TexasHoldEm(max_players=max_players, buyin=buyin, 
                                small_blind=small_blind, big_blind=big_blind)
        self.time_limit = time_limit        

    def run_hand(self, verbose: bool = False, display: bool = False, auto: bool = True, delay: float = 0.5) -> str:
        """
        Runs a single hand of Texas Hold'em poker.
        Args:
            verbose (bool): If True, prints detailed information about the game.
            display (bool): If True, displays the game using a GUI.
            auto (bool): If True, automatically progresses the game without waiting for user input.
            delay (float): Delay between actions in seconds.
        Returns:
            str: History of the hand.
        """
        self.game.start_hand()
        history = ""
        
        if display:
            gui = TextGUI(self.game, enable_animation=USE_GUI_ANIMATIONS, no_wait=auto)
        
        while self.game.is_hand_running():
            player_id = self.game.current_player
            player: PokerAgentABC = self.players[player_id]
            try:
                with time_limit(seconds=self.time_limit, msg=f'{player_id}: FOLD action performed instead'):
                    s = format_game_state(self.game.players[player_id].state, self.game.hands[player_id], 
                                          self.game.board, self.game.players[player_id].chips, self.game.chips_at_stake(player_id), history)
                    move = player.choose_action(s, self.game.get_available_moves())
            except TimeoutException:
                move = (ActionType.FOLD, None)

            if not self.game.validate_move(player_id, *move):
                move = (ActionType.FOLD, None)
                warn(f'Invalid move {move} by {player_id}. Defaulting to FOLD.')
            
            history += f"{player_id}:{move[0].value}" + f"{':{}|'.format(move[1]) if move[1] is not None else ':|'}"   
            
            if display:
                gui.display_state()
                if auto: 
                    sleep(delay)
                gui.wait_until_prompted()

            self.game.take_action(*move)
            
            if display:
                gui.display_action()
        
        if display:
            gui.display_win()
        
        history += f"|RESULT||{','.join(str(card) for card in self.game.board)}|{sum(p.amount for p in self.game.pots)}|{','.join(f'{player.player_id}:{player.chips}' for player in self.game.players)}"
        self.rewards = [current_reward + player.chips for current_reward, player in zip(self.rewards, self.game.players)]
        return history
    
    def run_hand_n_times(self, num_rounds: int = 100, verbose: bool = False, display: bool = False, auto: bool = True, delay: float = 0.5) -> list[str]:
        """
        Runs multiple hands of Texas Hold'em poker.
        Args:
            num_rounds (int): Number of hands to run.
            verbose (bool): If True, prints detailed information about the game.
            display (bool): If True, displays the game using a GUI.
            auto (bool): If True, automatically progresses the game without waiting for user input.
            delay (float): Delay between actions in seconds.
        Returns:
            list[str]: List of histories for each hand.
        """
        history = []
        for _ in range(num_rounds):
            history.append(self.run_hand(verbose=verbose, display=display, auto=auto, delay=delay))
        
        return history
    
    def run_game(self, reset: bool = True, verbose: bool = False, display: bool = False, auto: bool = True, delay: float = 0.5) -> tuple[list[str], int, int]:
        """
        Runs a complete game of Texas Hold'em poker. Ends when only one player is able to play
        Args:
            reset (bool): If True, resets the game before starting.
            verbose (bool): If True, prints detailed information about the game.
            display (bool): If True, displays the game using a GUI.
            auto (bool): If True, automatically progresses the game without waiting for user input.
            delay (float): Delay between actions in seconds.
        Returns:
            tuple[list[str], int, int]: History of the game, ID of the winning player, and chips of the winning player.
        """
        history = []
        if reset:
            self.reset()
        while self.game.is_game_running():
            history.append(self.run_hand(verbose=verbose, display=display, auto=auto, delay=delay))
        if display:
            gui = TextGUI(self.game, enable_animation=USE_GUI_ANIMATIONS, no_wait=auto)
            gui.display_win()
        
        winner = max(self.game.players, key=lambda x: x.chips)
        
        return history, winner.player_id, winner.chips

    def run_game_n_times(self, num_rounds: int = 100, reset: bool = True, verbose: bool = False, display: bool = False, auto: bool = True, delay: float = 0.5) -> tuple[list[str], int, int]:
        """
        Runs multiple games of Texas Hold'em poker.
        Args:
            num_rounds (int): Number of games to run.
            reset (bool): If True, resets the game before starting each game.
            verbose (bool): If True, prints detailed information about the game.
            display (bool): If True, displays the game using a GUI.
            auto (bool): If True, automatically progresses the game without waiting for user input.
            delay (float): Delay between actions in seconds.
        Returns:
            tuple[list[str], int, int]: History of all games, win count for each player, and chips count for each player.
        """
        history = []
        win_cnt = [0] * len(self.players)
        chips_cnt = [0] * len(self.players)
        
        for _ in range(num_rounds):
            h, win, chips = self.run_game(reset=reset, verbose=verbose, display=display, auto=auto, delay=delay)
            history.append(h)
            win_cnt[win] += 1
            chips_cnt[win] += chips
        
        return history, win_cnt, chips_cnt

    def reset(self):
        """
        Resets the game to its initial state.
        """
        self.rewards = [0] * len(self.players)
        self.game = TexasHoldEm(*self._settings.values())
        
if __name__ == '__main__':
    judge = Judge(*[CallAgent()]*4)
    h = judge.run_hand_n_times(display=False)
    #print(h)
    print(judge.rewards)
    