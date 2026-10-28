Optimising Othello Strategies with Co-Evolutionary Learning
============================================================
This project was created as part of the Final Year Project/Dissertation undertaken during my study at the University of Leeds, and has now been archived.

The aim of the project was to develop an Othello playing program with alpha-beta search and common heuristics to judge the game position, then use a genetic algorithm to create many players that evolve through competing to be part of the makeup of the following generation. Through this I aimed to empirically determine the value of various heuristics and therefore strategies at different stages of the game of Othello for both the current 8x8 board and a future prospective 10x10 board. More information (or access to the report) can be requested via email.

------------------------------------------------------------
The program runs on Python 3.14.4, and requires no external libraries or dependencies.

Instructions to run:
- clone the repository
- run "python main.py" or equivalent

From the main.py command line interface the available options are displayed.

The evolutionary learning methods work as expected: simply follow the options from the command line interface (WARNING: execution time can be very long for population sizes above 10 or 20).

To gather results, it is necessary to change the player weight sets in main.py and read from the log file after execution.

To run unit tests, enter "python -m unittest followed by all the tests you want to run (i.e. "python.exe -m unittest tests\test_board.py tests\test_search.py tests\test_game.py tests\test_generation.py").
