import random
from item import Weapon, Shield, Tool, CowBell, Bucket, roll_weapon_dmg
from assets.context import small_damage_contexts, large_damage_contexts

class Player:
    def __init__(self, name, starting_hp=20, starting_cash=50):
        self.name = name
        self.hp = starting_hp
        self.cash = starting_cash
        self.inventory = []
        self.weapon = None
        self.shield = None

    def display_info(self, combat=True):
        print(f"{self.name} | HP: {self.hp} | Cash: ${self.cash}")
        if combat:
            if not self.weapon and not self.shield:
                print("Weapon: None | Shield: None")
            else:
                self.weapon.stats() if self.weapon else print("Weapon: None")
                self.shield.stats() if self.shield else print("Shield: None")

    def equip(self, item):
        if isinstance(item, Weapon):
            self.weapon = item
            print(f"{self.name} equipped {item.name} as weapon.")
        elif isinstance(item, Shield):
            self.shield = item
            print(f"{self.name} equipped {item.name} as shield.")
        else:
            print(f"{item.name} is neither a weapon nor a shield and cannot be equipped.")

    def update_hp(self, amount):
        self.hp += amount
        status = "healed" if amount > 0 else "took"
        print(f"{self.name} {status} {abs(amount)} HP. Current HP: {self.hp}")

    def take_damage(self, amount):
        self.hp -= amount
        print(f"{self.name} took {amount} damage. Current HP: {self.hp}")
        if self.hp <= 0:
            self.die()

    def print_small_damage_context(self, cow_name, total_damage):
        context = random.choice(small_damage_contexts)
        context = context.format(player_name=self.name, cow_name=cow_name, total_damage=total_damage)
        print(context)

    def print_large_damage_context(self, cow_name, total_damage):
        context = random.choice(large_damage_contexts)
        context = context.format(player_name=self.name, cow_name=cow_name, total_damage=total_damage)
        print(context)

    def deal_damage(self, cow):
        base_damage = 3 * (self.cash // 25)
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

    def die(self):
        print(f"{self.name} has died.")
        # Logic for handling player death, such as resetting stats, can be added here.

    def buy_item(self, item, cost):
        if self.cash >= cost:
            self.cash -= cost
            self.add_item_to_inventory(item)
            print(f"{self.name} bought {item.name} for ${cost}. Remaining cash: ${self.cash}")
        else:
            print(f"{self.name} does not have enough cash to buy {item.name}. Required: ${cost}, Available: ${self.cash}")

    def sell_item(self, item, value):
        if item in self.inventory:
            self.inventory.remove(item)
            self.cash += value
            print(f"{self.name} sold {item.name} for ${value}. Current cash: ${self.cash}")
        else:
            print(f"{self.name} does not have {item.name} in their inventory to sell.")

    def add_item_to_inventory(self, item):
        if len(self.inventory) >= 8:
            print(f"{self.name}'s inventory is full. {item.name} could not be added.")
            return

        self.inventory.append(item)

        if isinstance(item, (Weapon, Shield)) and item.is_upgrade(self, item):
            print(f"{self.name} added {item.name} to their inventory and equipped it as their new {item.type}.")
            self.equip(item)
        else:
            print(f"{self.name} added {item.name} to their inventory.")

    def remove_item_from_inventory(self, item):
        self.inventory.remove(item)
        print(f"{self.name} dropped {item.name} from their inventory.")
    
    def check_inventory(self):
        items = ', '.join(item.name for item in self.inventory) if self.inventory else "empty"
        print(f"{self.name}'s inventory: {items}\n")

    def use_item(self, item):
        if item in self.inventory:
            if isinstance(item, Tool):
                item.action()
                self.remove_item_from_inventory(item)
            else:
                print(f"{self.name} cannot use {item.name}.")
        else:
            print(f"{self.name} does not have {item.name} in their inventory.")
