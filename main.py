import pygame
import chess
from settings import WIDTH, HEIGHT
from src.board import load_pieces
from src.menu import run_menu
from src.game import run_game

def main():
    pygame.init()
    pygame.mixer.init()  # for sound

    # Use full screen size with panel
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess AI")
    clock = pygame.time.Clock()

    # Load piece images once
    load_pieces()

    running = True
    while running:
        # Show menu
        result = run_menu(screen, clock)
        if result is None:
            break  # quit

        # Unpack result
        if isinstance(result[0], chess.Board):
            # Loaded game: (board, depth, ai_color, player_color)
            board, depth, ai_color, player_color = result
        else:
            # New game: (depth, ai_color, player_color, None)
            depth, ai_color, player_color, _ = result
            board = chess.Board()

        # Run game
        outcome = run_game(screen, clock, board, depth, ai_color, player_color)
        if outcome == 'quit':
            running = False
        elif outcome == 'menu':
            continue
        elif outcome == 'new':
            # Start a new game with same settings
            board = chess.Board()
            outcome = run_game(screen, clock, board, depth, ai_color, player_color)
            # (loop will handle outcome)

    pygame.quit()

if __name__ == "__main__":
    main()