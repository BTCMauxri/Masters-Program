# Opponent Agent: Monte Carlo Tree Search (MCTS)
# Architecture: Selection, Expansion, Simulation, Backpropagation

import time
import random
import math
import numpy as np
from reversi import reversi

class MCTSNode:
    """Represents a game state in the Monte Carlo search tree."""
    def __init__(self, game, move=None, parent=None, turn=1):
        self.game = game
        self.move = move
        self.parent = parent
        self.turn = turn
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = game.legal_moves(turn)
        
    def uct_select_child(self):
        """Uses the Upper Confidence Bound (UCB1) formula to balance exploration and exploitation."""
        log_visits = math.log(self.visits)
        # 1.41 (sqrt of 2) is the standard exploration parameter
        return max(self.children, key=lambda c: (c.wins / c.visits) + 1.41 * math.sqrt(log_visits / c.visits))
        
    def add_child(self, move, game_state, turn):
        """Expands the tree by adding a new game state."""
        child = MCTSNode(game_state, move=move, parent=self, turn=turn)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child
        
    def update(self, result):
        """Backpropagates the simulation result up the tree."""
        self.visits += 1
        self.wins += result

def simulate(game, turn, original_turn):
    """Plays completely random moves until the board is full to determine a winner."""
    current_turn = turn
    while True:
        moves = game.legal_moves(current_turn)
        if not moves:
            current_turn = -current_turn
            moves = game.legal_moves(current_turn)
            if not moves:
                break # Neither player has moves; game over
                
        move = random.choice(moves)
        game.step(move[0], move[1], current_turn, commit=True)
        current_turn = -current_turn
        
    # Calculate the winner of the simulation
    my_pieces = np.sum(game.board == original_turn)
    opp_pieces = np.sum(game.board == -original_turn)
    
    if my_pieces > opp_pieces: return 1
    elif my_pieces == opp_pieces: return 0.5
    else: return 0

def choose_move(board, turn, time_limit):
    """Required entry point for the Reversi client."""
    start_time = time.monotonic()
    
    root_game = reversi()
    root_game.board = board.copy()
    root = MCTSNode(root_game, turn=turn)
    
    # Failsafes for forced moves
    if not root.untried_moves: return None
    if len(root.untried_moves) == 1: return root.untried_moves[0]
        
    # Run the 4-step MCTS loop until the 4.8-second cutoff
    safe_time_limit = (time_limit - 0.2) if time_limit else 4.8
    
    while time.monotonic() - start_time < safe_time_limit:
        node = root
        
        # 1. Selection: Drill down to a node that has untried moves
        while not node.untried_moves and node.children:
            node = node.uct_select_child()
            
        # 2. Expansion: Pick one untried move and add it to the tree
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            new_game = reversi()
            new_game.board = node.game.board.copy()
            new_game.step(move[0], move[1], node.turn, commit=True)
            node = node.add_child(move, new_game, -node.turn)
            
        # 3. Simulation: Play the rest of the game out randomly
        sim_game = reversi()
        sim_game.board = node.game.board.copy()
        result = simulate(sim_game, node.turn, turn)
        
        # 4. Backpropagation: Update the win rates for the path we just took
        while node is not None:
            node.update(result)
            node = node.parent
            
    # Time is up. Return the move that the algorithm visited the most often.
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.move