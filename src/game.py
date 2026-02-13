import pygame
import chess
from settings import (
    HEIGHT, SQUARE_SIZE, AI_DELAY, FPS,
    HIGHLIGHT, PANEL_BG, PANEL_TEXT, TEXT_COLOR, BUTTON_COLOR, BUTTON_HOVER
)
from src.board import (
    draw_board, draw_pieces, draw_move_hints, highlight_square, draw_check,
    AnimatedPiece, get_piece_image
)
from src.ai import get_ai_move
from src.utils import get_square_from_mouse, square_to_coords
from src.sound import SoundManager
from src.save_load import save_game

# -----------------------------------------------------------------
# Screen dimensions – board is square, panel on the right
# -----------------------------------------------------------------
BOARD_WIDTH = HEIGHT
PANEL_WIDTH = 200
SCREEN_WIDTH = BOARD_WIDTH + PANEL_WIDTH
SCREEN_HEIGHT = HEIGHT

def draw_panel(screen, board, depth, ai_color, player_color, sound_mgr):
    """Draw game information panel with classic colors."""
    panel_rect = pygame.Rect(BOARD_WIDTH, 0, PANEL_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, PANEL_BG, panel_rect)

    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)

    # Turn indicator
    turn_text = "White" if board.turn == chess.WHITE else "Black"
    turn_label = font.render(f"Turn: {turn_text}", True, PANEL_TEXT)
    screen.blit(turn_label, (BOARD_WIDTH + 20, 30))

    # Player side
    player_text = "You: White" if player_color == chess.WHITE else "You: Black"
    player_label = font.render(player_text, True, PANEL_TEXT)
    screen.blit(player_label, (BOARD_WIDTH + 20, 70))

    # AI depth
    depth_label = font.render(f"AI Depth: {depth}", True, PANEL_TEXT)
    screen.blit(depth_label, (BOARD_WIDTH + 20, 110))

    # Sound toggle
    sound_text = f"Sound: {'ON' if sound_mgr.enabled else 'OFF'}"
    sound_label = small_font.render(sound_text, True, PANEL_TEXT)
    screen.blit(sound_label, (BOARD_WIDTH + 20, 160))
    s_hint = small_font.render("Press 'S' to toggle", True, PANEL_TEXT)
    screen.blit(s_hint, (BOARD_WIDTH + 20, 185))

    # ESC and M hints
    esc_label = small_font.render("ESC: Save & Menu", True, PANEL_TEXT)
    screen.blit(esc_label, (BOARD_WIDTH + 20, SCREEN_HEIGHT - 60))
    menu_label = small_font.render("M: Menu (no save)", True, PANEL_TEXT)
    screen.blit(menu_label, (BOARD_WIDTH + 20, SCREEN_HEIGHT - 35))

