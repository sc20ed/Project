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


# test that frontier and move validation function correctly
class TestMoveValidation(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        
        moves = [(3, 5), (5, 6), (6, 3), (2, 5)]
        for i in moves:
            player = self.board.whose_turn
            opponent = player * -1
            self.board.make_move(player, opponent, i)
            self.board.advance_turn(0)


    def test_find_frontier(self):
        self.board.find_frontier()


# test that move making functions correctly
class TestMoveMaking(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)


    def test_setup(self):
        self.board


# test that turn passing and unmaking function correctly
class TestTurns(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        
        moves = [(3, 5), (5, 6), (6, 3), (2, 5)]
        for i in moves:
            player = self.board.whose_turn
            opponent = player * -1
            self.board.make_move(player, opponent, i)
            self.board.advance_turn(0)


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
    print(os.getcwd())
    unittest.main()