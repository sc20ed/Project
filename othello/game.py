from othello.board import Board
from othello.search import minimax, alpha_beta
from copy import deepcopy
import random
import logging

log = logging.getLogger("game.py")


# game turn 
def turn(board, p_type, depth=4, endgame=False):
    player = board.whose_turn
    opponent = player * -1
    move = None

    # select move with current player method
    if p_type == 0:
        moves = board.find_moves(player, opponent)
        if len(moves) > 0:
            move = moves[random.randint(0, len(moves)-1)]
            log.debug("Randomly selected move %s", move)

    elif p_type == 1:
        maximising = bool(player+1)
        move, score = minimax(board, depth, maximising, endgame)
        log.debug("Minimax search with depth %s selected move %s with score %d", depth, move, score)

    elif p_type == 2:
        maximising = bool(player+1)
        move, score = alpha_beta(board, depth, maximising, endgame)
        log.debug("Alpha-beta search with depth %s selected move %s with score %d", depth, move, score)

    elif p_type == 3:
        # player move selection for testing
        try:
            moves = board.find_moves(player, opponent)

            if len(moves) > 0:
                print(moves)
                choice = int(input("Select a move from the list (i.e. \'1\', \'2\' etc.): ")) - 1
                move = moves[choice]
                log.debug("Player selected move %s", move)

            else:
                print("No move available, turn passed.")

        except (ValueError, IndexError):
            print("Invalid selection. First move selected by default.")
            move = moves[0]
            log.debug("Invalid player selection, selected move %s", move)
    
    # make move or pass if none are available
    if move == (-1, -1) or move == None:
        board.advance_turn(1)
        log.debug("No move available, turn passed")
        passed = True
    else:
        board.make_move(player, opponent, move)
        log.debug("Made move")
        board.advance_turn(0)
        passed = False

    # avoid overhead if logging level is not debug
    if log.getEffectiveLevel() <= 10:
        if move in [(1, 1), (1, board.size-2),
                     (board.size-2, 1), (board.size-2, board.size-2)]:
            log.debug("Changed corresponding weight grid corner values")

        # set appropriate player and game phase heuristics and weights
        if board.whose_turn == 1:
            p_wg_score = board.wg_score[0]
            if board.move_count < int(board.max_moves/4):
                w = board.p1_weight_phases[0]
            elif board.move_count < int((board.max_moves*2)/3):
                w = board.p1_weight_phases[1]
            else:
                w = board.p1_weight_phases[2]
        else:
            p_wg_score = board.wg_score[1]
            if board.move_count < int(board.max_moves/4):
                w = board.p2_weight_phases[0]
            elif board.move_count < int((board.max_moves*2)/3):
                w = board.p2_weight_phases[1]
            else:
                w = board.p2_weight_phases[2]
    
        score = board.heuristics()
        w_disc = board.disc_difference * w[0]
        w_wg = (p_wg_score/100) * w[1] # the grid values themselves are also weights, /100 is normalization
        w_mob = (sum(board.mobility)/2) * w[2]
        w_pmob = (sum(board.p_mobility)/2) * w[3]
        w_stab = board.stability * w[4]

        log.debug("Heuristics for this turn:\n" +
              "\t\t\t\t\t\t\t\t\t         |  score\t  weight\ttotal\n"
              "\t\t\t\t\t\t\t\t\td_diff   | % -8d * % -3.2f    = % -.2f \n" +
              "\t\t\t\t\t\t\t\t\twg_score | % -8d * % -3.2f    = % -.2f\n" +
              "\t\t\t\t\t\t\t\t\tmob      | % -3d - %-3d* % -3.2f    = % -.2f\n" +
              "\t\t\t\t\t\t\t\t\tp_mob    | % -3d - %-3d* % -3.2f    = % -.2f\n" +
              "\t\t\t\t\t\t\t\t\tstab     | % -8d * % -3.2f    = % -.2f\n" +
              "\t\t\t\t\t\t\t\t\ttotal    | % -d", board.disc_difference, w[0], w_disc,
              p_wg_score, w[1], w_wg, board.mobility[0], -board.mobility[1], w[2], w_mob,
              board.p_mobility[0], -board.p_mobility[1], w[3], w_pmob, board.stability,
              w[4], w_stab, score)
        
        if endgame:
            log.debug("Endgame search, only final disc_diff considered")
    
    return passed

# run test game based on arguments
# p_type arguments represent the method used for move selection
def run_game(size=8, p1_type=0, p1_depth=0, p1_weights=None,
                  p2_type=0, p2_depth=0, p2_weights=None, n_random_moves=0):

    # initialise board representation
    board = Board(size, p1_weights, p2_weights)

    # play random starting moves
    if n_random_moves > 0:
        for i in range(n_random_moves):
            turn(board, 0, 0, False)
        log.debug("Set up board with %s random moves", n_random_moves)

        # adjust turn order
        if n_random_moves % 2 == 1:
            p1_type, p2_type = p2_type, p1_type
            p1_depth, p2_depth = p2_depth, p1_depth
            log.debug("Swapped turn order to offset odd number of random moves")

    # main game loop
    active = 1
    endgame = False
    while active == 1:
        moves_remaining = board.max_moves - board.move_count
        if moves_remaining <= 8:
            endgame = True
            p1_depth = moves_remaining
            p2_depth = moves_remaining

        log.debug("Player %s, turn %s", (board.whose_turn+3)%3, board.turn_count+1)
        p1_pass = turn(board, p1_type, p1_depth, endgame)
        if moves_remaining == 0:
            log.debug("Board full, game complete")
            break

        log.debug("Player %s, turn %s", (board.whose_turn+3)%3, board.turn_count+1)
        p2_pass = turn(board, p2_type, p2_depth, endgame)
        if moves_remaining == 0:
            log.debug("Board full, game complete")
            break
        
        if p1_pass and p2_pass:
            log.debug("Neither player can  move, game complete")
            active = 0

    return board.game_over()


