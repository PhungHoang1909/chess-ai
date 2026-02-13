import pygame
import chess
import math
from settings import (
    LIGHT, DARK, HIGHLIGHT, MOVE_HINT, CHECK, HOVER,
    SQUARE_SIZE, IMAGES_DIR, ANIMATION_SPEED
)
from src.utils import square_to_coords, lerp

# -----------------------------------------------------------------
# Load piece images (once)
# -----------------------------------------------------------------
piece_images = {}

def load_pieces():
    piece_names = {
        'p': 'bp', 'n': 'bn', 'b': 'bb', 'r': 'br', 'q': 'bq', 'k': 'bk',
        'P': 'wp', 'N': 'wn', 'B': 'wb', 'R': 'wr', 'Q': 'wq', 'K': 'wk'
    }
    for symbol, filename in piece_names.items():
        try:
            img = pygame.image.load(f"{IMAGES_DIR}/{filename}.png")
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            piece_images[symbol] = img
        except FileNotFoundError:
            print(f"Warning: {IMAGES_DIR}/{filename}.png not found.")

def get_piece_image(symbol):
    return piece_images.get(symbol)

# -----------------------------------------------------------------
# Board drawing
# -----------------------------------------------------------------
def draw_board(screen, hover_square=None, perspective=chess.WHITE):
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

    # Hover effect
    if hover_square is not None:
        x, y = square_to_coords(hover_square, perspective)
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HOVER)
        screen.blit(s, (x, y))

# -----------------------------------------------------------------
# Piece drawing with smooth animation
# -----------------------------------------------------------------
class AnimatedPiece:
    def __init__(self, piece, from_square, to_square, perspective):
        self.piece = piece
        self.from_square = from_square
        self.to_square = to_square
        self.perspective = perspective
        self.progress = 0.0
        self.active = True

    def update(self, dt):
        self.progress += dt / ANIMATION_SPEED
        if self.progress >= 1.0:
            self.progress = 1.0
            self.active = False

    def draw(self, screen):
        from_x, from_y = square_to_coords(self.from_square, self.perspective)
        to_x, to_y = square_to_coords(self.to_square, self.perspective)
        x = lerp(from_x, to_x, self.progress)
        y = lerp(from_y, to_y, self.progress)
        img = get_piece_image(self.piece.symbol())
        if img:
            screen.blit(img, (x, y))

def draw_pieces(screen, board, perspective, animated_moves=None):
    moving_square = None
    if animated_moves:
        for anim in animated_moves:
            if anim.active:
                moving_square = anim.to_square
                break

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and square != moving_square:
            x, y = square_to_coords(square, perspective)
            img = get_piece_image(piece.symbol())
            if img:
                screen.blit(img, (x, y))

    if animated_moves:
        for anim in animated_moves:
            if anim.active:
                anim.draw(screen)

# -----------------------------------------------------------------
# Highlights
# -----------------------------------------------------------------
def highlight_square(screen, square, perspective, color=HIGHLIGHT, alpha=80):
    if square is None:
        return
    x, y = square_to_coords(square, perspective)
    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    s.fill(color + (alpha,))
    screen.blit(s, (x, y))

def draw_move_hints(screen, board, square, perspective, time_ms):
    if square is None:
        return
    piece = board.piece_at(square)
    if piece is None:
        return
    pulse = 0.5 + 0.5 * math.sin(time_ms * 0.005)
    radius = int(SQUARE_SIZE // 6 * (0.8 + pulse * 0.4))
    for move in board.legal_moves:
        if move.from_square == square:
            x, y = square_to_coords(move.to_square, perspective)
            center = (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, MOVE_HINT, center, radius)
            pygame.draw.circle(screen, (255, 255, 255), center, radius-2, 1)

def draw_check(screen, board, perspective):
    if board.is_check():
        king_square = board.king(board.turn)
        if king_square is not None:
            highlight_square(screen, king_square, perspective, color=CHECK, alpha=120)