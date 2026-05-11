from collections import deque
import logging

log = logging.getLogger("board.py")


# object to handle current board, game state and heuristics
class Board:
    def __init__(self, size=8, p1_weights=None, p2_weights=None):
        if p1_weights == None:
            p1_weights = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                          [0.5, 1, 2, 1, 1], [0.5, 1, 2, 1, 1], [0.5, 1, 2, 1, 1]]
        if p2_weights == None:
            p2_weights = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                          [0.5, 1, 2, 1, 1], [0.5, 1, 2, 1, 1], [0.5, 1, 2, 1, 1]]

        self.board = []
        self.unmake_list = []
        self.size = size + 2
        self.max_moves = (size*size) - 4
        self.move_count = 0
        self.turn_count = 0
        self.whose_turn = 1
        self.disc_difference = 0
        self.mobility = [0, 0]
        self.p_mobility = [0, 0]
        self.stability = 0
        self.wg_score = [0, 0]
        self.p1_weight_grid = []
        self.p1_grid_weights = p1_weights[0]
        self.p1_weight_phases = p1_weights[1:]
        self.p2_weight_grid = []
        self.p2_grid_weights = p2_weights[0]
        self.p2_weight_phases = p2_weights[1:]

        midpoint = int(self.size/2)
        self.setup_board(midpoint)            
        
        self.init_weight_grids()
        if self.size > 6:
            self.setup_weight_grid(self.p1_weight_grid, self.p1_grid_weights, midpoint)
            self.setup_weight_grid(self.p2_weight_grid, self.p2_grid_weights, midpoint)
        else:
            self.setup_weight_grid_simple(self.p1_weight_grid, self.p1_grid_weights, midpoint)
            self.setup_weight_grid_simple(self.p2_weight_grid, self.p2_grid_weights, midpoint)
    

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
    def init_weight_grids(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            self.p1_weight_grid.append(row)
            self.p2_weight_grid.append(row)


    # create weighted squares grid for current board
    def setup_weight_grid(self, weight_grid, grid_weights, midpoint):
        size = self.size # for readability            

        # grid_weights are laid out by index as follows:
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
                    weight_value = grid_weights[0]
                elif x == 2:
                    weight_value = grid_weights[2]

            else:
                weight_value = grid_weights[5]
        
            for i, j in [(x, x), (x, size-(x+1)), (size-(x+1), x), (size-(x+1), size-(x+1))]:
                weight_grid[i][j] = weight_value

        # set up squares on edges (8 instances each)
        for x in range(2, 5 + int((size-10)/2)):
            if x < 4:
                if x == 2:
                    weight_value = grid_weights[1]
                else:
                    weight_value = grid_weights[3]
            else:
                weight_value = grid_weights[6]

            for i, j in [(1, x), (1, size-(x+1)), (x, 1), (x, size-2),
                     (size-(x+1), 1), (size-(x+1), size-2), (size-2, x), (size-2, size-(x+1))]:
                weight_grid[i][j] = weight_value

        # set up squares not on main diagonals or edges (8 instances each)
        for x in range(2, 4 + int((size-10)/2)):
            if x == 2:
                for y in range(x+1, 5 + int((size-10)/2)):
                    for i, j in [(x, y), (x, size-(y+1)), (y, x), (y, size-(x+1)),
                                 (size-(y+1), x), (size-(y+1), size-(x+1)),
                                 (size-(x+1), y), (size-(x+1), size-(y+1))]:
                        if y == 3:
                            weight_grid[i][j] = grid_weights[4]
                        else:
                            weight_grid[i][j] = grid_weights[7]

            else:
                for y in range(x+1, 5 + int((size-10)/2)):
                    for i, j in [(x, y), (x, size-(y+1)), (y, x), (y, size-(x+1)),
                                 (size-(y+1), x), (size-(y+1), size-(x+1)),
                                 (size-(x+1), y), (size-(x+1), size-(y+1))]:
                        weight_grid[i][j] = grid_weights[8]
                    
        # set up squares around midpoint
        for i, j in [(midpoint-1, midpoint-1), (midpoint-1, midpoint),
                     (midpoint, midpoint-1), (midpoint, midpoint)]:
            weight_grid[i][j] = grid_weights[9]


    # create simple weighted square heuristic for boards smaller than 7x7
    def setup_weight_grid_simple(self, weight_grid, grid_weights, midpoint):
        size = self.size # for readability

        # see previous function for weight grid structure explanation
        # set in order of danger squares, then corners, then centre
        # so that accuracy is preserved where it is most important

        for i, j in [(1, 2), (1, size-3), (2, 1), (2, size-2),
                     (size-3, 1), (size-3, size-2), (size-2, 2), (size-2, size-3)]:
                weight_grid[i][j] = grid_weights[1]

        for i, j in [(2, 2), (2, size-3), (size-3, 2), (size-3, size-3)]:
            weight_grid[i][j] = grid_weights[2]

        for i, j in [(1, 1), (1, size-2), (size-2, 1), (size-2, size-2)]:
                weight_grid[i][j] = grid_weights[0]

        for i, j in [(midpoint-1, midpoint-1), (midpoint-1, midpoint),
                     (midpoint, midpoint-1), (midpoint, midpoint)]:
                weight_grid[i][j] = grid_weights[9]


    # if corner has been captured update weight grid adjacent to corner    
    def weight_grid_corner_change(self, move):
        wg_change = []
        
        # update the 3 grid_weights adjacent to the given corner directly
        # and corrects the weighted squares heuristic accordingly
        # (it is faster and simpler to do this with if statements)
        if move == (1, 1):
            for i, j in [(1, 2), (2, 1), (2, 2)]:
                s_player =  self.board[i][j]
                self.wg_score[0] -= self.p1_weight_grid[i][j] * s_player
                self.wg_score[1] -= self.p2_weight_grid[i][j] * s_player
                wg_change.append((i, j))

                if (i, j) == (2, 2):
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[2] / -4
                    self.wg_score[0] += self.p1_weight_grid[i][j] * s_player
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[2] / -4
                    self.wg_score[1] += self.p2_weight_grid[i][j] * s_player
                else:
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[1] * -1
                    self.wg_score[0] += self.p1_weight_grid[i][j] * s_player
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[1] * -1
                    self.wg_score[1] += self.p2_weight_grid[i][j] * s_player

        elif move == (1, self.size-2):
            for i, j in [(1, self.size-3), (2, self.size-3), (2, self.size-2)]:
                s_player =  self.board[i][j]
                self.wg_score[0] -= self.p1_weight_grid[i][j] * s_player
                self.wg_score[1] -= self.p2_weight_grid[i][j] * s_player
                wg_change.append((i, j))

                if (i, j) == (2, self.size-3):
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[2] / -4
                    self.wg_score[0] += self.p1_weight_grid[i][j] * s_player
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[2] / -4
                    self.wg_score[1] += self.p2_weight_grid[i][j] * s_player
                else:
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[1] * -1
                    self.wg_score[0] += self.p1_weight_grid[i][j] * s_player
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[1] * -1
                    self.wg_score[1] += self.p2_weight_grid[i][j] * s_player

        elif move == (self.size-2, 1):
            for i, j in [(self.size-3, 1), (self.size-3, 2), (self.size-2, 2)]:
                s_player =  self.board[i][j]
                self.wg_score[0] -= self.p1_weight_grid[i][j] * s_player
                self.wg_score[1] -= self.p2_weight_grid[i][j] * s_player
                wg_change.append((i, j))

                if (i, j) == (self.size-3, 2):
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[2] / -4
                    self.wg_score[0] += self.p1_weight_grid[i][j] * s_player
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[2] / -4
                    self.wg_score[1] += self.p2_weight_grid[i][j] * s_player
                else:
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[1] * -1
                    self.wg_score[0] += self.p1_weight_grid[i][j] * s_player
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[1] * -1
                    self.wg_score[1] += self.p2_weight_grid[i][j] * s_player

        elif move == (self.size-2, self.size-2):
            for i, j in [(self.size-3, self.size-3), (self.size-3, self.size-2), (self.size-2, self.size-3)]:
                s_player =  self.board[i][j]
                self.wg_score[0] -= self.p1_weight_grid[i][j] * s_player
                self.wg_score[1] -= self.p2_weight_grid[i][j] * s_player
                wg_change.append((i, j))

                if (i, j) == (self.size-3, self.size-3):
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[2] / -4
                    self.wg_score[0] += self.p1_weight_grid[i][j] * s_player
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[2] / -4
                    self.wg_score[1] += self.p2_weight_grid[i][j] * s_player
                else:
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[1] * -1
                    self.wg_score[0] += self.p1_weight_grid[i][j] * s_player
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[1] * -1
                    self.wg_score[1] += self.p2_weight_grid[i][j] * s_player

        return wg_change


    # reset board and values
    def reset(self):
        self.board = []
        self.unmake_list = []
        self.move_count = 0
        self.turn_count = 0
        self.whose_turn = 1
        self.disc_difference = 0
        self.mobility = [0, 0]
        self.p_mobility = [0, 0]
        self.stability = 0
        self.wg_score = [0, 0]

        midpoint = int(self.size/2)
        self.setup_board(midpoint)

        if self.size > 6:
            self.setup_weight_grid(self.p1_weight_grid, self.p1_grid_weights, midpoint)
            self.setup_weight_grid(self.p2_weight_grid, self.p2_grid_weights, midpoint)
        else:
            self.setup_weight_grid_simple(self.p1_weight_grid, self.p1_grid_weights, midpoint)
            self.setup_weight_grid_simple(self.p2_weight_grid, self.p2_grid_weights, midpoint)


    # print board to terminal flipped to traditional orientation
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
            self.unmake_list.append([self.disc_difference, 'p'])

        self.turn_count += 1
        self.whose_turn *= -1


    # revert to previous turn and heuristics 
    def retract_turn(self):
        prev_turn = self.unmake_list.pop()
        self.turn_count -= 1

        if prev_turn[1] == 'p':
            self.whose_turn *= -1
            return
        
        self.disc_difference = prev_turn.popleft()
        self.wg_score = prev_turn.popleft()
        wg_change = prev_turn.popleft()
        if wg_change:
            for i, j in wg_change:
                if (i, j) in [(2, 2), (2, self.size-3), (self.size-3, 2), (self.size-3, self.size-3)]:
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[2]
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[2]
                else:
                    self.p1_weight_grid[i][j] = self.p1_grid_weights[1]
                    self.p2_weight_grid[i][j] = self.p2_grid_weights[1]

        self.mobility = prev_turn.popleft()
        self.p_mobility = prev_turn.popleft()
        prev_move = prev_turn.popleft()
        self.board[prev_move[0]][prev_move[1]] = 0

        while prev_turn:
            i, j = prev_turn.popleft()
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

        p_index = (player+2)%3
        self.mobility[p_index] = len(moves) * player

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

        # use the correct weight grid and score
        self.flip(player, move, flip_squares)


    # flip squares captured by chosen move, update heuristics and record changes for unmake list
    def flip(self, player, move, squares):
        turn_change = deque()
        turn_change.extend([self.disc_difference, [self.wg_score[0], self.wg_score[1]]])
        wg_change = self.weight_grid_corner_change(move)
        turn_change.extend([wg_change, [self.mobility[0], self.mobility[1]],
                            [self.p_mobility[0], self.p_mobility[1]], (move)])

        self.board[move[0]][move[1]] = player
        self.disc_difference += player
        self.wg_score[0] += self.p1_weight_grid[move[0]][move[1]] * player
        self.wg_score[1] += self.p2_weight_grid[move[0]][move[1]] * player

        for line in squares:
            for square in line:
                turn_change.append(square)
                self.board[square[0]][square[1]] = player
                self.disc_difference += (player*2)
                self.wg_score[0] += self.p1_weight_grid[square[0]][square[1]] * (player*2)
                self.wg_score[1] += self.p2_weight_grid[square[0]][square[1]] * (player*2)

        self.unmake_list.append(turn_change)


    # update stability from discs around current position
    def find_stable_group(self, checked, player, p_stability, square):
        # for each adjacent player square check if it has at least one stable neighour
        # on each of the possible directions that it could be attacked

        # check if queued squares are stable and add adjacent squares to queue
        adj_queue = deque()
        adj_queue.append(square)
        checked[square[0]][square[1]] = True
        while adj_queue:
            i, j = adj_queue.popleft()

            # check if square is stable
            opposite_adj_pairs = [((i, j+1), (i,j-1)), ((i+1, j), (i-1, j)),
                           ((i+1, j+1), (i-1, j-1)), ((i-1, j+1), (i+1, j-1))]
            vuln_directions = 4
            for a, b in opposite_adj_pairs:
                if p_stability[a[0]][a[1]] or p_stability[b[0]][b[1]]:
                    vuln_directions -= 1

                if not vuln_directions:
                    p_stability[i][j] = True
                    self.stability += player

                    # if stable, queue adjacent squares
                    for a, b in opposite_adj_pairs[:2]:
                        if not checked[a[0]][a[1]] and self.board[a[0]][a[1]] == player:
                            checked[a[0]][a[1]] = True
                            adj_queue.append((a[0], a[1]))
                        elif not checked[b[0]][b[1]] and self.board[b[0]][b[1]] == player:
                            checked[b[0]][b[1]] = True
                            adj_queue.append((b[0], b[1]))


    # calculate the stability heuristic
    def update_stability(self):
        self.stability = 0
        p1_stability = []
        p2_stability = []
        checked = []

        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == 0 or j == 0 or i == self.size-1 or j == self.size-1:
                    row.append(True)
                else:
                    row.append(False)
            checked.append(row)
            p1_stability.append(row)
            p2_stability.append(row)

        # start from each corner and update stability for the occupying player
        for i, j in [(1, 1), (1, self.size-2), (self.size-2, 1), (self.size-2, self.size-2)]:
                if self.board[i][j] != 0 and not checked[i][j]:
                    if self.board[i][j] == 1:
                        self.find_stable_group(checked, 1, p1_stability, (i, j))
                    else:
                        self.find_stable_group(checked, -1, p2_stability, (i, j))


    # evaluation function
    def heuristics(self):
        # select appropriate player and game phase heuristics and weights
        if self.whose_turn == 1:
            p_wg_score = self.wg_score[0]
            if self.move_count < int(self.max_moves/4):
                w = self.p1_weight_phases[0]
            elif self.move_count < int((self.max_moves*2)/3):
                w = self.p1_weight_phases[1]
            else:
                w = self.p1_weight_phases[2]
        else:
            p_wg_score = self.wg_score[1]
            if self.move_count < int(self.max_moves/4):
                w = self.p2_weight_phases[0]
            elif self.move_count < int((self.max_moves*2)/3):
                w = self.p2_weight_phases[1]
            else:
                w = self.p2_weight_phases[2]

        # compute heuristic scores from weights
        self.update_stability()
        w_diff = self.disc_difference * w[0]
        w_wg = (p_wg_score/100) * w[1] # the grid values themselves are also weights, /100 is normalization
        w_mob = (sum(self.mobility)/2) * w[2]
        w_pmob = (sum(self.p_mobility)/2) * w[3]
        w_stab = self.stability * w[4]

        return int(w_diff + w_wg + w_mob + w_pmob + w_stab)


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