# run test game based on arguments
# the board position is printed to the command line each turn
# p_type arguments represent the method used for move selection
def run_game_test(size=8, p1_type=0, p1_depth=0, p1_weights=None,
                  p2_type=0, p2_depth=0, p2_weights=None, n_random_moves=0):

    # initialise board representation
    board = Board(size, p1_weights, p2_weights)

    # play random starting moves
    if n_random_moves > 0:
        for i in range(n_random_moves):
            turn(board, 0, 0, False)
        log.debug("Set up board with %s random moves", n_random_moves)
        board.display()
        print("")

        # adjust turn order
        if n_random_moves % 2 == 1:
            p1_type, p2_type = p2_type, p1_type
            p1_depth, p2_depth = p2_depth, p1_depth
            log.debug("Swapped turn order to offset odd number of random moves")

    # main game loop
    active = 1
    endgame = False
    while active == 1:
        moves_remaining = board.max_moves - board.move_count
        if moves_remaining <= 8:
            endgame = True
            p1_depth = moves_remaining
            p2_depth = moves_remaining

        log.debug("Player %s, turn %s", (board.whose_turn+3)%3, board.turn_count+1)
        p1_pass = turn(board, p1_type, p1_depth, endgame)
        print(board.turn_count)
        board.display()
        print("")
        
        if moves_remaining == 0:
            log.debug("Board full, game complete")
            break

        log.debug("Player %s, turn %s", (board.whose_turn+3)%3, board.turn_count+1)
        p2_pass = turn(board, p2_type, p2_depth, endgame)
        print(board.turn_count)
        board.display()
        print("")

        if moves_remaining == 0:
            log.debug("Board full, game complete")
            break
        
        if p1_pass and p2_pass:
            log.debug("Neither player can  move, game complete")
            active = 0

    return board.game_over()


# run series of games based on arguments
# the board position is printed to the command line each turn
# p_type arguments represent the method used for move selection
def run_game_series(size=8, series_length=12, p1_type=0, p1_depth=0, p1_weights=None,
                  p2_type=0, p2_depth=0, p2_weights=None, n_random_moves=0):
    
    board_starts_seen = []
    series_results = []
    while series_length:

        # initialise board representation
        setup_board = Board(size)

        # play random starting moves
        if n_random_moves > 0:
            for i in range(n_random_moves):
                turn(setup_board, 0, 0, False)
            log.debug("Set up board with %s random moves", n_random_moves)
            setup_board.display()
            print("")

            # adjust turn order
            if n_random_moves % 2 == 1:
                p1_type, p2_type = p2_type, p1_type
                p1_depth, p2_depth = p2_depth, p1_depth
                log.debug("Swapped turn order to offset odd number of random moves")

        board_starting_position = setup_board.board
        if board_starting_position in board_starts_seen:
            continue
        board_starts_seen.append(board_starting_position)
        game_set_results = []
        
        # main game loop x 2, one for each player as each colour
        for i in range(2):
            board = Board(size, p1_weights, p2_weights)
            board.board = deepcopy(board_starting_position)
            
            active = 1
            endgame = False
            while active == 1:
                moves_remaining = board.max_moves - board.move_count
                if moves_remaining <= 8:
                    endgame = True
                    p1_depth = moves_remaining
                    p2_depth = moves_remaining

                log.debug("Player %s, turn %s", (board.whose_turn+3)%3, board.turn_count+1)
                p1_pass = turn(board, p1_type, p1_depth, endgame)
                print(board.turn_count)
                board.display()
                print("")
                
                if moves_remaining == 0:
                    log.debug("Board full, game complete")
                    break

                log.debug("Player %s, turn %s", (board.whose_turn+3)%3, board.turn_count+1)
                p2_pass = turn(board, p2_type, p2_depth, endgame)
                print(board.turn_count)
                board.display()
                print("")

                if moves_remaining == 0:
                    log.debug("Board full, game complete")
                    break
                
                if p1_pass and p2_pass:
                    log.debug("Neither player can  move, game complete")
                    active = 0

            winner, score = board.game_over()
            game_set_results.append([winner, score])

            # swap player colours for next game
            p1_type, p2_type = p2_type, p1_type
            p1_depth, p2_depth = p2_depth, p1_depth
            p1_weights, p2_weights = p2_weights, p1_weights

        # correct score for player colour swap
        game_set_results[1][0] = game_set_results[1][0] * -1
        corrected_game_1_score = game_set_results[1][1][1], game_set_results[1][1][0]
        game_set_results[1][1] = corrected_game_1_score
        series_results.append(game_set_results[0])
        series_results.append(game_set_results[1])
        series_length -= 1

    return series_results