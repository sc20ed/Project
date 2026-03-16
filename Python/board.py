class Board:
    def __init__(self, size=8):
        self.board = []
        self.size = size + 2
        self.frontier = set()
        self.square_difference = 0
        self.move_count = 0
        self.turn_count = 0
        self.whose_turn = 1
        self.unmake_list = []

        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(0)
            self.board.append(row)

        self.setup()
        #print(self.frontier)


    def setup(self):
        midpoint = int(self.size/2)
        self.board[midpoint-1][midpoint] = 2
        self.board[midpoint-1][midpoint-1] = 1
        self.board[midpoint][midpoint] = 1
        self.board[midpoint][midpoint-1] = 2

        """
        self.update_frontier((midpoint-1, midpoint))
        self.update_frontier((midpoint-1, midpoint-1))
        self.update_frontier((midpoint, midpoint))
        self.update_frontier((midpoint, midpoint-1))
        """


    def reset(self):
        for j in range(1, self.size-1):
            for i in range(1, self.size-1):
                self.board[i][j] = 0


    def display(self):
        for j in range(1, self.size-1):
            for i in range(1, self.size-1):
                print(str(self.board[i][j]) + " ", end='')
            print("")
        print("")


    def advance_turn(self, skipped):
        if not skipped:
            self.move_count += 1
        else:
            self.unmake_list.append([-1, -1])

        self.turn_count += 1
        self.whose_turn = (self.whose_turn*2) % 3


    def retract_turn(self):
        try:
            prev_turn = self.unmake_list.pop()
        except IndexError:
            return
        
        self.turn_count -= 1

        if prev_turn[0] == -1:
            self.whose_turn = (self.whose_turn*2) % 3
            return
        
        self.square_difference = prev_turn.pop(0)
        prev_move = prev_turn.pop(0)
        self.board[prev_move[0]][prev_move[1]] = 0

        for i, j in prev_turn:
            self.board[i][j] = self.whose_turn

        self.move_count -= 1
        self.whose_turn = (self.whose_turn*2) % 3


    """
    def update_frontier(self, move):
        x = move[0]
        y = move[1]

        if self.board[x][y+1] == 0 and y < 8:
            self.frontier.add((x, y+1))
        if self.board[x][y-1] == 0 and y > 1:
            self.frontier.add((x, y-1))
        if self.board[x+1][y] == 0 and x < 8:
            self.frontier.add((x+1, y))
        if self.board[x-1][y] == 0 and x > 1:
            self.frontier.add((x-1, y))
        if self.board[x+1][y+1] == 0 and x < 8 and y < 8:
            self.frontier.add((x+1, y+1))
        if self.board[x+1][y-1] == 0 and x < 8 and y > 1:
            self.frontier.add((x+1, y-1))
        if self.board[x-1][y+1] == 0 and x > 1 and y < 8:
            self.frontier.add((x-1, y+1))
        if self.board[x-1][y-1] == 0 and x > 1 and y > 1:
            self.frontier.add((x-1, y-1))
    """

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
    
    
    def validate_move(self, player, opponent, square):
        x = square[0]
        y = square[1]

        # for each direction if there is an opponent continue checking adjacent squares
        # if player is reached before empty or edge, add to move list and dont check other directions

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

    
    def find_moves(self, player, opponent):
        # Simplified frontier for now
        frontier = self.find_frontier(opponent)
        moves = []
        
        for square in frontier:
            if (self.validate_move(player, opponent, square)):
                moves.append(square)

        return moves


    def make_move(self, player, opponent, move):
        x = move[0]
        y = move[1]
        flip_squares = []

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
        #self.frontier.remove(move)
        #self.update_frontier(move)


    def flip(self, player, move, squares):
        modifier = 1
        if player == 2:
            modifier = -1

        turn_change = [self.square_difference, move]

        self.board[move[0]][move[1]] = player
        self.square_difference += modifier

        for line in squares:
            for square in line:
                turn_change.append(square)
                self.board[square[0]][square[1]] = player
                self.square_difference += (modifier*2)

        self.unmake_list.append(turn_change)
 

    def game_over(self):
        self.turn_count -= 2
        p1_total = 0
        p2_total = 0

        for i in range(1, self.size-1):
            for j in range(1, self.size-1):
                if self.board[i][j] == 1:
                    p1_total += 1
                elif self.board[i][j] == 2:
                    p2_total += 1

        print(p1_total)
        print(p2_total)
        print("Turn", self.turn_count)
        print("Moves", self.move_count)
        print("Heuristic =", self.heuristics())


        if p1_total > p2_total:
            print("Game over! The winner is player 1, with a total score of " + str(p1_total) + "!")

        elif p2_total > p1_total:
            print("Game over! The winner is player 2, with a total score of " + str(p2_total) + "!")

        else:
            print("Game over! The game is a draw, both players scored " + str(p1_total) + "!")
        

    # heuristic functions
    def heuristics(self):
        # naive heuristics first
        # total squares
        return self.square_difference
        

    


    
