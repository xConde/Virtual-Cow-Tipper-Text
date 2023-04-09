import random

class CowInteraction():
    def __init__(self, game_instance, player, cow):
        self.game_instance = game_instance
        self.player = player
        self.cow = cow

    def interact(self):
        handlers = {
            "aggro": self.handle_combat,
            "shop": self.handle_shop,
            "dairy": self.handle_dairy,
            "tip_or_leave": self.handle_tip_or_leave
        }
        
        cow_type = "shop" if self.cow.is_shop else "dairy" if self.cow.is_dairy else "aggro" if self.cow.is_aggro else "tip_or_leave"
        handler = handlers[cow_type]
        
        self.game_instance.player.display_info(combat=self.cow.is_aggro)
        handler()

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

    def handle_shop(self):
        print('shopping!')

    def handle_dairy(self):
        bucket = self.get_bucket()
        if bucket:
            liquid_gold = bucket.use()
            self.player.update_inventory(liquid_gold, "add")
            self.player.update_inventory(bucket, "remove")
            print(self.cow.print_response(self.cow.name, 'dairy_bucket'))
        else:
            print(self.cow.print_response(self.cow.name, 'dairy_no_bucket'))

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
        self.cow.print_response(self.cow.name, 'intro')
        attempts = 2
        total_tip = 0
        while attempts > 0:
            print("1. Tip the cow")
            print("2. Run")

            choice = input("Choose an action (1-2): ")

            if choice == "1":
                try:
                    tip_amount = float(input("How much do you want to tip the cow? "))
                    if (tip_amount <= 0):
                        print("You decided not to tip the cow.\n")
                        attempts = -1
                    else:
                        tip_amount = float(tip_amount)
                        self.player.cash -= tip_amount
                        total_tip += tip_amount

                    if tip_amount >= self.cow.req_amount:
                        score = (2 if attempts == 2 else 1) * (2 if tip_amount > 20 else 1)
                        self.cow.likeliness += score
                        self.game_instance.update_cow_scores(self.cow, score)
                        self.cow.print_response(self.cow.name, 'graceful')
                        return
                    else:
                        attempts -= 1
                        if (attempts == 0):
                            self.cow.likeliness -= 1
                            self.game_instance.update_cow_scores(self.cow, -1)
                        tip_amount = float(tip_amount)
                        self.player.cash -= tip_amount
                        print(f'The cow is disappointed with your tip. You have ${int(self.player.cash)} left.\n')
                        self.cow.print_response(self.cow.name, 'counter')
                except ValueError:
                    print("Please enter a number.\n")
            elif choice == "2":
                print("You decided to run away from the cow.\n")
                self.game_instance.update_cow_scores(self.cow, -2)
                return
            else:
                print("Please enter a number between 1 and 2.")
