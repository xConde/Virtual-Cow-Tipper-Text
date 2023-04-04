from cow import Cow
from player import Player
from item import Item
from context import cow_sayings, approaches, interruptions

import random

class VirtualCowTipper:
    def __init__(self):
        player_name = input("Enter your name: ")
        self.player = Player(player_name)
        self.cows = []
        self.pack_membership = {}
        self.generate_cows()
        self.running = True

    def start(self):
        print("Welcome to Virtual Cow Tipper!")

        while self.running:
            self.player_turn()
            self.check_end_conditions()

    def generate_cows(self):
        total_cows = 30
        pack_size = 6

        for i in range(total_cows):
            cow_properties = Cow.generate_random_cow_properties()
            cow = Cow(cow_properties["name"], cow_properties["mood"], cow_properties["req_amount"])
            pack_num = i // pack_size
            self.cows.append(cow)
            self.pack_membership[cow] = pack_num

    def player_turn(self):
        self.player.display_info()
        self.get_approach()
        is_interrupted = self.get_interruption()
        chosen_cow = random.choices(self.cows)

        if is_interrupted:
            self.player.interact_with_cow(chosen_cow)
            return

        actions = {
            "approach the cow": self.player.interact_with_cow,
            "check inventory": self.player.check_inventory,
            "use an item from inventory": self.player.use_item,
            "quit game": lambda: setattr(self, "running", False),
        }
        while True:
            print("Actions:")
            for i, action in enumerate(actions.keys()):
                print(f"{i+1}. {action.capitalize()}")

            choice = input("Choose an action (1-4): ")
            if choice.isdigit() and int(choice) in range(1, 5):
                action_idx = int(choice) - 1
                action_name = list(actions.keys())[action_idx]
                try:
                    actions[action_name](chosen_cow)
                except TypeError:
                    actions[action_name]()
                return
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")


    def get_approach(self):
        print(f"\n{random.choice(approaches)}\n")
    
    def get_interruption(self):
        is_interrupted = random.randint(1, 100) <= 10
        print(f"\n{random.choice(interruptions)}\n") if is_interrupted else None
        return is_interrupted

    def check_end_conditions(self):
        if self.player.hp <= 0 or self.player.cash <= 0:
            print("Game Over!")
            self.running = False
