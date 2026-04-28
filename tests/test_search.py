import unittest
from othello.board import Board
from othello.search import minimax, alpha_beta


# test minimax search functions correctly
class TestMinimax(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)


    def test_negative_depth(self):
        self.assertRaises(RecursionError, minimax, self.board, -1, 1)


    def test_no_depth(self):
        move, score = minimax(self.board, 0, 1)
        self.assertIsNone(move)
        self.assertEqual(score, 0)


    def test_min_depth(self):
        move, score = minimax(self.board, 1, 1)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)


    def test_mid_depth(self):
        move, score = minimax(self.board, 4, 1)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)


    def test_high_depth(self):
        move, score = minimax(self.board, 8, 1)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)


    def test_p2_search(self):
        self.board.make_move(1, -1, (4, 6))
        self.board.advance_turn(0)
        move, score = minimax(self.board, 4, -1)
        self.assertIs(type(move), tuple)
        self.assertNotEqual(move, (-1, -1))
        self.assertIs(type(score), int)


    def test_large_board_search(self):
        l_board = Board(32)

        move, score = minimax(l_board, 4, 1)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)


    def test_small_board_complete_search(self):
        s_board = Board(4)

        move, score = minimax(s_board, 8, 1)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)

        player = s_board.whose_turn
        opponent = player * -1

        for i in range(12):
            maximising = bool(player+1)
            move, score = minimax(s_board, 12-i, maximising)
            s_board.make_move(player, opponent, move)
            s_board.advance_turn(0)
            player, opponent = opponent, player

        winner, score = s_board.game_over()
        self.assertEqual(winner, -1)
        self.assertEqual(score, (6, 10))

    
    def test_midgame_search(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0, 0, -1, 0, 0, 0],
                            [0, 0, 0, 0, 1, -1, 1, 0, 0, 0],
                            [0, 0, 0, 0, -1, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        move, score = minimax(self.board, 4, False)
        self.assertEqual(move, (1, 8))
        self.assertIs(type(score), int)


    def test_endgame_search(self):
        self.board.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                            [0, -1, 1, 1, 1, 1, 1, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        
        self.board.move_count = 58
        move, score = minimax(self.board, 4, False)
        self.assertEqual(move, (1, 1))
        self.assertIs(type(score), int)


    def test_only_pass(self):
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
        
        move, score = minimax(self.board, 4, 1)
        self.assertEqual(move, (-1, -1))
        self.assertIs(type(score), int)


# test alpha-beta search functions correctly based on if it improves on minimax search
class TestAlphaBeta(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        


if __name__ == "__main__":
    unittest.main()