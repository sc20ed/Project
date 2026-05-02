import unittest
import time
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
        move, score = minimax(self.board, 7, 1)
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
        
        move, score = minimax(self.board, 4, 0)
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
        move, score = minimax(self.board, 4, 0)
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


# as alpha-beta search and minimax search are very similar, some basic tests are redundant
# tests for alpha-beta compare execution time with minimax to ensure that the implementation is an improvement

# test alpha-beta search functions correctly based on if it improves on minimax search
class TestAlphaBeta(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
        self.moves = [(3, 5), (5, 6), (6, 3), (2, 5),
                 (4, 6), (3, 6), (5, 7), (6, 8),
                 (5, 8), (4, 8), (3, 7), (2, 6),
                 (1, 6), (6, 4), (6, 5), (7, 5),
                 (6, 6), (5, 3), (3, 4), (6, 7)]
        
        player = self.board.whose_turn
        opponent = player * -1

        for move in self.moves:
            self.board.make_move(player, opponent, move)
            self.board.advance_turn(0)
            player = self.board.whose_turn
            opponent = player * -1
        
    
    def test_no_depth(self):
        move, score = alpha_beta(self.board, 0, 1)
        self.assertIsNone(move)
        self.assertIs(type(score), int)


    def test_min_depth(self):
        move, score = alpha_beta(self.board, 1, 1)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)


    def test_depth_4(self):
        move, score = 0, 0

        mm_start = time.process_time()
        move, score = minimax(self.board, 4, 1)
        mm_finish = time.process_time()
        mm_time = mm_finish - mm_start

        ab_start = time.process_time()
        move, score = alpha_beta(self.board, 4, 1)
        ab_finish = time.process_time()
        ab_time = ab_finish - ab_start
        
        self.assertLess(ab_time, mm_time)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)


    def test_depth_5(self):
        move, score = 0, 0

        mm_start = time.process_time()
        move, score = minimax(self.board, 5, 1)
        mm_finish = time.process_time()
        mm_time = mm_finish - mm_start

        ab_start = time.process_time()
        move, score = alpha_beta(self.board, 5, 1)
        ab_finish = time.process_time()
        ab_time = ab_finish - ab_start
        
        self.assertLess(ab_time, mm_time)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)


    # for this depth and beyond a new board is used to reduce search time
    def test_depth_6(self):
        board = Board(8)
        player = board.whose_turn
        opponent = player * -1

        for move in self.moves[:4]:
            board.make_move(player, opponent, move)
            board.advance_turn(0)
            player = board.whose_turn
            opponent = player * -1

        move, score = 0, 0

        mm_start = time.process_time()
        move, score = minimax(board, 6, 1)
        mm_finish = time.process_time()
        mm_time = mm_finish - mm_start

        ab_start = time.process_time()
        move, score = alpha_beta(board, 6, 1)
        ab_finish = time.process_time()
        ab_time = ab_finish - ab_start

        self.assertLess(ab_time, mm_time)
        self.assertIs(type(move), tuple)
        self.assertIs(type(score), int)


    def test_p2_search(self):
        self.board.make_move(1, -1, (7, 6))
        self.board.advance_turn(0)

        move, score = alpha_beta(self.board, 4, -1)
        self.assertIs(type(move), tuple)
        self.assertNotEqual(move, (-1, -1))
        self.assertIs(type(score), int)


    # may fail due to current heuristic implementation
    def test_small_board_complete_search(self):
        s_board = Board(4)
        player = s_board.whose_turn
        opponent = player * -1

        mm_start = time.process_time()
        for i in range(12):
            maximising = bool(player+1)
            move, score = minimax(s_board, 12-i, maximising)
            s_board.make_move(player, opponent, move)
            s_board.advance_turn(0)
            player, opponent = opponent, player
        mm_finish = time.process_time()
        mm_time = mm_finish - mm_start

        s_board.reset()
        player = s_board.whose_turn
        opponent = player * -1

        ab_start = time.process_time()
        for i in range(12):
            maximising = bool(player+1)
            move, score = alpha_beta(s_board, 12-i, maximising)
            s_board.make_move(player, opponent, move)
            s_board.advance_turn(0)
            player, opponent = opponent, player
        ab_finish = time.process_time()
        ab_time = ab_finish - ab_start

        winner, score = s_board.game_over()
        self.assertLess(ab_time, mm_time)
        self.assertEqual(winner, -1)
        self.assertEqual(score, (6, 10))
    

if __name__ == "__main__":
    unittest.main()