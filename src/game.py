from player_abc import PlayerABC
from agents.random_agent import SaveRandomAgent
from poker import Hand, Card
from general import Blind
import random

NUM_PLAYERS = 8
BET_LIMIT = 10

class Judge:
    def __init__(self, *players: PlayerABC, starting_chips: int = 100):
        self.players = players
        if len(self.players) < NUM_PLAYERS:
            self.players += [SaveRandomAgent() for _ in range(NUM_PLAYERS - len(self.players))]
        
        self.players_dict = {i:(self.players[i], starting_chips, Hand()) for i in range(NUM_PLAYERS)}
        
    def run_game_secure(self, num_rounds: int = 100):
        # Setup:
        small_blind = random.randint(0,NUM_PLAYERS)
        big_blind = (small_blind + 1) % NUM_PLAYERS
        
        for _ in range(num_rounds):            
            self.run_round(small_blind, big_blind)
            small_blind += 1; small_blind %= NUM_PLAYERS
            big_blind += 1; big_blind %= NUM_PLAYERS
    
    def run_round_secure(self, small_blind: int, big_blind: int): #TODO fix case where player chips == 0
        # Setup:
        self.players[small_blind].blind_type = Blind.SMALL
        self.players[big_blind].blind_type = Blind.BIG
        
        deck = list(Card)
        random.shuffle(deck)
        
        # Correct chips and hands
        for player, chips, hand in self.players_dict.items():
            player.chips = chips
            hand = Hand.from_cards(deck.pop(), deck.pop())
            player.hand = hand
        
        # Play Round:
        self.players[small_blind].chips -= BET_LIMIT // 2 # Note that if bet limit is odd this is rounded down
        self.players[big_blind].chips -= BET_LIMIT
        
        
            
           