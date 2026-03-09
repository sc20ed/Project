
# implement a faster solution later?

    # approach 1
    # ----------
    # check for free spaces
    # after each free space check if there any adjacent spaces occupied by the opponent
    # if there are, check in that direction until there is a free space, currently owned space or the edge of the board is reached
    # append the original space to the move list if currently owned space is reached

    # approach 2
    # ----------
    # check for spaces occupied by the opponent
    # check for adjacent player spaces
    # if found, check in the opposite direction until a free space is found or the edge of the board is reached
    # append the free space to the move list if found

def find_available_moves(player, opponent):
    available_moves = []
    opp_squares = []

    for i in range(8):
        for j in range(8):
            if board[i][j] == opponent:
                opp_squares.append((i, j))

    

    for target in opp_squares:
        i = target[0]
        j = target[1]

        # vertical
        try:
            if board[i+1][j] == player:
                for x in range(i-1, -1, -1):
                    if board[x][j] == 0:
                        available_moves.append((x, j))
                        break
                    elif board[x][j] == player:
                        break
        except IndexError:
            pass

        try:
            if board[i-1][j] == player:
                for x in range(i+1, 8, 1):
                    if board[x][j] == 0:
                        available_moves.append((x, j))
                        break
                    elif board[x][j] == player:
                        break
        except IndexError:
            pass

        # horizontal
        try:
            if board[i][j+1] == player:
                for y in range(j-1, -1, -1):
                    if board[i][y] == 0:
                        available_moves.append((i, y))
                        break
                    elif board[i][y] == player:
                        break
        except IndexError:
            pass

        try:
            if board[i][j-1] == player:
                for y in range(j+1, 8, 1):
                    if board[i][y] == 0:
                        available_moves.append((i, y))
                        break
                    elif board[i][y] == player:
                        break
        except IndexError:
            pass

        # diagonal
        try:
            if board[i+1][j+1] == player:
                y = j
                for x in range(i-1, -1, -1):
                    y -= 1
                    if board[x][y] == 0:
                        available_moves.append((x, y))
                        break
                    elif board[x][y] == player:
                        break
        except IndexError:
            pass

        try:
            if board[i+1][j-1] == player:
                y = j
                for x in range(i-1, -1, -1):
                    y += 1
                    if board[x][y] == 0:
                        available_moves.append((x, y))
                        break
                    elif board[x][y] == player:
                        break
        except IndexError:
            pass

        try:
            if board[i-1][j+1] == player:
                y = j
                for x in range(i+1, 8, 1):
                    y -= 1
                    if board[x][y] == 0:
                        available_moves.append((x, y))
                        break
                    elif board[x][y] == player:
                        break
        except IndexError:
            pass

        try:
            if board[i-1][j-1] == player:
                y = j
                for x in range(i+1, 8, 1):
                    y += 1
                    if board[x][y] == 0:
                        available_moves.append((x, y))
                        break
                    elif board[x][y] == player:
                        break
        except IndexError:
            pass

    return available_moves


def game_over():
    p1_total = 0
    p2_total = 0

    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                p1_total += 1
            elif board[i][j] == 2:
                p2_total += 1

    print("")
    print(p1_total)
    print(p2_total)
    print("")

    if p1_total > p2_total:
        print("\nP1 WIN")

    elif p1_total < p2_total:
        print("\nP2 WIN")

    else:
        print("\nDRAW")


def make_move(x, y, player):
    
    board[x][y] = player

    # vertical
    try:
        for i in range(x+1, 8, 1):
            if board[i][y] is not 0 or player:
                break
            else: 
                board[i][y] == player
    except IndexError:
        pass
    
    try:
        for i in range(x-1, -1, -1):
            if board[i][y] is not 0 or player:
                break
            else: 
                board[i][y] == player
    except IndexError:
        pass

    # horizontal
    try:
        for j in range(j+1, 8, 1):
            if board[x][j] is not 0 or player:
                break
            else: 
                board[x][j] == player
    except IndexError:
        pass

    try:
        for j in range(j-1, -1, -1):
            if board[x][j] is 0 or player:
                break
            else: 
                board[x][j] == player
    except IndexError:
        pass

    # diagonal
    try:
        i = x
        j = y
        while j < 8 and i < 8:
            i += 1
            j += 1
            if board[i][j] is 0 or player:
                    break
                else: 
                    board[i][j] == player
    except IndexError:
        pass

    try:
        j = y
        for i in range(x-1, -1, -1):
            j += 1
            if board[i][j] is not 0 or player:
                break
            else: 
                board[i][j] == player
    except IndexError:
        pass

    try:
        if board[i-1][j+1] == player:
            y = j
            for x in range(i+1, 8, 1):
                y -= 1
                if board[x][y] == 0:
                    available_moves.append((x, y))
                    break
                elif board[x][y] == player:
                    break
    except IndexError:
        pass

    try:
        if board[i-1][j-1] == player:
            y = j
            for x in range(i+1, 8, 1):
                y += 1
                if board[x][y] == 0:
                    available_moves.append((x, y))
                    break
                elif board[x][y] == player:
                    break
    except IndexError:
        pass


def turn(player, opponent):
    for i in range(8):
        for j in range(8):
            print(str(board[i][j]) + " ", end='')
        print("")
    print("")

    moves = find_available_moves(player, opponent)
    print("")
    print(moves)
    print("")

    if not moves:
        print("NO MOVES")
        game_over()
        return 0

    # insert selection method/algorithm
    make_move(moves[0][0]][moves[0][1], player)
    return 1


def init():
    board = []

    for i in range(8):
        row = []
        for j in range(8):
            row.append(0)

        board.append(row)

    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1


board = []

for i in range(8):
    row = []
    for j in range(8):
        row.append(0)

    board.append(row)

board[3][3] = 1
board[3][4] = 2
board[4][3] = 2
board[4][4] = 1


game_running = 1
while game_running == 1:
    game_running = turn(1, 2)
    game_running = turn(2, 1)
