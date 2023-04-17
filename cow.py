import random
from assets.context import cow_sayings, cow_names, approaches

class Cow:
    def __init__(self, game_terminal, name, req_amount, likeliness, strength, hp, cash, is_shop, is_aggro, pack, approach):
        self.game_terminal = game_terminal
        self.name = name
        self.req_amount = req_amount
        self.likeliness = likeliness
        self.strength = strength
        self.hp = hp
        self.max_hp = hp
        self.cash = cash
        self.is_shop = is_shop
        self.is_aggro = is_aggro
        self.pack = pack
        self.approach = approach
        self.mood = self.set_mood(self.likeliness)

    @staticmethod
    def generate_random_cow_properties(player):
        likeliness = Cow.set_random_likeliness()
        max_strength = max(int(player.hp * 0.25), int(player.cash // 20))
        strength = random.randint(3, max_strength) if 3 < max_strength else 3
        hp = max(10, strength * random.randint(1, 2) * (2 if likeliness < 5 else 1)) + random.randint(1, 3) * int(player.cash % 20)
        is_aggro = random.randint(0, 99) < 15 + int(player.cash / 20)
        is_shop = random.randint(0, 99) < 15 if not is_aggro else False

        return {
            "name": random.choice(cow_names),
            "req_amount": (random.randint(3, 12) + 5 * player.cash % 25),
            "likeliness": likeliness,
            "strength": strength,
            "hp": hp,
            "cash": random.choices([random.randint(strength, hp), random.randint(strength, hp) * 2], weights=[0.40, 0.60])[0],
            "is_shop": is_shop,
            "is_aggro": is_aggro,
            "pack": random.randint(1, 6),
            "approach": random.choice(approaches)
        }

    @staticmethod
    def set_random_likeliness():
        mood_base = 5
        mood_weights = [10, 80, 10]
        mood_offsets = random.choices([-2, 0, 2], weights=mood_weights)[0]
        return mood_base + mood_offsets

    def set_mood(self, likeliness):
        return 'upset' if likeliness <= 4 else 'friendly' if likeliness >= 7 else 'neutral'

    def tip(self, amount):
        response = 'graceful' if amount >= self.req_amount else 'counter'
        self.likeliness += (amount >= self.req_amount)
        return self.get_response(response)

    def get_response(self, response_type):
        return random.choice(cow_sayings[self.mood][response_type])

    def get_approach(self):
        print(f'\n{self.approach}')
        self.game_terminal.draw_dialog(self.approach)
        self.game_terminal.refresh()

    def print_response(self, cow_name, response_type, gap=True):
        print(f"{cow_name}: {self.get_response(response_type)}" + ('\n' if gap else ''))
        self.game_terminal.draw_dialog(self.get_response(response_type))
        
    def get_combat_stats(self):
        hp_str = f"{self.hp}/{self.max_hp}" if self.hp != self.max_hp else f"{self.hp}"
        return f"{self.name} | {self.strength} STR | {hp_str} HP"

    def get_mood_status(self):
        return f"{self.name} | {self.mood}."
        