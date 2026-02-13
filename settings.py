import chess
import pygame

# -----------------------------------------------------------------
# Window & Board – base size (menu uses these dimensions)
# -----------------------------------------------------------------
WIDTH = 720
HEIGHT = 720
SQUARE_SIZE = WIDTH // 8
BOARD_POS = (0, 0)

# -----------------------------------------------------------------
# Classic Chess Colors
# -----------------------------------------------------------------
LIGHT = (240, 217, 181)          # light wood
DARK  = (181, 136, 99)           # dark wood
HIGHLIGHT = (255, 255, 0)        # yellow
MOVE_HINT = (0, 180, 0)          # green
CHECK = (255, 80, 80)           # red
HOVER = (255, 255, 200, 60)     # soft yellow overlay

# Menu – bright and clean
MENU_BG = (245, 245, 240)        # off-white
BUTTON_COLOR = (70, 130, 180)    # steel blue
BUTTON_HOVER = (100, 160, 210)   # lighter blue
TEXT_COLOR = (30, 30, 30)        # dark grey
TITLE_COLOR = (50, 50, 80)       # navy

# Panel – complements the board
PANEL_BG = (220, 220, 210)       # light beige
PANEL_TEXT = (30, 30, 30)

# -----------------------------------------------------------------
# Timing
# -----------------------------------------------------------------
AI_DELAY = 400
ANIMATION_SPEED = 0.15
FPS = 60

# -----------------------------------------------------------------
# AI Search depths
# -----------------------------------------------------------------
MIN_DEPTH = 1
MAX_DEPTH = 6
DEFAULT_DEPTH = 3

# -----------------------------------------------------------------
# Piece values
# -----------------------------------------------------------------
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

# -----------------------------------------------------------------
# Paths
# -----------------------------------------------------------------
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
SAVE_FILE = "save.json"