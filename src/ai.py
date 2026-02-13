import random
import chess
from settings import PIECE_VALUES

# -----------------------------------------------------------------
# Evaluation
# -----------------------------------------------------------------
def evaluate_board(board):
    """Score from White's perspective. Positive = White advantage."""
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

# -----------------------------------------------------------------
# Random move (fallback)
# -----------------------------------------------------------------
def get_random_move(board):
    try:
        return random.choice(list(board.legal_moves))
    except IndexError:
        return None

# -----------------------------------------------------------------
# Greedy (depth 1)
# -----------------------------------------------------------------
def get_greedy_move(board):
    best_move = None
    if board.turn == chess.WHITE:
        best_score = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = evaluate_board(board)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = evaluate_board(board)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
    return best_move

# -----------------------------------------------------------------
# Minimax (fixed depth)
# -----------------------------------------------------------------
def minimax(board, depth, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if maximizing:
        best_score = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            score, _ = minimax(board, depth-1, False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = float('inf')
        for move in board.legal_moves:
            board.push(move)
            score, _ = minimax(board, depth-1, True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move

def get_minimax_move(board, depth):
    maximizing = (board.turn == chess.WHITE)
    _, move = minimax(board, depth, maximizing)
    return move

# -----------------------------------------------------------------
# Alpha‑Beta (pruned minimax)
# -----------------------------------------------------------------
def alphabeta(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if maximizing:
        best_score = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            score, _ = alphabeta(board, depth-1, alpha, beta, False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        for move in board.legal_moves:
            board.push(move)
            score, _ = alphabeta(board, depth-1, alpha, beta, True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score, best_move

def get_alphabeta_move(board, depth):
    maximizing = (board.turn == chess.WHITE)
    _, move = alphabeta(board, depth, -float('inf'), float('inf'), maximizing)
    return move

# -----------------------------------------------------------------
# Unified AI move selector (depth‑aware)
# -----------------------------------------------------------------
def get_ai_move(board, depth):
    """
    Choose AI move based on search depth:
    - depth <= 0: random
    - depth == 1: greedy
    - depth == 2: minimax
    - depth >= 3: alpha‑beta
    """
    if depth <= 0:
        return get_random_move(board)
    elif depth == 1:
        return get_greedy_move(board)
    elif depth == 2:
        return get_minimax_move(board, depth)
    else:
        return get_alphabeta_move(board, depth)