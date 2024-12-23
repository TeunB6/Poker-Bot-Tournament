from __future__ import annotations

from player_abc import PlayerABC
from move import Move, MoveType
from agents.random_agent import SaveRandomAgent
from poker import Hand, Card
from general import Blind, PlayerState, HandPhase
from typing import Iterable, Iterator
from collections import deque
import random

NUM_PLAYERS = 8
BIG_BLIND = 10

class PlayerJudge:
    def __init__(self, player: PlayerABC):
        self.player = player
        self._chips = player.chips
        self._hand = player.hand
        self.state = PlayerState.TO_CALL
    
    @property
    def chips(self):
        return self._chips

    @chips.setter
    def chips(self, new: int):
        self.player.chips = new
        self._chips = new
        
    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, new: int):
        self.player.hand = new
        self._hand = new

    def choose_move(self, community_cards: list[Card], bet: int, pot: int) -> Move:
        return self.player.choose_move(community_cards, bet, pot)

class Judge:
    def __init__(self, *players: PlayerJudge, starting_chips: int = 100) -> None:
        raw_players = players
        if len(raw_players) < NUM_PLAYERS:
            raw_players += [SaveRandomAgent() for _ in range(NUM_PLAYERS - len(raw_players))]
        
        self.players = [PlayerJudge(p) for p in raw_players]
        self.max_players = len(self.players)
        
    def run_game(self, num_rounds: int = 100) -> None:
        # Setup:
        self.sb_loc = random.randint(0, NUM_PLAYERS)
        self.bb_loc = (self.sb_loc + 1) % NUM_PLAYERS
        self.community_cards = []
        
        for _ in range(num_rounds):            
            self.run_hand()
            self.sb_loc += 1; self.sb_loc %= NUM_PLAYERS
            self.bb_loc += 1; self.bb_loc %= NUM_PLAYERS
    
    def _bet(self, player: PlayerJudge, amount: int):
        if amount > player.chips:
            amount = player.chips
            raise Warning("Warning: Bet placed greater than Chips, defaulting to ALL-IN")
        player.chips -= amount
        self.pot += amount
        self.ante = max(amount, self.ante)
    
    def _validate_move(self, move: Move, player: PlayerJudge, raises: bool = True) -> bool:
        return True
    
    def _execute_move(self, move: Move, player: PlayerJudge) -> None:
        
        if self._validate_move(self, move, player):
            move.type = MoveType.FOLD
        
        match move.type:
            case MoveType.FOLD:
                player.state = PlayerState.OUT
            case MoveType.CHECK:
                pass
            case MoveType.RAISE:
                self._bet(player, move.amount)
                for p in self.players:
                    if p.state == PlayerState.IN: 
                        p.state = PlayerState.TO_CALL
                player.state = PlayerState.IN
            case MoveType.CALL:
                self._bet(player, self.ante)
                player.state = PlayerState.IN
        if player.chips == 0:
            player.state = PlayerState.ALL_IN
    
    def _betting_round(self):
        # Add new cards
        self.community_cards += [self.deck.pop() for _ in range(self._phase.new_cards())]
        if self._phase == HandPhase.PREFLOP:
            self.current_player = self.bb_loc
        else:
            self.current_player = self.sb_loc
        
        player_queue = deque(self.active_iter(self.current_player))
        
        while not self._is_hand_over():
            self.current_player = player_queue.popleft()
            move = self.players[self.current_player].choose_move(self.community_cards, self.ante, self.pot)
            self._execute_move(move, self.players[self.current_player])
                        
            if move.type == MoveType.RAISE:
                # reset the round (i.e. as if the betting round started here)
                player_queue = deque(self.active_iter(self.current_player))
                if self.players[self.current_player].state != PlayerState.ALL_IN:
                    player_queue.popleft()
            
    
    def run_hand(self): #TODO fix case where player chips == 0
        # Setup:
        self.players[self.sb_loc].blind_type = Blind.SMALL
        self.players[self.bb_loc].blind_type = Blind.BIG
        self.pot = 0
        self.ante = 0
        self.deck = list(Card)
        random.shuffle(self.deck)
        
        # Correct chips and hands
        for player in self.players:
            player.chips = 100  # Initialize chips
            player.hand = Hand.from_cards(self.deck.pop(), self.deck.pop())
        
        ## Play Round:
        # Opening
        self._phase = HandPhase.PREFLOP
        self._bet(self.players[self.sb_loc], BIG_BLIND // 2)
        self._bet(self.players[self.bb_loc], BIG_BLIND)

        # Play
        while (self._phase != HandPhase.PREHAND):
            self._betting_round()
            self._phase = self._phase.next_phase()

    def _is_hand_over(self) -> bool:
        count = 0
        for i in self.active_iter():
            if self.players[i].state == PlayerState.TO_CALL:
                return False
            
            if self.players[i].state == PlayerState.IN:
                count += 1

            if count > 1:
                return False

        return True
    
    def player_iter(
        self,
        loc: int = None,
        reverse: bool = False,
        match_states: Iterable[PlayerState] = tuple(PlayerState),
        filter_states: Iterable[PlayerState] = (),
    ) -> Iterator[int]:
        """
        Iterates through all players starting at player_id and rotating in order
        of increasing player id.

        Arguments:
            loc (int, optional): The player_id to start at, default is :attr:`current_player`.
            reverse (bool): In reverse play order, default False
            match_states (Iterable[PlayerState]): Only include players with the given states
            filter_states (Iterable[PlayerState]): Exclude players with the given states
        Returns:
            Iterator[int]: An iterator over all player ids.

        """
        if loc is None:
            loc = self.current_player

        loc = loc % self.max_players

        start, stop, step = loc, loc + self.max_players, 1
        if reverse:
            start, stop, step = stop, start, -step

        for i in range(start, stop, step):
            if (
                self.players[i % self.max_players].state not in filter_states
                and self.players[i % self.max_players].state in match_states
            ):
                yield i % self.max_players

    def in_pot_iter(self, loc: int = None, reverse: bool = False) -> Iterator[int]:
        """
        Iterates through all players with a stake in the pot (i.e. all players without
        states :obj:`~texasholdem.game.player_state.PlayerState.OUT` or
        :obj:`~texasholdem.game.player_state.PlayerState.SKIP`

        Arguments:
            loc (int, optional): The location to start at, defaults to current_player
            reverse (bool): In reverse play order, default False
        Returns:
            Iterator[int]: An iterator over players with a stake in the pot

        """
        if loc is None:
            loc = self.current_player
        yield from self.player_iter(
            loc=loc, reverse=reverse, filter_states=(PlayerState.OUT, PlayerState.SKIP)
        )

    def active_iter(self, loc: int = None, reverse: bool = False) -> Iterator[int]:
        """
        Iterates through all players that can take an action.
        i.e. players with states :obj:`~texasholdem.game.player_state.PlayerState.IN`
        or :obj:`~texasholdem.game.player_state.PlayerState.TO_CALL` (not including
        :obj:`~texasholdem.game.player_state.PlayerState.ALL_IN`).

        Arguments:
            loc (int, optional): The location to start at, defaults to current_player
            reverse (bool): In reverse play order, default False
        Returns:
            Iterator[int]: An iterator over active players who can take an action.

        """
        if loc is None:
            loc = self.current_player
        yield from self.player_iter(
            loc=loc, reverse=reverse, match_states=(PlayerState.TO_CALL, PlayerState.IN)
        )


