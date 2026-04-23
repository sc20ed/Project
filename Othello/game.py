from random import randint
from board import Board
from search import minimax, alpha_beta


# simplified game turn
def tmp_turn(board, p_type):
    player = board.whose_turn
    opponent = player * -1
    maximising = bool(player+1)
    
    # select move with current player method
    if p_type == 0:
        moves = board.find_moves(player, opponent)
        move = moves[randint(0, len(moves)-1)]

    elif p_type == 1:
        move, score = minimax(board, 4, maximising)

    elif p_type == 2:
        move, score = alpha_beta(board, 5, maximising)

    else:
        try:
            print(moves)
            choice = int(input("Select a move from the list (i.e. \'1\', \'2\' etc.): ")) - 1
        except ValueError:
            print("Invalid selection. First move selected by default.")
            choice = 0
        move = moves[choice]
    
    # make move or pass if none are available
    if move == (-1, -1) or move == None:
        board.advance_turn(1)
        return 1
    else:
        print(move)
        board.make_move(player, opponent, (move))
        board.advance_turn(0)
        return 0


# select move (or skip if none) and complete game turn
def turn(board, move_select):
    print(board.turn_count)
    print(board.whose_turn)
    player = board.whose_turn
    opponent = player * -1
    moves = board.find_moves(player, opponent)

    if len(moves) == 0:
        return 1
    
    if move_select == 0:
        choice = randint(0, len(moves)-1)
        move = moves[choice]
    elif move_select == 1:
        choice = ("minimax")
        move, score = minimax(board, 4, True)
    elif move_select == 2:
        choice = ("alpha beta")
        move, score = alpha_beta(board, 5, False)
    else:
        choice = int(input("Select a move from the list (i.e. \'1\', \'2\' etc.): ")) - 1
        if choice > len(moves) or choice < 0:
            print("Invalid selection. First move selected by default.")
            choice = 0
        move = moves[choice]
    
    print(choice, move)
    print("")
    board.make_move(player, opponent, (move))
    board.display()

    return 0


# run game with random cpu vs ab-search
def cpu_game():
    gameboard = Board(8)
    gameboard.display()

    active = 1
    while active == 1:
        p1_can_move = turn(gameboard, 0)
        gameboard.advance_turn(p1_can_move)
        p2_can_move = turn(gameboard, 2)
        gameboard.advance_turn(p2_can_move)
        
        if p1_can_move == 1 and p2_can_move == 1:
            active = 0

    print("")
    print("GAME OVER")
    gameboard.game_over()


# run game with player vs ab-search
def player_game():
    gameboard = Board(8)
    gameboard.display()

    active = 1
    while active == 1:
        p1_can_move = turn(gameboard, 3)
        gameboard.advance_turn(p1_can_move)
        p2_can_move = turn(gameboard, 2)
        gameboard.advance_turn(p2_can_move)

        print("\nScore")
        print(gameboard.heuristics())
        print("")
        
        if p1_can_move == 1 and p2_can_move == 1:
            active = 0

    print("")
    print("GAME OVER")
    gameboard.game_over()


# run game based on arguments - p_type arguments represent the method used for move selection
def run_game(size=8, p1_type=0, p2_type=0, n_random_moves=0):

    # initialise board a with set number of random moves
    board = Board(size)
    for i in range(n_random_moves):
        turn(board, 0)

    # adjust turn order
    if n_random_moves % 2 == 1:
        p1_type, p2_type = p2_type, p1_type

    # main game loop
    active = 1
    while active == 1:
        p1_pass = tmp_turn(board, p1_type)
        board.display()
        print("")
        #if board.is_full():
        #    break

        p2_pass = tmp_turn(board, p2_type)
        board.display()
        print("")
        #if board.is_full():
        #    break
        
        if p1_pass == 1 and p2_pass == 1:
            active = 0

    print("DONE")

    #return board.game_over()