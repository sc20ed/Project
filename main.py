from learning.learn import generate_players, evolve, standalone_fitness_evaluation
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
            print("Invalid option.")


# CLI for selecting evolutionary learning methods
def evolutionary_learning_cli():
    option = None
    while option not in [4, 5]:
        print("\n1: Generate population of players" \
              "\n2: Evolve population" \
              "\n3: Conduct additional population fitness evaluation" \
              "\n4: Return to main menu" \
              "\n5: Exit")
        option = int(input("Select an option: "))

        # create initial population and save to file
        if option == 1:
            filename = input("Enter filename for population (without extension): ")
            size = int(input("Enter population size: "))
            while size not in range(2, 101):
                print("\nPopulation size must be between 2 and 100.")
                size = int(input("\nEnter population size: "))
            generate_players(filename, size)
            print("Saved population to file " + filename + ".csv.")

        # evolve population from a starting file
        elif option == 2:
            filename = input("Enter filename of population to evolve (without extension): ")
            generations = int(input("Enter number of generations to compute: "))
            while generations not in range(1, 101):
                print("\nNumber of generations must be between 1 and 100.")
                generations = int(input("\nEnter number of generations to compute: "))
            board_size = int(input("Enter board size: "))
            while board_size not in range(8, 14, 2):
                print("\nBoard size must be either 8, 10, or 12.")
                board_size = int(input("\nEnter board size: "))
            evolve(filename, generations, board_size)
            print("Completed evolution of " + str(generations) + " generations for " + filename + ".csv.")

        # evaluate fitness for a population separate from evolve loop
        elif option == 3:
            filename = input("Enter filename of population to evaluate (without extension): ")
            board_size = int(input("Enter board size: "))
            while board_size not in range(8, 14, 2):
                print("\nBoard size must be either 8, 10, or 12.")
                board_size = int(input("\nEnter board size: "))
            print("Running fitness evaluation for " + filename + ".csv...")
            standalone_fitness_evaluation(filename, board_size)
            print("Completed fitness evaluation.")
                
        # return to main menu
        elif option == 4:
            pass

        # exit
        elif option == 5:
            return 5

        else:
            print("Invalid option.")


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

        # enter evolutionary learning menu
        if option == 1:
            option = evolutionary_learning_cli()
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
            print("Invalid option.")


if __name__ == "__main__":
    main()