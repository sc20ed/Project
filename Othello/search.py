# basic minimax
def minimax(board, depth, maximising):
    if depth == 0 or board.move_count >= 60:
        return None, board.heuristics()
    
    # MAX PLAYER
    if maximising:
        score = -999999
        moves = board.find_moves(1, -1)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = minimax(board, depth-1, False)
            board.retract_turn()

            if temp_score > score:
                score = temp_score
                best_move = (-1, -1)

        for move in moves:
            board.make_move(1, -1, move)
            board.advance_turn(0)
            _, temp_score = minimax(board, depth-1, False)
            board.retract_turn()

            if temp_score > score:
                score = temp_score
                best_move = move

    # MIN PLAYER
    else:
        score = 999999
        moves = board.find_moves(-1, 1)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = minimax(board, depth-1, True)
            board.retract_turn()

            if temp_score < score:
                score = temp_score
                best_move = (-1, -1)

        for move in moves:
            board.make_move(-1, 1, move)
            board.advance_turn(0)
            _, temp_score = minimax(board, depth-1, True)
            board.retract_turn()

            if temp_score < score:
                score = temp_score
                best_move = move           

    return best_move, score


# minimax with alpha-beta pruning
def alpha_beta(board, depth, maximising, alpha=-999999, beta=999999):
    if depth == 0 or board.move_count >= 60:
        return None, board.heuristics()
    
    # MAX PLAYER
    if maximising:
        score = -999999
        moves = board.find_moves(1, -1)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = alpha_beta(board, depth-1, False, alpha, beta)
            board.retract_turn()

            if temp_score > score:
                score = temp_score
                best_move = (-1, -1)

            alpha = max(alpha, score)

        for move in moves:
            board.make_move(1, -1, move)
            board.advance_turn(0)
            _, temp_score = alpha_beta(board, depth-1, False, alpha, beta)
            board.retract_turn()

            if temp_score > score:
                score = temp_score
                best_move = move

            # stop evaluating subtree if a move guarantees it won't be chosen by MIN
            if score >= beta:
                break

            alpha = max(alpha, score)

    # MIN PLAYER
    else:
        score = 999999
        moves = board.find_moves(-1, 1)

        if len(moves) == 0:
            board.advance_turn(1)
            _, temp_score = alpha_beta(board, depth-1, True, alpha, beta)
            board.retract_turn()

            if temp_score < score:
                score = temp_score
                best_move = (-1, -1)

            beta = min(beta, score)

        for move in moves:
            board.make_move(-1, 1, move)
            board.advance_turn(0)
            _, temp_score = alpha_beta(board, depth-1, True, alpha, beta)
            board.retract_turn()

            if temp_score <= score:
                score = temp_score
                best_move = move

            # stop evaluating subtree if a move guarantees it won't be chosen by MAX
            if score < alpha:
                break

            beta = min(beta, score)

    return best_move, score
