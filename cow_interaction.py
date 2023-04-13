import random
from item import CowBell, Bucket, random_item_roll, get_shop_items


class CowAttack:
    def __init__(self, name, damage=None, effect=None, duration=None, healing=None, accuracy=100):
        self.name = name
        self.damage = damage
        self.effect = effect
        self.duration = duration
        self.healing = healing
        self.accuracy = accuracy

    @classmethod
    def generate_cow_combat_styles(cls, cow_strength):
        return [
            cls("headbutt", damage=random.randint(3, 2 + cow_strength), accuracy=85),
            cls("hoof kick", damage=random.randint(5, 4 + cow_strength), accuracy=60),
            cls("tail whip", damage=random.randint(1, 1 + cow_strength // 2), accuracy=95),

            cls("stunning bellow", effect="stun", duration=1, accuracy=75),
            cls("paralyzing stare", effect="stun", duration=random.randint(1, 3), accuracy=60),
            cls("milk rejuvenation", effect="heal", healing=random.randint(3, 3 + int(cow_strength * 0.5)), accuracy=100),
            cls("power-up snort", effect="power_up", accuracy=100),

            cls("moo of doom", damage=random.randint(4, 4 + int(cow_strength * 1.5)), accuracy=65),
            cls("haymaker", damage=random.randint(6, 5 + int(cow_strength * 1.7)), accuracy=75),
            cls("bull rush", damage=random.randint(5, 5 + int(cow_strength * 2)), accuracy=80),
        ]

    @classmethod
    def cow_attack(cls, player, cow):
        cow_combat_styles = cls.generate_cow_combat_styles(cow.strength)
        attack_weights = [25, 15, 18, 9, 9, 9, 9, 3, 2, 1]
        chosen_attack = random.choices(cow_combat_styles, weights=attack_weights, k=1)[0]

        hit_chance = random.randint(0, 100)
        if hit_chance <= chosen_attack.accuracy:
            if chosen_attack.damage:
                player.hp -= chosen_attack.damage
                print(f"{cow.name} uses {chosen_attack.name} and deals {chosen_attack.damage} damage to {player.name}!")

            if chosen_attack.effect:
                if chosen_attack.effect == "stun":
                    print(f"{player.name} is stunned for {chosen_attack.duration} turns!")
                    # Add logic to handle stun effect for the player
                elif chosen_attack.effect == "heal":
                    print(f"{cow.name} heals for {chosen_attack.healing} HP!")
                    cow.hp += chosen_attack.healing
                    # Cap the cow's HP to its maximum HP
                    cow.hp = min(cow.hp, cow.max_hp)
                elif chosen_attack.effect == "power_up":
                    print(f"{cow.name} powers up")
        else:
            print(f"{cow.name} uses {chosen_attack.name} but misses {player.name}!")


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
        
        cow_type = "aggro" if self.cow.is_aggro else "shop" if self.cow.is_shop else "dairy" if self.calculate_dairy_chance() else "tip_or_leave"
        handler = handlers[cow_type]
        
        self.game_instance.player.display_info(combat=self.cow.is_aggro)
        handler()

    def calculate_dairy_chance(self):
        cow_bell = self.get_cow_bell()
        dairy_encounter_chance = 5 if not cow_bell else 15
        is_dairy = random.randint(0, 99) < dairy_encounter_chance
        if is_dairy:
            if cow_bell:
                rand_destroy = random.randint(0, 99) < 5 + int(self.player.cash) // 20
                print(f'Your cowbell helps attract the cow.')
                if rand_destroy:
                    print('The cowbell breaks in the process.')
                    self.player.inventory.remove(cow_bell)
            else:
                print('You hear a dairy cow mooing in the distance.')
        return is_dairy

    def handle_dairy(self):
        bucket = self.get_bucket()
        if bucket:
            liquid_gold = bucket.use()
            self.player.update_inventory(liquid_gold, "add")
            self.player.update_inventory(bucket, "remove")
            print(f"You milk {self.cow.name} with your bucket and obtain liquid gold.")
            self.cow.print_response(self.cow.name, 'dairy_bucket')
        else:
            print(f"You encounter a dairy cow named {self.cow.name}, but you don't have a bucket to milk it.")
            self.cow.print_response(self.cow.name, 'dairy_no_bucket')

    def handle_combat(self):
        print(f"A combat with '{self.cow.name}' has started!")

        cow_strength = self.cow.strength

        while self.player.hp > 0 and self.cow.hp > 0:
            print("\n1. Attack | 2. Check inventory | 3. Use an item from inventory | 4. Flee")
            choice = input("Choose an action (1-4): ")

            if choice.isdigit() and int(choice) in range(1, 5):
                choice = int(choice)
                if choice == 1:
                    self.player.deal_damage(self.cow)
                    if self.cow.hp <= 0:
                        print(f"You defeat {self.cow.name}.")
                        self.cow.print_response(self.cow.name, 'enraged_end')
                        print(f"You gain ${self.cow.cash}.")
                        self.player.cash += self.cow.cash
                        break
                elif choice == 2:
                    check_inventory(self.player)
                elif choice == 3:
                    use_item(self.player)
                elif choice == 4:
                    print("You flee from the combat.")
                    break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
            
            if self.cow.hp > 0:
                CowAttack.cow_attack(self.player, self.cow)
                
    def handle_shop(self):
        print(f'You enter a shop run by a cow named {self.cow.name} who is currently {self.cow.mood}.')
        self.cow.print_response(self.cow.name, 'shop_keeper_intro')
        isLucky = random.randint(0, 99) < (40 if self.cow.mood == 'upset' else 25)
        if (self.cow.mood == 'friendly' and isLucky):
            print(f"The shop owner is very welcoming and shows you all the items in their shop with a smile.")
        elif (self.cow.mood == 'upset' and isLucky):
            print(f"{self.cow.name} grudgingly charges extra, but you're feeling lucky.")
        while True:
            print("Items available:")
            available_items = get_shop_items(self.cow.mood, self.player.cash, isLucky)
            item_strings = []
            for i, item in enumerate(available_items):
                item_name = item['label'] if self.cow.mood != 'friendly' else item['item'].name
                price = item["price"]
                item_strings.append(f"{i + 1}. {item_name} - ${price}")
            print(" | ".join(item_strings) + " | 4. Leave the shop")

            choice = input("Choose an action (1-4): ")
            if choice.isdigit() and int(choice) in range(1, 5):
                choice = int(choice)
                if choice == 4:
                    self.cow.print_response(self.cow.name, 'shop_keeper_end')
                    return

                item_choice = available_items[choice - 1]
                item_price = item_choice['price']
                if self.player.cash >= item_price:
                    self.player.cash -= item_price
                    self.player.add_item_to_inventory(item_choice['item'])
                    self.cow.print_response(self.cow.name, 'shop_keeper_purchase')
                    if item_choice['item'].type in ['weapon', 'shield']:
                        print(f"You purchased a {item_choice['item'].stats()} for ${item_price}.")
                    else:
                        print(f"You purchased {item_choice['item'].name} for ${item_price}.")
                    print(f"Remaining cash: ${self.player.cash}\n")
                else:
                    print("You don't have enough cash for that item.\n")
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

    def handle_tip_or_leave(self):
        print(f'You encounter a cow named {self.cow.name} who is currently {self.cow.mood}.')
        self.cow.print_response(self.cow.name, 'intro')
        attempts = 2
        total_tip = 0
        while attempts > 0:
            print("1. Tip the cow | 2. Run")

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
                        print(f'You tipped {self.cow.name} ${int(total_tip)}. The cow is happy with your tip. You have ${int(self.player.cash)} left.')
                        self.cow.print_response(self.cow.name, 'graceful')
                        return
                    else:
                        attempts -= 1
                        tip_amount = float(tip_amount)
                        self.player.cash -= tip_amount
                        print(f"{self.cow.name} is disappointed with your tip{' of $'+str(int(total_tip)) if total_tip > 0 else ''}. You have ${int(self.player.cash)} left.")
                        if (attempts == 0):
                            self.cow.likeliness -= 1
                            self.game_instance.update_cow_scores(self.cow, -1)
                            print(f"...{self.cow.name} runs away.")
                        else:
                             print("...The cow looks at you expectantly, waiting for more money.")
                        self.cow.print_response(self.cow.name, 'counter')
                except ValueError:
                    print("Please enter a number.\n")
            elif choice == "2":
                print("You decided to run away from the cow.\n")
                self.game_instance.update_cow_scores(self.cow, -2)
                return
            else:
                print("Please enter a number between 1 and 2.")

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

