from game import VirtualCowTipper

def main():
    player_name = input('Enter your name: ')
    game = VirtualCowTipper(player_name)
    game.start()

if __name__ == "__main__":
    main()