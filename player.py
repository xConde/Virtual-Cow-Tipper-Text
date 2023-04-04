
class Player:
    def __init__(self, name, starting_hp=20, starting_cash=50):
        self.name = name
        self.hp = starting_hp
        self.cash = starting_cash
        self.inventory = []
        self.weapon = None
        self.shield = None

    def display_info(self):
        print(f"Name: {self.name}\nHP: {self.hp}\nCash: ${self.cash}")
        print(f"{'Equipped Weapon:' + self.weapon.name if self.weapon else 'No weapon equipped.'}")
        print(f"{'Equipped Shield:' + self.shield.name if self.shield else 'No shield equipped.'}\n")

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
    
    def update_inventory(self, item, action):
        if action == "add":
            if len(self.inventory) < 4:
                self.inventory.append(item)
                print(f"{self.name} added {item.name} to their inventory.")
            else:
                print(f"{self.name}'s inventory is full. {item.name} could not be added.")
        elif action == "remove":
            self.inventory.remove(item)
            print(f"{self.name} dropped {item.name} from their inventory.")

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

    def interact_with_cow(self, chosen_cow):
        combat_chance = self.calculate_combat_chance(chosen_cow)
        dairy_chance = self.calculate_dairy_chance()

        action_roll = random.randint(1, 100)

        if action_roll <= combat_chance:
            self.handle_combat(chosen_cow)
        elif action_roll <= combat_chance + dairy_chance:
            self.handle_dairy(chosen_cow)
        else:
            self.handle_tip_or_leave(chosen_cow)

    def calculate_combat_chance(self, chosen_cow):
        base_chance = 15
        scaling_factor = (35 - base_chance) / 9
        combat_chance = base_chance + scaling_factor * (10 - chosen_cow.likeliness)
        return combat_chance

    def calculate_dairy_chance(self):
        cow_bell = any(isinstance(item, CowBell) for item in self.inventory)
        return 5 if not cow_bell else 15

    def handle_combat(self, chosen_cow):
        # Handle combat interaction with chosen_cow
        pass

    def handle_dairy(self, chosen_cow):
        has_bucket = any(isinstance(item, Bucket) for item in self.inventory)
        print(chosen_cow.get_dairy_response(has_bucket))

    def handle_tip_or_leave(self, chosen_cow):
        # Handle tipping or leaving interaction with chosen_cow
        pass

