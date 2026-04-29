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

        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            self.board.append(row)

        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            self.weight_grid.append(row)

        self.setup()
    

    # create initial game position and weighted squares heuristic
    def setup(self):
        midpoint = int(self.size/2)
        self.board[midpoint-1][midpoint-1] = 1
        self.board[midpoint-1][midpoint] = -1
        self.board[midpoint][midpoint-1] = -1
        self.board[midpoint][midpoint] = 1
        
        # switch to file later
        self.weight_grid[1][1] = 50
        self.weight_grid[1][self.size-2] = 50
        self.weight_grid[self.size-2][1] = 50
        self.weight_grid[self.size-2][self.size-2] = 50

        self.weight_grid[2][1] = -25
        self.weight_grid[1][2] = -25
        self.weight_grid[2][2] = -25
        self.weight_grid[2][self.size-2] = -25
        self.weight_grid[1][self.size-3] = -25
        self.weight_grid[2][self.size-3] = -25
        self.weight_grid[self.size-3][1] = -25
        self.weight_grid[self.size-2][2] = -25
        self.weight_grid[self.size-3][2] = -25
        self.weight_grid[self.size-3][self.size-2] = -25
        self.weight_grid[self.size-2][self.size-3] = -25
        self.weight_grid[self.size-3][self.size-3] = -25


    # reset board and values
    def reset(self):
        self.unmake_list = []
        self.move_count = 0
        self.turn_count = 0
        self.whose_turn = 1
        self.square_difference = 0
        self.wg_score = 0

        for j in range(1, self.size-1):
            for i in range(1, self.size-1):
                self.board[i][j] = 0

        self.setup()


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


    # find frontier by checking the entire board
    def find_frontier(self, opponent):
        frontier = []

        for i in range(1, self.size-1):
            for j in range(1, self.size-1):
                if self.board[i][j] == 0:
                    if (self.board[i][j+1] == opponent or
                        self.board[i][j-1] == opponent or
                        self.board[i+1][j] == opponent or
                        self.board[i-1][j] == opponent or
                        self.board[i+1][j+1] == opponent or
                        self.board[i+1][j-1] == opponent or
                        self.board[i-1][j+1] == opponent or
                        self.board[i-1][j-1] == opponent):
                        frontier.append((i, j))

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

    
    # check what legal moves are available
    def find_moves(self, player, opponent):

        frontier = self.find_frontier(opponent)
        moves = []
        
        for square in frontier:
            if (self.validate_move(player, opponent, square)):
                moves.append(square)

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
        score = (self.square_difference +
                self.wg_score)

        return score