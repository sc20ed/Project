from game import cpu_game, player_game, run_game
# CLI for initiating cpu or player vs cpu games 

if __name__ == "__main__":

    option = None
    while option != 3:
        print("\n1: CPU vs CPU game\n2: TEST game\n3: exit")
        option = int(input("Select an option: "))

        if option == 1:
            run_game(8, 0, 2, 0)

        elif option == 2:
            run_game(8, 3, 2, 0)

        elif option == 3:
            pass

        else:
            print("\nInvalid option.")