import random

class CowInteraction():
    def __init__(self, player, cow):
        self.player = player
        self.cow = cow

    def interact(self):
        combat_chance = self.calculate_combat_chance()
        dairy_chance = self.calculate_dairy_chance()

        action_roll = random.randint(1, 100)

        if action_roll <= combat_chance:
            self.handle_combat()
        elif action_roll <= combat_chance + dairy_chance:
            self.handle_dairy()
        else:
            self.handle_tip_or_leave()

    def calculate_combat_chance(self):
        base_chance = 15
        scaling_factor = (35 - base_chance) / 9
        combat_chance = base_chance + scaling_factor * (10 - self.cow.likeliness)
        return combat_chance

    def calculate_dairy_chance(self):
        cow_bell = self.get_cow_bell()
        return 5 if not cow_bell else cow_bell.get_dairy_bonus()


    def handle_combat(self):
        print(f"A combat with '{self.cow.name}' has started!")

        while self.player.hp > 0 and self.cow.hp > 0:
            player_damage = self.player.deal_damage()
            self.cow.hp -= player_damage
            print(f"You dealt {player_damage} damage to the cow. The cow has {self.cow.hp} HP left.")

            if self.cow.hp <= 0:
                print("You have defeated the cow.")
                break
            
            hit_prob = 40 + self.cow.likeliness * random.randint(1, 2) * (2 if self.cow.mood == 'upset' else 1)
            hit_player = random.random() < hit_prob / 100
            if hit_player:
                self.player.hp -= self.cow.strength
                print(f"The cow hit you for {self.cow.strength} damage. You have {self.player.hp} HP left.")
            else:
                print("The cow missed its attack.")

        if self.player.hp <= 0:
            print("You have been defeated by the cow.")

    def handle_dairy(self):
        bucket = self.get_bucket()
        if bucket:
            liquid_gold = bucket.use()
            self.player.update_inventory(liquid_gold, "add")
            self.player.update_inventory(bucket, "remove")
            print(self.cow.get_dairy_response(True))
        else:
            print(self.cow.get_dairy_response(False))

    def get_cow_bell(self):
        for item in self.player.inventory:
            if isinstance(item, CowBell):
                return item
        return None

    def get_bucket(self):
        for item in self.player.inventory:
            if isinstance(item, Bucket):
                return item
        return None

    def handle_tip_or_leave(self):
        # Handle tipping or leaving interaction with self.cow
        pass
