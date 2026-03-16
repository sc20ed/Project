# functions for minimax game tree
from board import Board
from copy import deepcopy
"""
class GameTree:
    def __init__(self):
        pass
"""

# basic minimax
def minimax(board, depth, maximising):
    if depth == 0 or board.turn_count >= 60:
        temp_score = board.heuristics()
        board.retract_turn()
        return None, temp_score
    
    if maximising:
        score = -9999
        moves = board.find_moves(1, 2)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = minimax(board, depth-1, False)

            if temp_score > score:
                score = temp_score
                best_move = (-1, -1)

        for move in moves:
            board.make_move(1, 2, move)
            board.advance_turn(0)
            _, temp_score = minimax(board, depth-1, False)

            if temp_score > score:
                score = temp_score
                best_move = move

    else:
        score = 9999
        moves = board.find_moves(2, 1)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = minimax(board, depth-1, True)

            if temp_score < score:
                score = temp_score
                best_move = (-1, -1)

        for move in board.find_moves(2, 1):
            board.make_move(2, 1, move)
            board.advance_turn(0)
            _, temp_score = minimax(board, depth-1, True)

            if temp_score < score:
                score = temp_score
                best_move = move

    board.retract_turn()

    return best_move, score
    

    
    # recursive function, include alphabeta later
    # if max depth, return the current heuristic
    # get possible moves
    # if there are no moves available, skip the turn
    # for each move, make the move on a copy of the board and loop the function
    # when max depth is reached, update the previous nodes
    # if it is the caller's turn, save the max if it is the highest seen so far
