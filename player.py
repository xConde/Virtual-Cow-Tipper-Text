import random
from item import Weapon, Shield, Tool, CowBell, Bucket, roll_weapon_dmg
from assets.context import small_damage_contexts, large_damage_contexts

class Player:
    def __init__(self, game_terminal, name, starting_hp=20, starting_cash=50):
        self.game_terminal = game_terminal
        self.name = name
        self.hp = starting_hp
        self.cash = starting_cash
        self.inventory = []
        self.weapon = None
        self.shield = None

    def display_info(self, combat=True):
        player_stats = f"{self.name} | HP: {self.hp} | Cash: ${self.cash}"
        weapon = self.weapon.display_name() if self.weapon else "Weapon: None"
        shield = self.shield.display_name() if self.shield else "Shield: None"
        self.game_terminal.set_player_stats(player_stats, weapon, shield)
        self.game_terminal.refresh()

    def equip(self, item):
        if isinstance(item, Weapon):
            self.weapon = item
        elif isinstance(item, Shield):
            self.shield = item
        else:
            print(f"{item.name} is neither a weapon nor a shield and cannot be equipped.")

    def print_small_damage_context(self, cow_name, total_damage):
        context = random.choice(small_damage_contexts)
        context = context.format(player_name=self.name, cow_name=cow_name, total_damage=total_damage)
        print(context)

    def print_large_damage_context(self, cow_name, total_damage):
        context = random.choice(large_damage_contexts)
        context = context.format(player_name=self.name, cow_name=cow_name, total_damage=total_damage)
        print(context)

    def deal_damage(self, cow):
        base_damage = 2 * random.randint(1, 4)  + (self.cash // 25)
        weapon_damage = roll_weapon_dmg(self.weapon)
        total_damage = base_damage + weapon_damage
        total_damage = total_damage if cow.hp >= total_damage else cow.hp
        cow.hp -= total_damage

        print_small_hit_context = total_damage <= cow.hp * 0.2 and random.random() <= 0.66
        print_large_hit_context = total_damage >= cow.hp * 0.5

        if print_small_hit_context:
            self.print_small_damage_context(cow.name, total_damage)
        elif print_large_hit_context:
            self.print_large_damage_context(cow.name, total_damage)
        else:
            print(f"{self.name} dealt {total_damage} damage to {cow.name}.")
        self.display_info()

    def update_cash(self, amount):
        self.cash += amount
        self.display_info()

    def die(self):
        print(f"{self.name} has died.")
        # Logic for handling player death, such as resetting stats, can be added here.

    def update_inventory(self, item, action):
        if action == "add" and len(self.inventory) < 8:
            self.inventory.append(item)
            if isinstance(item, (Weapon, Shield)) and item.is_upgrade(self, item):
                self.equip(item)
        elif action == "remove" and item in self.inventory:
            self.inventory.remove(item)
        else:
            print(f"update_inventory failed to {action} {item.name}.")
    
    def check_inventory(self):
        items = ', '.join(item.name for item in self.inventory) if self.inventory else "empty"
        print(f"{self.name}'s inventory: {items}")

    def use_item(self, item):
        if item in self.inventory:
            if isinstance(item, Tool):
                item.action()
                self.remove_item_from_inventory(item)
            else:
                print(f"{self.name} cannot use {item.name}.")
        else:
            print(f"{self.name} does not have {item.name} in their inventory.")
