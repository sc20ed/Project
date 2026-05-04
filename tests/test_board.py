import unittest
from othello.board import Board


# test that the board is set up correctly
class TestSetupBoard(unittest.TestCase):
    def test_setup_8(self):
        board = Board(8)

        for i in range(board.size):
            for j in range(board.size):
                if (i in [4, 5]) and (j in [4, 5]):
                    continue
                self.assertEqual(board.board[i][j], 0)
                    
        self.assertEqual(board.board[4][4], 1)
        self.assertEqual(board.board[5][4], -1)
        self.assertEqual(board.board[4][5], -1)
        self.assertEqual(board.board[5][5], 1)


    def test_setup_10(self):
        board = Board(10)

        for i in range(board.size):
            for j in range(board.size):
                if (i in [5, 6]) and (j in [5, 6]):
                    continue
                self.assertEqual(board.board[i][j], 0)
                    
        self.assertEqual(board.board[5][5], 1)
        self.assertEqual(board.board[6][5], -1)
        self.assertEqual(board.board[5][6], -1)
        self.assertEqual(board.board[6][6], 1)


    def test_setup_64(self):
        board = Board(64)

        for i in range(board.size):
            for j in range(board.size):
                if (i in [32, 33]) and (j in [32, 33]):
                    continue
                self.assertEqual(board.board[i][j], 0)
                    
        self.assertEqual(board.board[32][32], 1)
        self.assertEqual(board.board[33][32], -1)
        self.assertEqual(board.board[32][33], -1)
        self.assertEqual(board.board[33][33], 1)


    def test_setup_odd(self):
        board = Board(7)

        for i in range(board.size):
            for j in range(board.size):
                if (i in [3, 4]) and (j in [3, 4]):
                    continue
                self.assertEqual(board.board[i][j], 0)
                    
        self.assertEqual(board.board[3][3], 1)
        self.assertEqual(board.board[4][3], -1)
        self.assertEqual(board.board[3][4], -1)
        self.assertEqual(board.board[4][4], 1)


    def test_setup_small(self):
        board = Board(4)

        for i in range(board.size):
            for j in range(board.size):
                if (i in [2, 3]) and (j in [2, 3]):
                    continue
                self.assertEqual(board.board[i][j], 0)
                    
        self.assertEqual(board.board[2][2], 1)
        self.assertEqual(board.board[3][2], -1)
        self.assertEqual(board.board[2][3], -1)
        self.assertEqual(board.board[3][3], 1)


    def test_setup_invalid(self):
        self.assertRaises(IndexError, Board, 0)


    def test_reset_board(self):
        board = Board(8)
        player = board.whose_turn
        opponent = player * -1
        moves = [(3, 5), (5, 6), (6, 3), (2, 5)]

        for move in moves:
            board.make_move(player, opponent, move)
            board.advance_turn(0)
            player = board.whose_turn
            opponent = player * -1

        board.reset()
        for i in range(board.size):
            for j in range(board.size):
                if (i in [4, 5]) and (j in [4, 5]):
                    continue
                self.assertEqual(board.board[i][j], 0)

        self.assertEqual(board.turn_count, 0)
        self.assertEqual(board.move_count, 0)


