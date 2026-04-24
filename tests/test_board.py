import unittest
from othello.board import Board


# test that the board is set up correctly
class TestSetup(unittest.TestCase):
    def test_setup_8(self):
        size = 8
        self.board = Board(size)

        for i in range(size+2):
            for j in range(size+2):
                if (i in [4, 5]) and (j in [4, 5]):
                    continue
                self.assertEqual(self.board.board[i][j], 0)
                    
        self.assertEqual(self.board.board[4][4], 1)
        self.assertEqual(self.board.board[5][4], -1)
        self.assertEqual(self.board.board[4][5], -1)
        self.assertEqual(self.board.board[5][5], 1)


    def test_setup_10(self):
        size = 10
        self.board = Board(size)

        for i in range(size+2):
            for j in range(size+2):
                if (i in [5, 6]) and (j in [5, 6]):
                    continue
                self.assertEqual(self.board.board[i][j], 0)
                    
        self.assertEqual(self.board.board[5][5], 1)
        self.assertEqual(self.board.board[6][5], -1)
        self.assertEqual(self.board.board[5][6], -1)
        self.assertEqual(self.board.board[6][6], 1)


    def test_setup_64(self):
        size = 64
        self.board = Board(size)

        for i in range(size+2):
            for j in range(size+2):
                if (i in [32, 33]) and (j in [32, 33]):
                    continue
                self.assertEqual(self.board.board[i][j], 0)
                    
        self.assertEqual(self.board.board[32][32], 1)
        self.assertEqual(self.board.board[33][32], -1)
        self.assertEqual(self.board.board[32][33], -1)
        self.assertEqual(self.board.board[33][33], 1)


    def test_setup_odd(self):
        size = 7
        self.board = Board(size)

        for i in range(size+2):
            for j in range(size+2):
                if (i in [3, 4]) and (j in [3, 4]):
                    continue
                self.assertEqual(self.board.board[i][j], 0)
                    
        self.assertEqual(self.board.board[3][3], 1)
        self.assertEqual(self.board.board[4][3], -1)
        self.assertEqual(self.board.board[3][4], -1)
        self.assertEqual(self.board.board[4][4], 1)


    def test_setup_small(self):
        size = 4
        self.board = Board(size)

        for i in range(size+2):
            for j in range(size+2):
                if (i in [2, 3]) and (j in [2, 3]):
                    continue
                self.assertEqual(self.board.board[i][j], 0)
                    
        self.assertEqual(self.board.board[2][2], 1)
        self.assertEqual(self.board.board[3][2], -1)
        self.assertEqual(self.board.board[2][3], -1)
        self.assertEqual(self.board.board[3][3], 1)


    @unittest.expectedFailure
    def test_setup_invalid(self):
        size = 0
        self.board = Board(size)

        for i in range(size+2):
            for j in range(size+2):
                if (i in [0, 1]) and (j in [0, 1]):
                    continue
                self.assertEqual(self.board.board[i][j], 0)
                    
        self.assertEqual(self.board.board[0][0], 1)
        self.assertEqual(self.board.board[1][0], -1)
        self.assertEqual(self.board.board[0][1], -1)
        self.assertEqual(self.board.board[1][1], 1)


    def test_reset_board(self):
        size = 8
        self.board = Board(size)
        self.board.reset()

        for i in range(size+2):
            for j in range(size+2):
                self.assertEqual(self.board.board[i][j], 0)


# test that move making functions correctly
class TestMoveMaking(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        self.moves = [(4, 6), (3, 6), (2, 6), (2, 7),
                      (2, 8), (1, 8), (3, 5), (5, 6)]


    def test_make_initial_move(self):
        player = self.board.whose_turn
        opponent = player * -1
        move = self.moves[0]
        self.board.make_move(player, opponent, move)

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, -1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        self.assertEqual(self.board.board, ex_board)

    
    def test_move_sequence(self):
        player = self.board.whose_turn
        opponent = player * -1
        
        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
                    [0, 0, 0, 0, 0, 0, 1, -1, 1, 0],
                    [0, 0, 0, 0, 0, 1, -1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, -1, 0, 0, 0],
                    [0, 0, 0, 0, -1, -1, -1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        self.assertEqual(self.board.board, ex_board)

    ########################################### PICK UP HERE
    def test_(self):
        player = self.board.whose_turn
        opponent = player * -1
        
        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
                    [0, 0, 0, 0, 0, 0, 1, -1, 1, 0],
                    [0, 0, 0, 0, 0, 1, -1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, -1, 0, 0, 0],
                    [0, 0, 0, 0, -1, -1, -1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        self.assertEqual(self.board.board, ex_board)


# test that frontier and move validation function correctly
class TestFrontierAndMoveValidation(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        self.moves = [(3, 5), (5, 6), (6, 3), (2, 5),
                      (4, 6), (3, 6), (5, 7), (6, 8),
                      (5, 8)]


    def test_initial_frontier(self):
        opponent = self.board.whose_turn * -1
        frontier = self.board.find_frontier(opponent)
        ex_frontier = [(3, 4), (3, 5), (3, 6), (4, 3),
                       (4, 6), (5, 3), (5, 6), (6, 3),
                       (6, 4), (6, 5)]

        self.assertEqual(frontier, ex_frontier)

    
    def test_midgame_frontier_1(self):
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves[:6]:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        frontier = self.board.find_frontier(opponent)
        ex_frontier = [(1, 4), (1, 5), (1, 6), (2, 4),
                       (2, 6), (2, 7), (3, 4), (3, 7),
                       (4, 7), (5, 7), (6, 4), (6, 5),
                       (6, 6), (6, 7)]
        
        self.assertEqual(frontier, ex_frontier)

    
    def test_midgame_frontier_2(self):
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        frontier = self.board.find_frontier(opponent)
        ex_frontier = [(3, 3), (3, 4), (4, 3), (4, 7),
                       (4, 8), (5, 2), (5, 3), (6, 2),
                       (6, 4), (6, 5), (6, 6), (6, 7),
                       (7, 2), (7, 3), (7, 4)]

        self.assertEqual(frontier, ex_frontier)


    def test_full_board_frontier(self):
        opponent = self.board.whose_turn * -1
        for i in range(1, 9):
            for j in range(1, 9):
                self.board.board[i][j] = opponent

        frontier = self.board.find_frontier(opponent)
        self.assertEqual(frontier, [])

    
    def test_valid_move(self):
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves[:4]:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        move_is_valid = self.board.validate_move(player, opponent, (2, 6))
        self.assertTrue(move_is_valid)

    
    def test_invalid_move(self):
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        move_is_valid = self.board.validate_move(player, opponent, (6, 7))
        self.assertFalse(move_is_valid)

    
    @unittest.expectedFailure
    def test_invalid_move_input(self):
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        move_is_valid = self.board.validate_move(player, opponent, (13, 15))
        self.assertFalse(move_is_valid)


# test that turn passing and unmaking function correctly
class TestTurns(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        moves = [(3, 5), (5, 6), (6, 3), (2, 5)]
        player = self.board.whose_turn
        opponent = player * -1

        for move in moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1


    def test_retract(self):
        self.board


    def test_retract_all(self):
        self.board


    def test_retract_empty(self):
        self.board

    
    def test_retract_redo(self):
        self.board


    def test_pass(self):
        self.board


# test that game over functions correctly
class TestGameOver(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)


    def test_setup(self):
        self.board


if __name__ == "__main__":
    unittest.main()