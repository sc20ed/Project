from learning.learn import test_eval
from othello.game import run_game, run_game_test
import logging

# create log and set config
log = logging.getLogger("main.py")
logging.basicConfig(filename="log.txt", filemode='w',
                    format="%(asctime)s | %(name)-8s | %(levelname)-8s | %(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S %p", encoding="utf-8", level=logging.INFO)

# prompt user to change the logging level
def set_logging_level():
    option = None
    while option not in range(1, 6):
        print("\n1: Debug\n2: Info\n3: Warning\n4: Error\n5: Critical")
        option = int(input("Select logging level: "))

        if option == 1:
            logging.getLogger().setLevel(logging.DEBUG)
        elif option == 2:
            logging.getLogger().setLevel(logging.INFO)
        elif option == 3:
            logging.getLogger().setLevel(logging.WARNING)
        elif option == 4:
            logging.getLogger().setLevel(logging.ERROR)
        elif option == 5:
            logging.getLogger().setLevel(logging.CRITICAL)
        else:
            print("\nInvalid option.")


# CLI for selecting evolutionary learning methods
def e_learning_cli():
    option = None
    while option not in [4, 5]:
        print("\n1: Test eval" \
              "\n2: tbc" \
              "\n3: tbc" \
              "\n4: Return to main menu" \
              "\n5: Exit")
        option = int(input("Select an option: "))

        # test evolutionary learning method
        if option == 1:
            test_eval()

        # return to main menu
        elif option == 4:
            pass

        # exit
        elif option == 5:
            return 5

        else:
            print("\nInvalid option.")


# CLI for selecting evolutionary learning, game type and logging level
def main():
    option = None
    while option != 5:
        print("\n1: Evolutionary Learning menu" \
              "\n2: CPU vs CPU game" \
              "\n3: Player vs CPU game" \
              "\n4: Set logging level" \
              "\n5: Exit")
        option = int(input("Select an option: "))

        # enter menu for evolutionary learning
        if option == 1:
            option = e_learning_cli()
            if option != 5:
                print("Returning to main menu.")

        # cpu vs cpu
        elif option == 2:
            log.info("Starting CPU vs CPU game")
            p1 = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                  [-2, 1, 2, 2, 1], [-1, 0.7, 2, 1, 1], [2, 0.5, 2, 1, 3]]
            p2 = [[2500, -250, -500, 70, -60, -120, -10, -50, -30, -40],
                  [0.5, 1, 2, 1, 1], [0.5, 1, 2, 1, 1], [0.5, 1, 2, 1, 1]]
            
            winner, score = run_game(8, 0, 4, p1, 2, 4, p2, 0)
            if winner == 0:
                print(f"DRAW")
                log.info("Draw with score %s", score)
            else:
                print(f"WINNER: Player {(winner+3)%3}")
                log.info("Player %s win with score %s", winner, score)
            print(f"SCORE: {score[0]} - {score[1]}")

        # player vs cpu
        elif option == 3:
            log.info("Starting Player vs CPU game")
            winner, score = run_game_test(8, 3, 0, 2, 4, 0)
            if winner == 0:
                print(f"DRAW")
                log.info("Draw with score %s", score)
            else:
                print(f"WINNER: Player {(winner+3)%3}")
                log.info("Player %s win with score %s", winner, score)
            print(f"SCORE: {score[0]} - {score[1]}")

        # change logging level
        elif option == 4:
            set_logging_level()
            log.info("Logging level set to %s", logging.getLevelName(log.getEffectiveLevel()))

        # exit
        elif option == 5:
            log.info("User exit")

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()