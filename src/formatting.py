from texasholdem import ActionType, TexasHoldEm
from copy import deepcopy
    
def format_game_state_str(game: TexasHoldEm, history: str) -> str:
    return f"{game.players[game.current_player].state.value};\
            {''.join([str(c) for c in game.hands[game.current_player]])};\
            {''.join([str(c) for c in game.board])};{game.players[game.current_player].chips};\
            {game.chips_at_stake(game.current_player)}||{history}"


def format_game_state_dict(game: TexasHoldEm, history: list) -> dict:
    return {
        "player_states": [p.state for p in game.players],
        "hand": deepcopy(game.hands[game.current_player]),
        "board": deepcopy(game.board),
        "chips": [p.chips for p in game.players],
        "at_stake": [game.chips_at_stake(p) for p in game.players],
        "move_history": deepcopy(history)
    }

def format_move(player_id: int, move: tuple[ActionType, int]) -> str:
    return f"{player_id}:{move[0].name}" + f"{':{}\n'.format(move[1]) if move[1] is not None else ':\n'}"
        