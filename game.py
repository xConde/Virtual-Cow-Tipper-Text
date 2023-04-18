from cow import Cow
from player import Player
from item import Item
from assets.context import interruptions
from cow_interaction import CowInteraction
from game_terminal import GameTerminal
import random

class VirtualCowTipper:
    def __init__(self, player_name):
        self.game_terminal = GameTerminal()
        self.player = Player(self.game_terminal, player_name)
        self.cow = None
        self.cows = [self.generate_cow() for _ in range(3)]
        self.cow_packs = {pack: 0 for pack in range(1, 7)}
        self.running = True

    def start(self):
        while self.running:
            self.game_terminal.refresh()
            self.player.display_info()
            self.player_turn()
            self.check_end_conditions()

    def generate_cow(self)-> Cow:
        cow_properties = Cow.generate_random_cow_properties(self.player)
        return Cow(
            self.game_terminal,
            cow_properties['name'],
            cow_properties['req_amount'],
            cow_properties['likeliness'],
            cow_properties['strength'],
            cow_properties['hp'],
            cow_properties['cash'],
            cow_properties['is_shop'],
            cow_properties['is_aggro'],
            cow_properties['pack'],
            cow_properties['approach']
        )

    def spawn_cow(self):
        if not self.cow:
            cow = self.cows.pop(0)
            pack_score = self.cow_packs[cow.pack]
            cow.likeliness += pack_score
            self.cow = cow
            self.cows.append(self.generate_cow())

    def destroy_cow(self):
        self.game_terminal.set_cow_stats('')
        self.cow = None

    def update_cow_scores(self, cow: Cow, score: float):
        self.cow_packs[cow.pack] += score
        for cow in self.cows:
            self.cows[self.cows.index(cow)].likeliness += score
        self.destroy_cow()

    def player_turn(self):
        if not self.cow:
            self.spawn_cow()
        self.cow.get_approach()

        is_interrupted = self.get_interruption()
        if is_interrupted:
            CowInteraction(self, self.player, self.cow).interact()
            return

        actions = {
            "approach the cow": lambda: CowInteraction(self, self.player, self.cow).interact(),
            "check inventory": lambda: self.player.check_inventory(),
            "use an item from inventory": self.player.use_item,
            "quit game": lambda: setattr(self, "running", False),
        }
        while True:
            menu_items = [f"{i+1}. {action.capitalize()}" for i, action in enumerate(actions.keys())]
            choice = self.game_terminal.get_menu_choice(menu_items)
            if int(choice) in range(1, len(actions.keys())+1):
                action_name = list(actions.keys())[int(choice) - 1]
                try:
                    actions[action_name](self.cow)
                except TypeError:
                    actions[action_name]()
                return
    
    def get_interruption(self):
        return (lambda m: (self.game_terminal.draw_dialog(m), m)[1] if random.random() < 0.1 else False)(random.choice(interruptions))

    def check_end_conditions(self):
        if self.player.hp <= 0 or self.player.cash <= 0:
            self.player.die()
            self.game_terminal.close_game_terminal()    # close the game terminal for now, add main menu later.
            self.running = False
