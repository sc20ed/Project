import unittest
from othello.board import Board
from othello.search import minimax, alpha_beta


# test something
class TestMinimax(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)


    def test_negative_depth(self):
        self.assertRaises(RecursionError, minimax, self.board, -1, 1)
        


if __name__ == "__main__":
    unittest.main()