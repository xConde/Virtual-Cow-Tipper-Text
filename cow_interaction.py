import random
import time
import os
import msvcrt
from item import CowBell, Bucket, random_item_roll, get_shop_items
from assets.context import cow_names

# rarity should raise the floor for items rare dag should not be min 1

# should be able to sell at the shop
class CowGames:
    def __init__(self, player, cow):
        self.player = player
        self.cow = cow

    def play_random_mini_game(self, bet_amount):
        mini_games = ['tipping_bar', 'cow_race', 'guessing_game']
        selected_game = random.choice(mini_games)
        return getattr(self, selected_game)(bet_amount)

    def tipping_bar(self, bet_amount):
        max_tip = bet_amount * 3
        time_interval = max(0.05, 0.3 - 0.01 * bet_amount)
        return self._tipping_bar(bet_amount, max_tip, time_interval)

    def _tipping_bar(self, tip_amount, max_tip, time_interval):
        bar_length = 40
        cow_face_position = random.randint(5, bar_length - 10)
        target_position = random.randint(5, bar_length - 10)

        while abs(cow_face_position - target_position) < 5:
            target_position = random.randint(5, bar_length - 10)

        arrow_position = 0
        direction = 1

        input(f"Tipping Bar | Press ENTER to stop the arrow at the right spot {tip_amount} / {max_tip} | Press ENTER to start!")
        time.sleep(time_interval)

        while not msvcrt.kbhit():
            arrow_line = [' '] * bar_length
            arrow_line[arrow_position] = '>'

            # Cow face rendering
            cow_face = [
                '      \\^__^/',
                '      ( oo )\\________',
                '        (__)\        )\/\ ',
                '            ||----w |',
                '            ||     ||'
            ]
            cow_face_width = len(cow_face[0])
            for i in range(len(cow_face)):
                cow_face_index = cow_face_position - (cow_face_width // 2) + i
                if cow_face_index >= 0 and cow_face_index < bar_length:
                    cow_face_line = list(cow_face[i])
                    if cow_face_line[0] != ' ':
                        cow_face_line[0] = '|'
                    if cow_face_line[-1] != ' ':
                        cow_face_line[-1] = '|'
                    cow_face_line = ''.join(cow_face_line)
                    arrow_line[cow_face_index] = cow_face_line

            # Display the target
            target = [' '] * bar_length
            target[target_position - 2:target_position + 2] = '|*|-'
            print(''.join(target))

            # Display the arrow
            print(''.join(arrow_line))

            time.sleep(time_interval)
            arrow_position += direction
            if arrow_position == 0 or arrow_position == bar_length - 1:
                direction = -direction

            # Clear the terminal
            os.system('cls' if os.name == 'nt' else 'clear')

        msvcrt.getch()  # clear the key buffer

        # Calculate the tip amount based on whether the arrow_position is within range of the target
        if target_position - 1 <= arrow_position <= target_position + 1:
            tip_amount = arrow_position / (bar_length - 1) * max_tip
        else:
            tip_amount = 0

        return tip_amount
    def cow_race(self, bet_amount):
        race_length = 50
        base_speed = 1
        return self._cow_race(race_length, base_speed)

    def _cow_race(self, race_length, base_speed):
        selected_cow_names = [random.choice(cow_names) for _ in range(3)]

        print("Choose your cow to race with:")
        for i, name in enumerate(selected_cow_names, start=1):
            print(f"{i}. {name}")

        while True:
            try:
                selected_cow = int(input("Enter the number of your choice (1-3): ")) - 1
                if 0 <= selected_cow < 3:
                    break
                else:
                    print("Invalid selection. Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 3.")

        player_cow_position = race_length
        other_cow_positions = [race_length] * 3

        input("Cow Race | Press ENTER to start!")

        while player_cow_position > 0 and not any(pos <= 0 for pos in other_cow_positions):
            os.system('cls' if os.name == 'nt' else 'clear')
            player_cow_position -= base_speed
            other_cow_positions = [pos - random.randint(1, 3) for pos in other_cow_positions]

            print(f"{'🏁'}{' ' * (race_length - 8)}")
            print(f"{' ' * (player_cow_position - 1)}🐄 ({selected_cow_names[selected_cow]})")
            for idx, pos in enumerate(other_cow_positions, start=1):
                if idx - 1 != selected_cow:
                    print(f"{' ' * (pos - 1)}🐄 ({selected_cow_names[idx - 1]})")

            time.sleep(0.5)

        if player_cow_position <= 0:
            print("Congratulations! Your cow won the race!")
            return self.bet_amount * 2
        else:
            print("Your cow lost the race. Better luck next time.")
            return 0

    def guessing_game(self, tip_amount):
        secret_number = random.randint(1, int(tip_amount * 1.5))
        max_guesses = 4
        range_start, range_end = 1, int(tip_amount * 1.5)
        return self._guessing_game(tip_amount, secret_number, max_guesses, range_start, range_end)

    def _guessing_game(self, tip_amount, secret_number, max_guesses, range_start, range_end):
        range_size = range_end - range_start + 1
        guesses = 0
        prev_distance = None
        input(f"Guessing Game | Guess the cow's favorite number between {range_start} and {range_end} | You have {max_guesses} guesses | Press ENTER to start!")
        while guesses < max_guesses:
            try:
                guess = int(input("Enter your guess: "))
                if guess == secret_number:
                    print("You guessed the cow's favorite number!")
                    return tip_amount
                else:
                    guesses += 1
                    remaining_guesses = max_guesses - guesses
                    if remaining_guesses > 0:
                        distance = abs(guess - secret_number) / (range_size - 1)
                        general_hint = ""
                        if distance < 0.1 and range_end > 40:
                            general_hint = "You're very hot!"
                        elif distance < 0.2 and range_end > 20:
                            general_hint = "You're hot!"
                        elif distance < 0.3:
                            general_hint = "You're warm."
                        elif distance < 0.4:
                            general_hint = "You're cool."
                        else:
                            general_hint = "You're cold."
                        
                        warmer_colder_hint = ""
                        if prev_distance is not None:
                            if distance < prev_distance:
                                warmer_colder_hint = "Warmer! "
                            else:
                                warmer_colder_hint = "Colder! "
                        prev_distance = distance

                        print(f"Incorrect! {warmer_colder_hint}{general_hint} You have {remaining_guesses} guesses left.")
                    else:
                        print(f"Sorry, you're out of guesses! The correct number was {secret_number}.")
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print("An error occurred:", e)
        return 0
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
        self.game_instance.destroy_cow()

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
                        self.game_instance.update_cow_scores(self.cow, 1)
                        self.player.cash += self.cow.cash
                        print(f"You defeat {self.cow.name}. You gain ${self.cow.cash}.")
                        self.cow.print_response(self.cow.name, 'enraged_end')
                        break
                elif choice == 2:
                    check_inventory(self.player)
                elif choice == 3:
                    use_item(self.player)
                elif choice == 4:
                    self.game_instance.update_cow_scores(self.cow, -2)
                    print("You flee from the combat.")
                    break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
            
            if self.cow.hp > 0:
                CowAttack.cow_attack(self.player, self.cow)
                
    def handle_shop(self):
        print(f'You enter a shop run by a cow named {self.cow.name} who is currently {self.cow.mood}.')
        self.cow.print_response(self.cow.name, 'shop_keeper_intro', False)
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
                    self.game_instance.destroy_cow()
                    return

                item_choice = available_items[choice - 1]
                item_price = item_choice['price']
                if self.player.cash >= item_price:
                    self.player.cash -= item_price
                    score = 1 + int(item_choice['price'] // 50)
                    self.game_instance.update_cow_scores(self.cow, score)
                    self.player.add_item_to_inventory(item_choice['item'])
                    self.cow.print_response(self.cow.name, 'shop_keeper_purchase', False)
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
        self.cow.print_response(self.cow.name, 'intro', False)

        choice = input("Tip or leave? (1. Tip | 2. Leave): ")
        if choice == "1":
            min_bet = self.cow.req_amount
            max_bet = min(self.player.cash, self.cow.req_amount * random.randint(2,5))

            while True:
                try:
                    bet_amount = float(input(f"How much do you want to bet for the mini-game? (min: ${min_bet}, max: ${max_bet}) "))
                    if bet_amount < min_bet:
                        print(f"Come on, don't be stingy! The cow expects at least ${min_bet}.")
                    elif bet_amount > max_bet:
                        print(f"You can't bet more than ${max_bet}, that's the cow's limit.")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.\n")

            self.player.cash -= bet_amount
            cow_games_instance = CowGames(self.player, self.cow)
            reward = cow_games_instance.play_random_mini_game(bet_amount)

            if reward > bet_amount:
                win_amount = round(reward - bet_amount, 2)
                print(f"Congratulations! You won ${win_amount}!")
                self.player.cash += reward

                if win_amount >= bet_amount * 1.5:
                    score = 2
                elif win_amount >= bet_amount * 0.5:
                    score = 1
                else:
                    score = 0.5

                self.cow.likeliness += score
                self.game_instance.update_cow_scores(self.cow, score)

            else:
                loss_amount = bet_amount - reward
                self.player.cash += reward

                if loss_amount >= bet_amount * 0.5:
                    score = -0.5
                else:
                    score = -1

                self.cow.likeliness += score
                self.game_instance.update_cow_scores(self.cow, score)

        elif choice == "2":
            print(f"You decided to leave {self.cow.name}.")
            score = -2
            self.cow.likeliness += score
            self.game_instance.update_cow_scores(self.cow, score)
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

