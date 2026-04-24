from random import randint
from board import Board
from search import minimax, alpha_beta


# game turn 
def turn(board, p_type):
    player = board.whose_turn
    opponent = player * -1
    move = None


    # select move with current player method
    if p_type == 0:
        moves = board.find_moves(player, opponent)
        if len(moves) > 0:
            move = moves[randint(0, len(moves)-1)]

    elif p_type == 1:
        maximising = bool(player+1)
        move, score = minimax(board, 4, maximising)

    elif p_type == 2:
        maximising = bool(player+1)
        move, score = alpha_beta(board, 5, maximising)

    elif p_type == 3:
        # player move selection for testing
        try:
            moves = board.find_moves(player, opponent)

            if len(moves) > 0:
                print(moves)
                choice = int(input("Select a move from the list (i.e. \'1\', \'2\' etc.): ")) - 1
                move = moves[choice]

            else:
                print("No moves, turn passed.")

        except (ValueError, IndexError):
            print("Invalid selection. First move selected by default.")
            move = moves[0]
    
    # make move or pass if none are available
    if move == (-1, -1) or move == None:
        board.advance_turn(1)
        return 1
    else:
        board.make_move(player, opponent, (move))
        board.advance_turn(0)
        return 0


# run game based on arguments
# p_type arguments represent the method used for move selection
def run_game(size=8, p1_type=0, p2_type=0, n_random_moves=0):

    # initialise board a with set number of random moves
    board = Board(size)
    if n_random_moves > 0:
        for i in range(n_random_moves):
            turn(board, 0)
        board.display()
        print("")

    # adjust turn order
    if n_random_moves % 2 == 1:
        p1_type, p2_type = p2_type, p1_type

    # main game loop
    active = 1
    while active == 1:
        p1_pass = turn(board, p1_type)
        board.display()
        print("")
        if board.move_count >= board.max_moves:
            break

        p2_pass = turn(board, p2_type)
        board.display()
        print("")
        if board.move_count >= board.max_moves:
            break
        
        if p1_pass == 1 and p2_pass == 1:
            active = 0

    return board.game_over()