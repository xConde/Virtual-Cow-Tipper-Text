import random
from context import cow_sayings, cow_names

class Cow:
    def __init__(self, name, mood, req_amount):
        self.name = name
        self.mood = mood
        self.req_amount = req_amount
        self.likeliness = 0

    @staticmethod
    def generate_random_cow_properties():

        return {
            "name": Cow.get_random_cow_name(),
            "mood": Cow.set_random_mood(),
            "req_amount": random.randint(1, 20)
        }

    @staticmethod
    def set_req_amount(amount):
        # add variable to increase req_amount by player.cash
        return random.randint(1, 20) 

    @staticmethod
    def set_random_mood():
        mood_base = 5
        mood_weights = [10, 80, 10]
        mood_offsets = random.choices([-2, 0, 2], weights=mood_weights)[0]
        return mood_base + mood_offsets

    @staticmethod
    def get_random_cow_name():
        return random.choice(cow_names)

    def tip(self, amount):
        if amount >= self.req_amount:
            self.likeliness += 1
            return self.get_response('graceful')
        else:
            return self.get_response('counter')

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
