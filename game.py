from cow import Cow
from player import Player
from item import Item
from assets.context import cow_sayings, approaches, interruptions
from cow_interaction import CowInteraction
import random

class VirtualCowTipper:
    def __init__(self, player_name):
        self.player = Player(player_name)
        self.cows = [self.generate_cow() for _ in range(3)]
        self.cow_packs = {pack: 0 for pack in range(1, 7)}
        self.running = True

    def start(self):
        print("\nVirtual Cow Tipper!")

        while self.running:
            self.player_turn()
            self.check_end_conditions()

    def generate_cow(self)-> Cow:
        cow_properties = Cow.generate_random_cow_properties(self.player)
        return Cow(
            cow_properties['name'],
            cow_properties['req_amount'],
            cow_properties['likeliness'],
            cow_properties['strength'],
            cow_properties['hp'],
            cow_properties['is_shop'],
            cow_properties['is_aggro'],
            cow_properties['is_dairy'],
            cow_properties['pack']
        )

    def spawn_cow(self) -> Cow:
        cow = self.cows.pop(0)
        pack_score = self.cow_packs[cow.pack]
        cow.likeliness += pack_score
        self.cows.append(self.generate_cow())
        return cow

    def update_cow_scores(self, cow: Cow, score: float):
        self.cow_packs[cow.pack] += score
        for cow in self.cows:
            self.cows[self.cows.index(cow)].likeliness += score

    def player_turn(self):
        self.get_approach()
        is_interrupted = self.get_interruption()
        spawned_cow = self.spawn_cow()

        if is_interrupted:
            CowInteraction(self, self.player, spawned_cow).interact()
            return

        actions = {
            "approach the cow": lambda: CowInteraction(self, self.player, spawned_cow).interact(),
            "check inventory": lambda: self.player.check_inventory(),
            "use an item from inventory": self.player.use_item,
            "quit game": lambda: setattr(self, "running", False),
        }
        while True:
            print(*[f"{i+1}. {action.capitalize()}" for i, action in enumerate(actions.keys())], sep=" | ")

            choice = input("Choose an action (1-4): ")
            if choice.isdigit() and int(choice) in range(1, 5):
                action_idx = int(choice) - 1
                action_name = list(actions.keys())[action_idx]
                try:
                    actions[action_name](spawned_cow)
                except TypeError:
                    actions[action_name]()
                return
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")


    def get_approach(self):
        print(f"\n{random.choice(approaches)}\n")
    
    def get_interruption(self):
        return (lambda m: (print(f"\n{m}\n"), m)[1] if random.random() < 0.1 else False)(random.choice(interruptions))

    def check_end_conditions(self):
        if self.player.hp <= 0 or self.player.cash <= 0:
            self.player.die()
            self.running = False