# test that move making functions correctly
class TestMoveMaking(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        self.moves = [(4, 6), (3, 6), (2, 6), (2, 7),
                      (2, 8), (1, 8), (3, 5), (5, 6)]


    def test_initial_move(self):
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


    def test_wrong_move(self):
        player = self.board.whose_turn
        opponent = player * -1
        move = self.moves[2]
        self.board.make_move(player, opponent, move)

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, -1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        self.assertEqual(self.board.board, ex_board)
    

    def test_gap_move(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, -1, -1, 0, 0, 0, 0],
                            [0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        player = self.board.whose_turn
        opponent = player * -1
        move = (3, 7)
        self.board.make_move(player, opponent, move)

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, -1, -1, 0, 1, 0, 0],
                    [0, 0, 0, 0, -1, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
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

    
    def test_flip_full_board(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, 1, -1, -1, -1, -1, -1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        player = self.board.whose_turn
        opponent = player * -1
        moves = [(8, 7), (1, 1), (1, 2), (1, 3),
                 (1, 4), (1, 5), (1, 6), (8, 8),
                 (1, 7), (1, 8)]

        for move in moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            self.board.advance_turn(1)

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        self.assertEqual(self.board.board, ex_board)


    def test_full_four_corner_moves(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, -1, -1, -1, -1, -1, -1, 0, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, 1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, -1, -1, -1, -1, -1, -1, -1, -1, 0],
                            [0, 0, -1, -1, -1, -1, -1, -1, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        player = self.board.whose_turn
        opponent = player * -1
        moves = [(1, 1), (1, 8), (8, 1), (8, 8)]

        for move in moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            self.board.advance_turn(1)

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, -1, -1, -1, -1, 1, 1, 0],
                    [0, 1, -1, 1, -1, -1, 1, -1, 1, 0],
                    [0, 1, -1, -1, 1, 1, -1, -1, 1, 0],
                    [0, 1, -1, -1, 1, 1, -1, -1, 1, 0],
                    [0, 1, -1, 1, -1, -1, 1, -1, 1, 0],
                    [0, 1, 1, -1, -1, -1, -1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                
        self.assertEqual(self.board.board, ex_board)


    def test_invalid_bounds_move(self):
        player = self.board.whose_turn
        opponent = player * -1
        
        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        move = (0, 9)
        self.assertRaises(IndexError, self.board.make_move, player, opponent, move)


    def test_out_of_bounds_move(self):
        player = self.board.whose_turn
        opponent = player * -1
        
        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        move = (0, 10)
        self.assertRaises(IndexError, self.board.make_move, player, opponent, move)


# test that move validation functions correctly
class TestMoveValidation(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        self.moves = [(3, 5), (5, 6), (6, 3), (2, 5),
                      (4, 6), (3, 6), (5, 7), (6, 8),
                      (5, 8)]
        
        
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

    
    def test_invalid_move_1(self):
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        move_is_valid = self.board.validate_move(player, opponent, (6, 7))
        self.assertFalse(move_is_valid)


    def test_invalid_move_1(self):
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        move_is_valid = self.board.validate_move(player, opponent, (4, 1))
        self.assertFalse(move_is_valid)

    
    def test_invalid_move_input(self):
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1

        move = (13, 15)
        self.assertRaises(IndexError, self.board.validate_move, player, opponent, move)


# test that frontier generation functions correctly
class TestFrontier(unittest.TestCase):
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


# test that turn passing and retracting function correctly
class TestRetractTurn(unittest.TestCase):
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
        self.board.retract_turn()
        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, -1, -1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        self.assertEqual(self.board.board, ex_board)
        self.assertEqual(len(self.board.unmake_list), 3)
        


    def test_retract_all(self):
        for i in range(4):
            self.board.retract_turn()

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, -1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        self.assertEqual(self.board.board, ex_board)
        self.assertEqual(len(self.board.unmake_list), 0)


    def test_retract_empty(self):
        for i in range(4):
            self.board.retract_turn()

        self.assertRaises(IndexError, self.board.retract_turn)

    
    def test_retract_redo(self):
        self.board.retract_turn()
        player = self.board.whose_turn
        opponent = player * -1
        self.board.make_move(player, opponent, (2, 5))

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, -1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, -1, -1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        self.assertEqual(self.board.board, ex_board)
        self.assertEqual(len(self.board.unmake_list), 4)

    
    def test_retract_redo_retract(self):
        self.board.retract_turn()
        player = self.board.whose_turn
        opponent = player * -1
        self.board.make_move(player, opponent, (2, 5))
        self.board.advance_turn(0)
        self.board.retract_turn()

        ex_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, -1, -1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        self.assertEqual(self.board.board, ex_board)
        self.assertEqual(len(self.board.unmake_list), 3)


    def test_pass(self):
        self.board.advance_turn(1)
        self.assertEqual(self.board.whose_turn, -1)
        self.assertEqual(len(self.board.unmake_list), 5)
        self.assertEqual(self.board.unmake_list[4][1], -1)


# test that game over functions correctly
class TestGameOver(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)


    def test_p1_win(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, -1, -1, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        winner, score = self.board.game_over()
        self.assertEqual(winner, 1)
        self.assertEqual(score, (5, 2))


    def test_p2_win(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, -1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, -1, -1, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        winner, score = self.board.game_over()
        self.assertEqual(winner, -1)
        self.assertEqual(score, (3, 5))


    def test_draw(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, -1, 0, 0, 0, 0],
                            [0, 0, 0, -1, -1, -1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        winner, score = self.board.game_over()
        self.assertEqual(winner, 0)
        self.assertEqual(score, (5, 5))


    def test_full_board(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        winner, score = self.board.game_over()
        self.assertEqual(winner, 1)
        self.assertEqual(score, (64, 0))
        

    def test_overfull_board(self):
        self.board.board = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],]
        
        winner, score = self.board.game_over()
        self.assertEqual(winner, 1)
        self.assertEqual(score, (64, 0))


# test that heuristics function correctly
class TestHeuristics(unittest.TestCase):
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


    def test_disc_diff(self):
        pass


    def test_mob(self):
        pass
    

    def test_p_mob(self):
        pass

    
    def test_wg_setup(self):
        pass


    def test_wg_score(self):
        pass


    def test_retract_heuristics(self):
        pass
    

    def test_wg_corner_change(self):
        pass


    def test_retract_wg_corner_change(self):
        pass


if __name__ == "__main__":
    unittest.main()