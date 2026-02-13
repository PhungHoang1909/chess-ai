import chess
from settings import SQUARE_SIZE

def get_square_from_mouse(pos, perspective):
    """Convert mouse coordinates to chess square index, respecting board flip."""
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= row < 8 and 0 <= col < 8:
        if perspective == chess.WHITE:
            chess_row = 7 - row
            chess_col = col
        else:
            chess_row = row
            chess_col = 7 - col
        return chess_row * 8 + chess_col
    return None

def square_to_coords(square, perspective):
    """Convert chess square to (x, y) pixel coordinates for drawing."""
    rank = square // 8
    file = square % 8
    if perspective == chess.WHITE:
        row = 7 - rank
        col = file
    else:
        row = rank
        col = 7 - file
    return col * SQUARE_SIZE, row * SQUARE_SIZE

def lerp(a, b, t):
    """Linear interpolation."""
    return a + (b - a) * t