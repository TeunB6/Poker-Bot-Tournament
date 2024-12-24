from texasholdem.card import Card
from texasholdem import PlayerState
    
def format_game_state(player_state: PlayerState, hand: list[Card], board: list[Card], chips: int, at_stake: int, history: str) -> str:
    return f"{player_state.value};{''.join([str(c) for c in hand])};{''.join([str(c) for c in board])};{chips};{at_stake}||{history}"
        