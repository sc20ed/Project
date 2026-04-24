from game import run_game
import logging

log = logging.getLogger(__name__)
logging.basicConfig(filename="log.txt", filemode="w",
                    format='%(asctime)s | %(name)-8s | %(levelname)-8s | %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', encoding="utf-8", level=logging.DEBUG)

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



# CLI for selecting options and game type
def main():
    option = None
    while option != 4:
        print("\n1: CPU vs CPU game\n2: Player vs CPU game\n3: Set logging level\n4: exit")
        option = int(input("Select an option: "))

        if option == 1:
            log.info("Starting CPU vs CPU game")
            winner, score = run_game(8, 0, 2, 0)
            print(f"WINNER: Player {(winner+3)%3}")
            print(f"SCORE: {score[0]} - {score[1]}")
            log.info("Player %s win with score %s", winner, score)

        elif option == 2:
            log.info("Starting Player vs CPU game")
            winner, score = run_game(8, 3, 2, 0)
            print(f"WINNER: Player {(winner+3)%3}")
            print(f"SCORE: {score[0]} - {score[1]}")
            log.info("Player %s win with score %s", winner, score)

        elif option == 3:
            set_logging_level()
            log.info("Logging level set to %s", logging.getLevelName(log.getEffectiveLevel()))

        elif option == 4:
            log.info("User exit")

        else:
            print("\nInvalid option.")


if __name__ == "__main__":
    main()