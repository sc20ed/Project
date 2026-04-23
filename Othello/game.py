from random import randint
from board import Board
from search import minimax, alpha_beta


# select move (or skip if none) and complete game turn
def turn(board, move_select):
    print(board.turn_count)
    player = board.whose_turn
    opponent = (board.whose_turn*2) % 3
    moves = board.find_moves(player, opponent)

    if len(moves) == 0:
        return 1
    
    if move_select == 0:
        choice = randint(0, len(moves)-1)
        move = moves[choice]
    elif move_select == 1:
        choice = ("minimax")
        move, score = minimax(board, 4, True)
        print(score)
    elif move_select == 2:
        choice = ("alpha beta")
        move, score = alpha_beta(board, 5, False)
        print(score)
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
