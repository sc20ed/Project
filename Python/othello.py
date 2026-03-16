from random import randint
from board import Board
from minimax import minimax


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
        move, _ = minimax(board, 4, True)
    elif move_select == 2:
        choice = ("minimax")
        move, _ = minimax(board, 4, False)
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
    print("")

    return 0


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


def player_game():
    gameboard = Board(8)
    gameboard.display()

    active = 1
    while active == 1:
        p1_can_move = turn(gameboard, 3)
        gameboard.advance_turn(p1_can_move)
        p2_can_move = turn(gameboard, 2)
        gameboard.advance_turn(p2_can_move)
        
        if p1_can_move == 1 and p2_can_move == 1:
            active = 0

    print("")
    print("GAME OVER")
    gameboard.game_over()


#################################################
# CLI for initiating cpu or player vs cpu games #
#################################################

if __name__ == "__main__":

    option = None
    while option != 3:
        print("\n1: CPU vs CPU game\n2: Player vs CPU game\n3: exit")
        option = int(input("Select an option: "))

        if option == 1:
            cpu_game()

        elif option == 2:
            player_game()

        elif option == 3:
            pass

        else:
            print("\nInvalid option.")


    # test code for full board with padding    
    """
    for j in range(gameboard.size):
        for i in range(gameboard.size):
            print(str(gameboard.board[i][j]) + " ", end='')
        print("")
    print("")
    """