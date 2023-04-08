import random
from assets.context import cow_sayings, cow_names

class Cow:
    def __init__(self, name, req_amount, likeliness, strength, hp, is_shop, is_aggro, pack):
        self.name = name
        self.req_amount = req_amount
        self.likeliness = likeliness
        self.strength = strength
        self.hp = hp
        self.is_shop = is_shop
        self.is_aggro = is_aggro
        self.pack = pack
        self.mood = self.set_mood(self.likeliness)

    @staticmethod
    def generate_random_cow_properties(player):
        is_aggro = random.randint(0, 99) < 15 + int(player.cash / 20)
        is_shop = random.randint(0, 99) < 15 if not is_aggro else False
        max_strength = max(int(player.hp * 0.25), player.cash // 20)
        strength = random.randint(3, max_strength) if 3 < max_strength else 3
        likeliness = Cow.set_random_likeliness()

        return {
            "name": random.choice(cow_names),
            "req_amount": (random.randint(1, 20) + player.cash % 50),
            "likeliness": likeliness,
            "strength": strength,
            "hp": max(10, strength * random.randint(1, 2) * (2 if likeliness < 5 else 1)),
            "is_shop": is_shop,
            "is_aggro": is_aggro,
            "pack": random.randint(1, 6)
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

    def get_intro(self):
        return self.get_response('intro')

    def get_counter(self):
        return self.get_response('counter')

    def get_graceful_end(self):
        return self.get_response('graceful')

    def get_dairy_response(self, has_bucket):
        response_type = 'dairy_bucket' if has_bucket else 'dairy_no_bucket'
        return self.get_response(response_type)

    def get_enraged_intro(self):
        return self.get_response('enraged_intro')

    def get_enraged_end(self):
        return self.get_response('enraged_end')

    def get_shop_keeper_intro(self):
        return self.get_response('shop_keeper_intro')

    def get_shop_keeper_purchase(self):
        return self.get_response('shop_keeper_purchase')

    def get_shop_keeper_end(self):
        return self.get_response('shop_keeper_end')

    def change_mood(self, new_mood):
        self.mood = new_mood

    def likes_player(self):
        return self.likeliness >= 3

    def reset_likeliness(self):
        self.likeliness = 0
