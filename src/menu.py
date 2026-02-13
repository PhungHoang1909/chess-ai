import pygame
import chess
from settings import (
    WIDTH, HEIGHT, MENU_BG, BUTTON_COLOR, BUTTON_HOVER, TEXT_COLOR, TITLE_COLOR,
    MIN_DEPTH, MAX_DEPTH, DEFAULT_DEPTH
)
from src.save_load import load_game

def draw_button(screen, text, x, y, w, h, inactive_color, active_color, action=None):
    """Draw a button with relative coordinates (x,y) as top-left."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)

    hovered = rect.collidepoint(mouse)
    color = active_color if hovered else inactive_color
    pygame.draw.rect(screen, color, rect, border_radius=8)
    if hovered:
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

    if hovered and click[0] == 1 and action is not None:
        pygame.time.wait(200)
        return True
    return False

def run_menu(screen, clock):
    """Responsive menu – all positions relative to WIDTH, HEIGHT."""
    depth = DEFAULT_DEPTH
    player_side = 'white'
    dragging = False

    # Responsive layout calculations
    title_y = int(HEIGHT * 0.1)
    label_y = int(HEIGHT * 0.22)
    slider_y = int(HEIGHT * 0.32)
    depth_text_y = int(HEIGHT * 0.42)
    side_label_y = int(HEIGHT * 0.52)
    side_btn_y = int(HEIGHT * 0.60)
    side_text_y = int(HEIGHT * 0.70)
    action_btn_y = int(HEIGHT * 0.80)

    # Slider dimensions (responsive)
    slider_w = int(WIDTH * 0.45)
    slider_h = 10
    slider_x = (WIDTH - slider_w) // 2
    handle_radius = int(WIDTH * 0.016)  # scales with window

    def set_side(side):
        nonlocal player_side
        player_side = side

    menu_running = True
    while menu_running:
        screen.fill(MENU_BG)

        # Title
        font_title = pygame.font.Font(None, int(WIDTH * 0.1))
        title = font_title.render("Chess AI", True, TITLE_COLOR)
        title_rect = title.get_rect(center=(WIDTH//2, title_y))
        screen.blit(title, title_rect)

        # Subtitle
        font_label = pygame.font.Font(None, int(WIDTH * 0.045))
        label = font_label.render("Adjust AI Strength (Search Depth)", True, TEXT_COLOR)
        screen.blit(label, (WIDTH//2 - label.get_width()//2, label_y))

        # Slider track
        pygame.draw.rect(screen, (180, 180, 180), (slider_x, slider_y, slider_w, slider_h), border_radius=5)
        pygame.draw.rect(screen, (100, 100, 100), (slider_x, slider_y, slider_w, slider_h), 2, border_radius=5)

        # Handle position
        depth_range = MAX_DEPTH - MIN_DEPTH
        handle_x = slider_x + (depth - MIN_DEPTH) * slider_w // depth_range
        handle_y = slider_y + slider_h // 2
        pygame.draw.circle(screen, BUTTON_COLOR, (handle_x, handle_y), handle_radius)
        pygame.draw.circle(screen, BUTTON_HOVER, (handle_x, handle_y), handle_radius-2)

        # Depth display
        depth_text = font_label.render(f"Depth: {depth}", True, BUTTON_COLOR)
        screen.blit(depth_text, (WIDTH//2 - depth_text.get_width()//2, depth_text_y))

        # Side selection
        label2 = font_label.render("You play as:", True, TEXT_COLOR)
        screen.blit(label2, (WIDTH//2 - label2.get_width()//2, side_label_y))

        # Button dimensions (responsive)
        btn_w = int(WIDTH * 0.18)
        btn_h = int(HEIGHT * 0.07)
        btn_spacing = int(WIDTH * 0.05)
        white_x = WIDTH//2 - btn_w - btn_spacing//2
        black_x = WIDTH//2 + btn_spacing//2

        if draw_button(screen, "White", white_x, side_btn_y, btn_w, btn_h,
                       BUTTON_COLOR, BUTTON_HOVER, action=lambda: set_side('white')):
            set_side('white')
        if draw_button(screen, "Black", black_x, side_btn_y, btn_w, btn_h,
                       BUTTON_COLOR, BUTTON_HOVER, action=lambda: set_side('black')):
            set_side('black')

        side_text = font_label.render(f"Current: {player_side.capitalize()}",
                                      True, BUTTON_COLOR)
        screen.blit(side_text, (WIDTH//2 - side_text.get_width()//2, side_text_y))

        # Action buttons (New, Load, Quit)
        action_btn_w = int(WIDTH * 0.18)
        action_btn_h = int(HEIGHT * 0.07)
        action_spacing = int(WIDTH * 0.03)
        total_width = action_btn_w * 3 + action_spacing * 2
        start_x = (WIDTH - total_width) // 2

        new_btn = draw_button(screen, "NEW GAME", start_x, action_btn_y, action_btn_w, action_btn_h,
                              (0, 150, 0), (0, 200, 0), action="new")
        load_btn = draw_button(screen, "LOAD GAME", start_x + action_btn_w + action_spacing,
                               action_btn_y, action_btn_w, action_btn_h,
                               BUTTON_COLOR, BUTTON_HOVER, action="load")
        quit_btn = draw_button(screen, "QUIT", start_x + 2*(action_btn_w + action_spacing),
                               action_btn_y, action_btn_w, action_btn_h,
                               (150, 0, 0), (200, 0, 0), action="quit")

        # Check if save exists
        saved_exists = load_game() is not None
        if not saved_exists:
            # Grey out load button
            load_rect = pygame.Rect(start_x + action_btn_w + action_spacing,
                                    action_btn_y, action_btn_w, action_btn_h)
            pygame.draw.rect(screen, (150, 150, 150), load_rect, border_radius=8)
            load_text = font_label.render("LOAD GAME", True, (100, 100, 100))
            load_text_rect = load_text.get_rect(center=load_rect.center)
            screen.blit(load_text, load_text_rect)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if click on handle
                    mouse_x, mouse_y = event.pos
                    dist = ((mouse_x - handle_x) ** 2 + (mouse_y - handle_y) ** 2) ** 0.5
                    if dist <= handle_radius + 5:
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, _ = event.pos
                    mouse_x = max(slider_x, min(slider_x + slider_w, mouse_x))
                    depth = MIN_DEPTH + (mouse_x - slider_x) * depth_range // slider_w

        # Button actions
        if new_btn:
            ai_color = chess.BLACK if player_side == 'white' else chess.WHITE
            player_color = chess.WHITE if player_side == 'white' else chess.BLACK
            return depth, ai_color, player_color, None

        if load_btn and saved_exists:
            loaded = load_game()
            if loaded:
                return loaded

        if quit_btn:
            return None

        pygame.display.flip()
        clock.tick(60)