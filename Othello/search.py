# functions for minimax game tree
from board import Board


# basic minimax
def minimax(board, depth, maximising):
    if depth == 0 or board.move_count >= 60:
        return None, board.heuristics()
    
    if maximising:
        score = -9999
        moves = board.find_moves(1, 2)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = minimax(board, depth-1, False)
            board.retract_turn()

            if temp_score > score:
                score = temp_score
                best_move = (-1, -1)

        for move in moves:
            board.make_move(1, 2, move)
            board.advance_turn(0)
            _, temp_score = minimax(board, depth-1, False)
            board.retract_turn()

            if temp_score > score:
                score = temp_score
                best_move = move

    else:
        score = 9999
        moves = board.find_moves(2, 1)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = minimax(board, depth-1, True)
            board.retract_turn()

            if temp_score < score:
                score = temp_score
                best_move = (-1, -1)

        for move in board.find_moves(2, 1):
            board.make_move(2, 1, move)
            board.advance_turn(0)
            _, temp_score = minimax(board, depth-1, True)
            board.retract_turn()

            if temp_score < score:
                score = temp_score
                best_move = move           

    return best_move, score


# minimax with alpha-beta pruning
def alpha_beta(board, depth, alpha, beta, maximising):
    if depth == 0 or board.move_count >= 60:
        return None, board.heuristics()
    
    if maximising:
        score = -9999
        moves = board.find_moves(1, 2)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = minimax(board, depth-1, False)
            board.retract_turn()

            if temp_score > score:
                score = temp_score
                best_move = (-1, -1)

        for move in moves:
            board.make_move(1, 2, move)
            board.advance_turn(0)
            _, temp_score = minimax(board, depth-1, False)
            board.retract_turn()

            if temp_score > score:
                score = temp_score
                best_move = move

    else:
        score = 9999
        moves = board.find_moves(2, 1)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = minimax(board, depth-1, True)
            board.retract_turn()

            if temp_score < score:
                score = temp_score
                best_move = (-1, -1)

        for move in board.find_moves(2, 1):
            board.make_move(2, 1, move)
            board.advance_turn(0)
            _, temp_score = minimax(board, depth-1, True)
            board.retract_turn()

            if temp_score < score:
                score = temp_score
                best_move = move           

    return best_move, score
