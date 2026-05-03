import logging

log = logging.getLogger("board.py")


# object to handle current board, game state and heuristics
class Board:
    def __init__(self, size=8):
        self.board = []
        self.weight_grid = []
        self.unmake_list = []
        self.size = size + 2
        self.max_moves = (size*size) - 4
        self.move_count = 0
        self.turn_count = 0
        self.whose_turn = 1
        self.square_difference = 0
        self.wg_score = 0
        self.mobility = [0, 0]
        self.p_mobility = [0, 0]
        self.weights = []

        midpoint = int(self.size/2)
        self.setup_board(midpoint)

        # get weights for heuristics. move later?
        with open(file="weight_list.txt", mode='r', encoding="utf-8") as wl:
            next(wl)
            self.weights = [int(weight) for weight in wl.readline().strip('\n').split(',')]
        
        self.init_weight_grid()
        if self.size > 6:
            self.setup_weight_grid(self.weights, midpoint)
        else:
            self.setup_weight_grid_simple(self.weights, midpoint)
    

    # create initial game position
    def setup_board(self, midpoint):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            self.board.append(row)

        for i, j in [(midpoint-1, midpoint-1), (midpoint-1, midpoint),
                     (midpoint, midpoint-1), (midpoint, midpoint)]:
            if i == j:
                self.board[i][j] = 1
            else:
                self.board[i][j] = -1

    
    # initialise weighted squares grid to correct size
    def init_weight_grid(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            self.weight_grid.append(row)


    # create weighted squares grid for current board
    def setup_weight_grid(self, weights, midpoint):
        size = self.size # for readability            

        # weights are laid out by index as follows:
        # 0
        # 1 2
        # 3 4 5
        # 6 7 8 9
        # and are then used to fill out the board symmetrically

        # for board sizes larger than 8 the following extension applies:
        # 6 7 8 5
        # 6 7 8 8 5
        # 6 7 8 8 8 5
        # . . . . . . .
        # 6 7 8 8 8 8 8 9
        # this ensures some function of the weighted squares grid for any board size

        # set up squares on main diagonals (4 instances each)
        for x in range(1, 4 + int((size-10)/2)):
            if x < 3:
                if x == 1:
                    weight_value = weights[0]
                elif x == 2:
                    weight_value = weights[2]

            else:
                weight_value = weights[5]
        
            for i, j in [(x, x), (x, size-(x+1)), (size-(x+1), x), (size-(x+1), size-(x+1))]:
                self.weight_grid[i][j] = weight_value

        # set up squares on edges (8 instances each)
        for x in range(2, 5 + int((size-10)/2)):
            if x < 4:
                if x == 2:
                    weight_value = weights[1]
                else:
                    weight_value = weights[3]
            else:
                weight_value = weights[6]

            for i, j in [(1, x), (1, size-(x+1)), (x, 1), (x, size-2),
                     (size-(x+1), 1), (size-(x+1), size-2), (size-2, x), (size-2, size-(x+1))]:
                self.weight_grid[i][j] = weight_value

        # set up squares not on main diagonals or edges (8 instances each)
        for x in range(2, 4 + int((size-10)/2)):
            if x == 2:
                for y in range(x+1, 5 + int((size-10)/2)):
                    for i, j in [(x, y), (x, size-(y+1)), (y, x), (y, size-(x+1)),
                                 (size-(y+1), x), (size-(y+1), size-(x+1)),
                                 (size-(x+1), y), (size-(x+1), size-(y+1))]:
                        if y == 3:
                            self.weight_grid[i][j] = weights[4]
                        else:
                            self.weight_grid[i][j] = weights[7]

            else:
                for y in range(x+1, 5 + int((size-10)/2)):
                    for i, j in [(x, y), (x, size-(y+1)), (y, x), (y, size-(x+1)),
                                 (size-(y+1), x), (size-(y+1), size-(x+1)),
                                 (size-(x+1), y), (size-(x+1), size-(y+1))]:
                        self.weight_grid[i][j] = weights[8]
                    
        # set up squares around midpoint
        for i, j in [(midpoint-1, midpoint-1), (midpoint-1, midpoint),
                     (midpoint, midpoint-1), (midpoint, midpoint)]:
            self.weight_grid[i][j] = weights[9]


    # create simple weighted square heuristic for boards smaller than 7x7
    def setup_weight_grid_simple(self, weights, midpoint):
        size = self.size # for readability

        # see previous function for weight grid structure explanation
        # set in order of danger squares, then corners, then centre
        # so that accuracy is preserved where it is most important

        for i, j in [(1, 2), (1, size-3), (2, 1), (2, size-2),
                     (size-3, 1), (size-3, size-2), (size-2, 2), (size-2, size-3)]:
                self.weight_grid[i][j] = int(weights[1])

        for i, j in [(2, 2), (2, size-3), (size-3, 2), (size-3, size-3)]:
            self.weight_grid[i][j] = int(weights[2])

        for i, j in [(1, 1), (1, size-2), (size-2, 1), (size-2, size-2)]:
                self.weight_grid[i][j] = int(weights[0])

        for i, j in [(midpoint-1, midpoint-1), (midpoint-1, midpoint),
                     (midpoint, midpoint-1), (midpoint, midpoint)]:
                self.weight_grid[i][j] = int(weights[9])


    # reset board and values
    def reset(self):
        self.board = []
        self.unmake_list = []
        self.move_count = 0
        self.turn_count = 0
        self.whose_turn = 1
        self.square_difference = 0
        self.wg_score = 0
        self.mobility = [0, 0]
        self.p_mobility = [0, 0]

        midpoint = int(self.size/2)
        self.setup_board(midpoint)


    # print board to terminal
    def display(self):
        for j in range(1, self.size-1):
            for i in range(1, self.size-1):
                if self.board[i][j] == 0:
                    print("." + " ", end='')
                elif self.board[i][j] == 1:
                    print("X" + " ", end='')
                elif self.board[i][j] == -1:
                    print("O" + " ", end='')
                else:
                    print(str(self.board[i][j]) + " ", end='')
                    log.error("Invalid board character %s at [%d][%d]", str(self.board[i][j]), i, j)
            print("")

    # update turn count and current player
    def advance_turn(self, passed):
        if not passed:
            self.move_count += 1
        else:
            self.unmake_list.append([self.square_difference, -1])

        self.turn_count += 1
        self.whose_turn *= -1


    # revert to previous turn and heuristics 
    def retract_turn(self):
        prev_turn = self.unmake_list.pop()
        self.turn_count -= 1

        if prev_turn[1] == -1:
            self.whose_turn *= -1
            return
        
        self.square_difference = prev_turn.pop(0)
        self.wg_score = prev_turn.pop(0)
        prev_move = prev_turn.pop(0)
        self.board[prev_move[0]][prev_move[1]] = 0

        for i, j in prev_turn:
            self.board[i][j] = self.whose_turn

        self.move_count -= 1
        self.whose_turn *= -1


    # find frontier by checking the entire board, and update p_mobility
    def find_frontier(self, opponent):
        frontier = []
        p_index = (self.whose_turn+2)%3
        self.p_mobility[p_index] = 0

        # adds a square to the frontier if it is adjacent to an opponents disc,
        # then increments p_mobility if the square is not only adjacent to an edge disc
        for i in range(1, self.size-1):
            for j in range(1, self.size-1):
                if self.board[i][j] == 0:
                    solely_from_edge = True

                    for x, y in [(i, j+1), (i,j-1), (i+1, j), (i-1, j),
                                 (i+1, j+1), (i+1, j-1), (i-1, j+1), (i-1, j-1)]:
                        if self.board[x][y] == opponent:
                            frontier.append((i, j))

                            if i not in [2,7] and j not in [2, 7]:
                                solely_from_edge = False
                                break

                            else:
                                if x not in [1, 8] and y not in [1, 8]:
                                    solely_from_edge = False
                                    break

                    if not solely_from_edge:
                        self.p_mobility[p_index] += self.whose_turn

        return frontier
    
    
    # check if frontier squares are valid moves
    def validate_move(self, player, opponent, square):
        x = square[0]
        y = square[1]

        # for each direction if there is an opponent continue checking adjacent squares
        # if a player square is reached before an empty or edge then move is valid

        # horizontal
        if self.board[x+1][y] == opponent:
            for i in range(x+2, self.size-1, 1):
                if self.board[i][y] == opponent:
                    pass
                elif self.board[i][y] == player:
                    return True
                else:
                    break
                    
        if self.board[x-1][y] == opponent:
            for i in range(x-2, 0, -1):
                if self.board[i][y] == opponent:
                    pass
                elif self.board[i][y] == player:
                    return True
                else:
                    break

        # vertical
        if self.board[x][y+1] == opponent:
            for j in range(y+2, self.size-1, 1):
                if self.board[x][j] == opponent:
                    pass
                elif self.board[x][j] == player:
                    return True
                else:
                    break

        if self.board[x][y-1] == opponent:
            for j in range(y-2, 0, -1):
                if self.board[x][j] == opponent:
                    pass
                elif self.board[x][j] == player:
                    return True
                else:
                    break

        # diagonal
        if self.board[x+1][y+1] == opponent:
            for i, j in zip(range(x+2, self.size-1, 1), range(y+2, self.size-1, 1)):
                if self.board[i][j] == opponent:
                    pass
                elif self.board[i][j] == player:
                    return True
                else:
                    break
                    
        if self.board[x-1][y+1] == opponent:
            for i, j in zip(range(x-2, 0, -1), range(y+2, self.size-1, 1)):
                if self.board[i][j] == opponent:
                    pass
                elif self.board[i][j] == player:
                    return True
                else:
                    break

        if self.board[x+1][y-1] == opponent:
            for i, j in zip(range(x+2, self.size-1, 1), range(y-2, 0, -1)):
                if self.board[i][j] == opponent:
                    pass
                elif self.board[i][j] == player:
                    return True
                else:
                    break

        if self.board[x-1][y-1] == opponent:
            for i, j in zip(range(x-2, 0, -1), range(y-2, 0, -1)):
                if self.board[i][j] == opponent:
                    pass
                elif self.board[i][j] == player:
                    return True
                else:
                    break

        return False

    
    # check what legal moves are available and update mobility
    def find_moves(self, player, opponent):
        frontier = self.find_frontier(opponent)
        moves = []
        
        for square in frontier:
            if (self.validate_move(player, opponent, square)):
                moves.append(square)

        p_index = (self.whose_turn+2)%3
        self.mobility[p_index] = len(moves)   

        return moves


    # find and enact consequences of making chosen move
    def make_move(self, player, opponent, move):
        x = move[0]
        y = move[1]
        flip_squares = []

        # for each direction if there is an opponent continue checking adjacent squares
        # if a player square is reached before an empty or edge then add all squares checked to flip list

        # horizontal
        if self.board[x+1][y] == opponent:
            flip_line = []
            flip_line.append((x+1, y))
            for i in range(x+2, self.size-1, 1):
                if self.board[i][y] == opponent:
                    flip_line.append((i, y))
                elif self.board[i][y] == player:
                    flip_squares.append(flip_line)
                    break
                else:
                    break
                    
        if self.board[x-1][y] == opponent:
            flip_line = []
            flip_line.append((x-1, y))
            for i in range(x-2, 0, -1):
                if self.board[i][y] == opponent:
                    flip_line.append((i, y))
                elif self.board[i][y] == player:
                    flip_squares.append(flip_line)
                    break
                else:
                    break

        # vertical
        if self.board[x][y+1] == opponent:
            flip_line = []
            flip_line.append((x, y+1))
            for j in range(y+2, self.size-1, 1):
                if self.board[x][j] == opponent:
                    flip_line.append((x, j))
                elif self.board[x][j] == player:
                    flip_squares.append(flip_line)
                    break
                else:
                    break

        if self.board[x][y-1] == opponent:
            flip_line = []
            flip_line.append((x, y-1))
            for j in range(y-2, 0, -1):
                if self.board[x][j] == opponent:
                    flip_line.append((x, j))
                elif self.board[x][j] == player:
                    flip_squares.append(flip_line)
                    break
                else:
                    break

        # diagonal
        if self.board[x+1][y+1] == opponent:
            flip_line = []
            flip_line.append((x+1, y+1))
            for i, j in zip(range(x+2, self.size-1, 1), range(y+2, self.size-1, 1)):
                if self.board[i][j] == opponent:
                    flip_line.append((i, j))
                elif self.board[i][j] == player:
                    flip_squares.append(flip_line)
                    break
                else:
                    break
                    
        if self.board[x-1][y+1] == opponent:
            flip_line = []
            flip_line.append((x-1, y+1))
            for i, j in zip(range(x-2, 0, -1), range(y+2, self.size-1, 1)):
                if self.board[i][j] == opponent:
                    flip_line.append((i, j))
                elif self.board[i][j] == player:
                    flip_squares.append(flip_line)
                    break
                else:
                    break

        if self.board[x+1][y-1] == opponent:
            flip_line = []
            flip_line.append((x+1, y-1))
            for i, j in zip(range(x+2, self.size-1, 1), range(y-2, 0, -1)):
                if self.board[i][j] == opponent:
                    flip_line.append((i, j))
                elif self.board[i][j] == player:
                    flip_squares.append(flip_line)
                    break
                else:
                    break

        if self.board[x-1][y-1] == opponent:
            flip_line = []
            flip_line.append((x-1, y-1))
            for i, j in zip(range(x-2, 0, -1), range(y-2, 0, -1)):
                if self.board[i][j] == opponent:
                    flip_line.append((i, j))
                elif self.board[i][j] == player:
                    flip_squares.append(flip_line)
                    break
                else:
                    break

        self.flip(player, move, flip_squares)


    # flip squares captured by chosen move, update heuristics and record changes for unmake list
    def flip(self, player, move, squares):
        turn_change = [self.square_difference, self.wg_score, move]

        self.board[move[0]][move[1]] = player
        self.square_difference += player
        self.wg_score += self.weight_grid[move[0]][move[1]] * player

        for line in squares:
            for square in line:
                turn_change.append(square)
                self.board[square[0]][square[1]] = player
                self.square_difference += (player*2)
                self.wg_score += self.weight_grid[move[0]][move[1]] * player            

        self.unmake_list.append(turn_change)


    # end game and determine winner and score
    def game_over(self):
        p1_total = 0
        p2_total = 0

        for i in range(1, self.size-1):
            for j in range(1, self.size-1):
                if self.board[i][j] == 1:
                    p1_total += 1
                elif self.board[i][j] == -1:
                    p2_total += 1

        if p1_total > p2_total:
            winner = 1
        elif p2_total > p1_total:
            winner = -1
        else:
            winner = 0

        return winner, (p1_total, p2_total)
        

    # evaluation function
    def heuristics(self):
        score = int(self.square_difference +
                     (self.wg_score/50) +
                     sum(self.p_mobility) +
                     sum(self.mobility))

        return score