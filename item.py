import random

class Item:
    def __init__(self, name, item_type):
        self.name = name
        self.item_type = item_type

class Weapon(Item):
    def __init__(self, name, min_damage, max_damage, rarity):
        super().__init__(name, 'weapon')
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.rarity = rarity

class Shield(Item):
    def __init__(self, name, min_defense, max_defense, rarity):
        super().__init__(name, 'shield')
        self.min_defense = min_defense
        self.max_defense = max_defense
        self.rarity = rarity

class Tool(Item):
    def __init__(self, name, action):
        super().__init__(name, 'tool')
        self.action = action

class Object(Item):
    def __init__(self, name, description):
        super().__init__(name, 'object')
        self.description = description

def random_weapon_roll(less_likely=False):
    weapons = [
        {'name': 'dagger', 'min_dmg': 1, 'max_dmg': 10, 'max_scale': 3},
        {'name': 'short bow', 'min_dmg': 2, 'max_dmg': 15, 'max_scale': 2},
        {'name': 'sword', 'min_dmg': 3, 'max_dmg': 25, 'max_scale': 4}
    ]
    weapon = random.choice(weapons)
    weights = [50, 30, 15, 5] if not less_likely else [75, 20, 4, 1]
    scale = random.choices([1, 2, 3, 4], weights=weights)[0]
    max_damage = min(weapon['max_dmg'], weapon['min_dmg'] + scale)
    rarity = scale
    return Weapon(weapon['name'], weapon['min_dmg'], max_damage, rarity)


def random_shield_roll(less_likely=False):
    shields = [
        {'name': 'wooden shield', 'min_def': 1, 'max_def': 5, 'max_scale': 3},
        {'name': 'funny shield', 'min_def': 2, 'max_def': 10, 'max_scale': 3},
        {'name': 'hilarious shield', 'min_def': 4, 'max_def': 12, 'max_scale': 4}
    ]
    shield = random.choice(shields)
    weights = [50, 30, 15, 5] if not less_likely else [75, 20, 4, 1]
    scale = random.choices([1, 2, 3, 4], weights=weights)[0]
    max_defense = min(shield['max_def'], shield['min_def'] + scale)
    rarity = scale
    return Shield(shield['name'], shield['min_def'], max_defense, rarity)

def random_item_roll():
    item_type = random.choices(
        ['weapon', 'shield', 'tool', 'object'],
        weights=[35, 35, 10, 20]
    )[0]
    if item_type == 'weapon':
        return random_weapon_roll(less_likely=true)
    elif item_type == 'shield':
        return random_shield_roll(less_likely=true)
    elif item_type == 'tool':
        return random_tool_roll()
    else:
        return random_object_roll()