def run_game(screen, clock, board, depth, ai_color, player_color):
    """Main game loop with animations and sounds."""
    # Switch to game screen size
    game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Chess AI - Playing")

    selected_square = None
    ai_thinking = False
    ai_move_time = 0
    hover_square = None

    animated_moves = []
    last_time = pygame.time.get_ticks()

    sound_mgr = SoundManager()

    running = True
    while running:
        dt = (pygame.time.get_ticks() - last_time) / 1000.0
        last_time = pygame.time.get_ticks()

        # Update animations
        for anim in animated_moves[:]:
            anim.update(dt)
            if not anim.active:
                animated_moves.remove(anim)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_game(board, depth, ai_color, player_color)
                    return 'menu'
                elif event.key == pygame.K_m:
                    return 'menu'
                elif event.key == pygame.K_s:
                    sound_mgr.toggle()

            elif event.type == pygame.MOUSEMOTION:
                if not ai_thinking and board.turn != ai_color:
                    mouse_pos = (event.pos[0], event.pos[1])
                    if mouse_pos[0] < BOARD_WIDTH:
                        hover_square = get_square_from_mouse(mouse_pos, player_color)
                    else:
                        hover_square = None
                else:
                    hover_square = None

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not ai_thinking and board.turn != ai_color:
                    mouse_pos = (event.pos[0], event.pos[1])
                    if mouse_pos[0] < BOARD_WIDTH:
                        clicked_square = get_square_from_mouse(mouse_pos, player_color)
                        if clicked_square is not None:
                            clicked_piece = board.piece_at(clicked_square)

                            if selected_square is not None:
                                move = chess.Move(selected_square, clicked_square)
                                # Promotion: default to queen
                                if move in board.legal_moves:
                                    piece = board.piece_at(selected_square)
                                    if piece and piece.piece_type == chess.PAWN:
                                        to_rank = move.to_square // 8
                                        if (piece.color == chess.WHITE and to_rank == 7) or \
                                           (piece.color == chess.BLACK and to_rank == 0):
                                            move.promotion = chess.QUEEN

                                if move in board.legal_moves:
                                    # Play sound
                                    if board.is_capture(move):
                                        sound_mgr.play('capture')
                                    else:
                                        sound_mgr.play('move')

                                    # Create animation
                                    piece = board.piece_at(selected_square)
                                    anim = AnimatedPiece(piece, selected_square, move.to_square, player_color)
                                    animated_moves.append(anim)

                                    board.push(move)
                                    selected_square = None

                                    if board.is_check():
                                        sound_mgr.play('check')
                                    if board.is_game_over():
                                        sound_mgr.play('game_end')
                                else:
                                    if clicked_piece and clicked_piece.color == board.turn:
                                        selected_square = clicked_square
                                    else:
                                        selected_square = None
                            else:
                                if clicked_piece and clicked_piece.color == board.turn:
                                    selected_square = clicked_square

        # AI turn
        if not board.is_game_over() and board.turn == ai_color:
            if not ai_thinking and not animated_moves:
                ai_thinking = True
                ai_move_time = pygame.time.get_ticks() + AI_DELAY
        else:
            ai_thinking = False

        if ai_thinking and pygame.time.get_ticks() >= ai_move_time and not animated_moves:
            move = get_ai_move(board, depth)
            if move is not None:
                if board.is_capture(move):
                    sound_mgr.play('capture')
                else:
                    sound_mgr.play('move')

                piece = board.piece_at(move.from_square)
                anim = AnimatedPiece(piece, move.from_square, move.to_square, player_color)
                animated_moves.append(anim)

                board.push(move)
                if board.is_check():
                    sound_mgr.play('check')
                if board.is_game_over():
                    sound_mgr.play('game_end')

            selected_square = None
            ai_thinking = False

        # Drawing
        game_screen.fill(PANEL_BG)

        # Draw board on its own surface
        board_surface = pygame.Surface((BOARD_WIDTH, HEIGHT))
        draw_board(board_surface, hover_square, player_color)
        draw_pieces(board_surface, board, player_color, animated_moves)
        draw_check(board_surface, board, player_color)

        if selected_square is not None:
            highlight_square(board_surface, selected_square, player_color, HIGHLIGHT, 100)
            draw_move_hints(board_surface, board, selected_square, player_color, pygame.time.get_ticks())

        game_screen.blit(board_surface, (0, 0))
        draw_panel(game_screen, board, depth, ai_color, player_color, sound_mgr)

        # AI thinking message
        if ai_thinking:
            font = pygame.font.Font(None, 36)
            text = font.render("AI is thinking...", True, (0, 0, 0))
            text_rect = text.get_rect(center=(BOARD_WIDTH//2, HEIGHT//2))
            s = pygame.Surface((text_rect.width+20, text_rect.height+10), pygame.SRCALPHA)
            s.fill((255, 255, 255, 200))
            game_screen.blit(s, (text_rect.x-10, text_rect.y-5))
            game_screen.blit(text, text_rect)

        # Game over popup
        if board.is_game_over():
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            game_screen.blit(s, (0, 0))

            font = pygame.font.Font(None, 60)
            if board.is_checkmate():
                winner = "Black" if board.turn == chess.WHITE else "White"
                msg = f"Checkmate! {winner} wins."
            else:
                msg = "Stalemate!"
            text = font.render(msg, True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
            game_screen.blit(text, text_rect)

            # Buttons
            font_btn = pygame.font.Font(None, 40)
            btn_w = 120
            btn_h = 50
            new_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w - 10, SCREEN_HEIGHT//2 + 20, btn_w, btn_h)
            menu_rect = pygame.Rect(SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT//2 + 20, btn_w, btn_h)
            pygame.draw.rect(game_screen, (0, 150, 0), new_rect, border_radius=8)
            pygame.draw.rect(game_screen, (150, 0, 0), menu_rect, border_radius=8)
            new_text = font_btn.render("New", True, (255,255,255))
            menu_text = font_btn.render("Menu", True, (255,255,255))
            game_screen.blit(new_text, new_text.get_rect(center=new_rect.center))
            game_screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                mouse_pos = pygame.mouse.get_pos()
                if new_rect.collidepoint(mouse_pos):
                    return 'new'
                elif menu_rect.collidepoint(mouse_pos):
                    return 'menu'

        pygame.display.flip()
        clock.tick(FPS)

    return 'menu'