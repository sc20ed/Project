import unittest, unittest.mock
import contextlib
from othello.game import run_game, run_game_test, turn
from othello.board import Board


# test turns function correctly
class TestTurn(unittest.TestCase):
    def setUp(self):
        self.board = Board(8)
    

    def test_random_turn(self):
        turn(self.board, 0)
        self.assertEqual(self.board.turn_count, 1)
        self.assertEqual(self.board.move_count, 1)


    def test_minimax_turn(self):
        turn(self.board, 1)
        self.assertEqual(self.board.turn_count, 1)
        self.assertEqual(self.board.move_count, 1)

    
    def test_alpha_beta_turn(self):
        turn(self.board, 2)
        self.assertEqual(self.board.turn_count, 1)
        self.assertEqual(self.board.move_count, 1)


    @unittest.mock.patch("othello.game.input")
    def test_player_turn(self, input):
        input.side_effect = [4]
        with contextlib.redirect_stdout(None):
            turn(self.board, 3)

        self.assertEqual(self.board.turn_count, 1)
        self.assertEqual(self.board.move_count, 1)


    def test_turn_sequence(self):
        turn(self.board, 0)
        turn(self.board, 1)
        turn(self.board, 0)
        turn(self.board, 1)
        turn(self.board, 0)
        self.assertEqual(self.board.turn_count, 5)
        self.assertEqual(self.board.move_count, 5)
        self.assertEqual(self.board.whose_turn, -1)
    

    def test_no_move_available(self):
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
        
        result = turn(self.board, 0)
        self.assertEqual(result, 1)
        self.assertEqual(self.board.whose_turn, -1)


    def test_invalid_p_type(self):
        result = turn(self.board, 15)
        self.assertEqual(result, 1)
        self.assertEqual(self.board.whose_turn, -1)


# test different types of game function correctly
# run_game_test() is used as it is an older game function but is functionally
# the same as run_game() besides having both players use the same set of weights
# stdout is redirected because this test function usually prints to the command line
class TestGame(unittest.TestCase):
    def test_random_game(self):
        with contextlib.redirect_stdout(None):
            winner, score = run_game_test()

        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)


    def test_random_game_large(self):
        with contextlib.redirect_stdout(None):
            winner, score = run_game_test(16)

        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)


    def test_search_game(self):
        with contextlib.redirect_stdout(None):
            winner, score = run_game_test(8, 0, 0, 2, 4)

        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)


    def test_search_game_large(self):
        with contextlib.redirect_stdout(None):
            winner, score = run_game_test(12, 0, 0, 2, 4, 120)

        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)


    def test_player_order_swap(self):
        with self.assertLogs("game.py", 10) as logs:
            with contextlib.redirect_stdout(None):
                winner, score = run_game_test(8, 0, 0, 2, 2, 1)

        ex_log = "DEBUG:game.py:Swapped turn order to offset odd number of random moves"
        self.assertIn(ex_log, logs.output)
        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)


    def test_random_moves_1(self):
        with self.assertLogs("game.py", 10) as logs:
            with contextlib.redirect_stdout(None):
                winner, score = run_game_test(8, 0, 0, 2, 2, 4)

        ex_log = "DEBUG:game.py:Swapped turn order to offset odd number of random moves"
        self.assertNotIn(ex_log, logs.output)
        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)


    def test_random_moves_2(self):
        with self.assertLogs("game.py", 10) as logs:
            with contextlib.redirect_stdout(None):
                winner, score = run_game_test(8, 0, 0, 2, 2, 5)

        ex_log = "DEBUG:game.py:Swapped turn order to offset odd number of random moves"
        self.assertIn(ex_log, logs.output)
        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)


    def test_random_moves_full(self):
        with self.assertLogs("game.py", 10) as logs:
            with contextlib.redirect_stdout(None):
                winner, score = run_game_test(8, 0, 0, 2, 2, 60)
                
        ex_log = "DEBUG:game.py:Board full, game complete"
        self.assertIn(ex_log, logs.output)      
        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)


    def test_no_moves(self):
        with self.assertLogs("game.py", 10) as logs:
            with contextlib.redirect_stdout(None):
                winner, score = run_game_test(2)
        ex_log = "DEBUG:game.py:Board full, game complete"
        self.assertIn(ex_log, logs.output)      
        self.assertEqual(winner, 0)
        self.assertEqual(score, (2, 2))

    
    def test_endgame_search(self):
        endgame_depth = 10
        with self.assertLogs("game.py", 10) as logs:
            with contextlib.redirect_stdout(None):
                winner, score = run_game_test(8, 0, 0, 2, 2, 50)
        ex_log = "DEBUG:game.py:Endgame search, only final disc_diff considered"
        self.assertIn(ex_log, logs.output)      
        self.assertIs(type(winner), int)
        self.assertIs(type(score), tuple)

    
    def test_separate__heuristics_game(self):
        p1 = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
              [-2, 1, 2, 2, 1], [-1, 0.7, 2, 1, 1], [2, 0.5, 2, 1, 3]]
        p2 = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
              [2, -1, -2, -2, -1], [1, -0.7, -2, -1, -1], [-2, -0.5, -2, -1, -3]]
        
        winner, score = run_game(8, 2, 2, p1, 2, 2, p2, 0) 
        self.assertEqual(winner, 1)
        self.assertIs(type(score), tuple)


if __name__ == "__main__":
    unittest.main()