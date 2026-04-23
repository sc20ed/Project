from game import run_game
# CLI for initiating cpu or player vs cpu games 

if __name__ == "__main__":

    option = None
    while option != 3:
        print("\n1: CPU vs CPU game\n2: TEST game\n3: exit")
        option = int(input("Select an option: "))

        if option == 1:
            winner, score = run_game(8, 0, 2, 0)
            print(f"WINNER: Player {(winner+3)%3}")
            print(f"SCORE: {score[0]} - {score[1]}")

        elif option == 2:
            winner, score = run_game(8, 3, 2, 0)
            print(f"WINNER: Player {(winner+3)%3}")
            print(f"SCORE: {score[0]} - {score[1]}")

        elif option == 3:
            pass

        else:
            print("\nInvalid option.")