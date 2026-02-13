import json
import chess
from settings import SAVE_FILE

def save_game(board, depth, ai_color, player_color):
    data = {
        "fen": board.fen(),
        "depth": depth,
        "ai_color": ai_color,
        "player_color": player_color
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_game():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        board = chess.Board(data["fen"])
        return (
            board,
            data["depth"],
            data["ai_color"],
            data["player_color"]
        )
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return None