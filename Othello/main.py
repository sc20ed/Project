from game import cpu_game, player_game
# CLI for initiating cpu or player vs cpu games 

if __name__ == "__main__":

    option = None
    while option != 3:
        print("\n1: CPU vs CPU game\n2: Player vs CPU game\n3: exit")
        option = int(input("Select an option: "))

        if option == 1:
            cpu_game()

        elif option == 2:
            
            player_game()

        elif option == 3:
            pass

        else:
            print("\nInvalid option.")