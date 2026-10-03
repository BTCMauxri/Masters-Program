"""
    Group: 7
    Group Members: Odalys, Vyshnavi, Mauricio 
    Group Project: Reversi AI Agent
    Architecture: prioritizes Iterative Deepening, Alpha-Beta Pruning and Phase-Based Heuristics.
"""

import time
import numpy as np
from reversi import reversi

# Hardcoded static matrix table, Prioritizing corners and penalizing adjacent states.
STATE_WEIGHTS = np.array([
    [ 120, -20,  20,   5,   5,  20, -20,  120],
    [-20, -40,  -5,  -5,  -5,  -5, -40,  -20],
    [  20,  -5,  15,   3,   3,  15,  -5,   20],
    [   5,  -5,   3,   3,   3,   3,  -5,    5],
    [   5,  -5,   3,   3,   3,   3,  -5,    5],
    [  20,  -5,  15,   3,   3,  15,  -5,   20],
    [-20, -40,  -5,  -5,  -5,  -5, -40,  -20],
    [ 120, -20,  20,   5,   5,  20, -20,  120]
])

""" A custom exception: Will be used when 5-sec time limit is almost reached.  """
class TimeoutException(Exception):
    pass

""" Calculates heuristic score based on the current phase of the game. """
def Assess_Board(game, turn, empty_count):

    # some attributes for team_7 and opponents
    t7_pieces = np.sum(game.board == turn)
    t7_moves = len(game.legal_moves(turn))
    opp_pieces = np.sum(game.board == -turn)
    opp_moves = len(game.legal_moves(-turn))

    # Basic Metrics
    piece_diff = t7_pieces - opp_pieces
    mobility_diff = t7_moves - opp_moves
    state_score = np.sum(game.board * STATE_WEIGHTS) * turn

    # PHASE 1: Early Game = Mostly empty space
    if empty_count > 44: 
        return (mobility_diff * 50) + (state_score * 10) + (piece_diff * -5)

    # PHASE 2: Mid Game = Board filling up
    elif empty_count > 14:
        return (state_score * 50) + (mobility_diff * 20) + (piece_diff * 10)

    # PHASE 3: Late Game = Last 14 moves
    else: return piece_diff * 100

""" Function sorts moves to evaluate good moves first. """
def Sort_Moves(game, moves, turn):

    def move_score(move):
        # row and column
        r, c = move
        return STATE_WEIGHTS[r][c]

    return sorted(moves, key=move_score, reverse=True)
        
""" Minimax algorithm with Alpha-Beta pruning & timeout protection. """
def Alpha_Beta(game, depth, alpha, beta, current_turn, t7_turn, start_time, time_limit):

    # Check clock: 4.8s hard cutoff to prevent skipped turn
    if time_limit and (time.monotonic() - start_time > time_limit - 0.2):
        raise TimeoutException()

    legal_moves = game.legal_moves(current_turn)
    empty_count = np.sum(game.board == 0)

    # Base Case: reach depth limit or game over
    if depth == 0 or empty_count == 0 or not legal_moves:
        # Neither player has moves, game is over
        if not legal_moves and not game.legal_moves(-current_turn):
            return Assess_Board(game, t7_turn, 0), None
        elif not legal_moves:
            return Alpha_Beta(game, depth - 1, alpha, beta, -current_turn, t7_turn, start_time, time_limit)[0], None

        return Assess_Board(game, t7_turn, empty_count), None

    best_move = None
    sorted_moves = Sort_Moves(game, legal_moves, current_turn)

    if current_turn == t7_turn:
        max_eval = float('-inf')
        for x, y in sorted_moves:
            # simulate move
            simulated_game = reversi()
            simulated_game.board = game.board.copy()
            simulated_game.step(x, y, current_turn, commit=True)

            eval_score, _ = Alpha_Beta(simulated_game, depth - 1, alpha, beta, -current_turn, t7_turn, start_time, time_limit)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (x, y)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break   # Beta cutoff
        return max_eval, best_move

    else:
        min_eval = float('inf')
        for x, y in sorted_moves:
            simulated_game = reversi()
            simulated_game.board = game.board.copy()
            simulated_game.step(x, y, current_turn, commit=True)

            eval_score, _ = Alpha_Beta(simulated_game, depth - 1, alpha, beta, -current_turn, t7_turn, start_time, time_limit)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (x, y)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break   # Alpha cutoff
        return min_eval, best_move

""" Entry point for the Reversi client. """
def choose_move(board, turn, time_limit):
    game = reversi()
    game.board = board.copy()
    start_time = time.monotonic()

    empty_count = np.sum(board == 0)
    legal_moves = game.legal_moves(turn)

    # Play move available if only one exists to save time
    if len(legal_moves) == 1: return legal_moves[0]

    best_move = legal_moves[0]  # default fallback

    try:
        # Iterative Deepening: Start at depth 1 and go as deep as time allows
        for depth in range(1, empty_count + 1):
            _, move = Alpha_Beta(game, depth, float('-inf'), float('inf'), turn, turn, start_time, time_limit)
            if move:
                best_move = move
                
    except TimeoutException: pass

    return best_move
