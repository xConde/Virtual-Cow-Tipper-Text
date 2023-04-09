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

class CowBell(Tool):
    def __init__(self):
        super().__init__("Cow Bell", None)

    def get_dairy_bonus(self):
        return 15

class Bucket(Tool):
    def __init__(self):
        super().__init__("Bucket", None)

    def use(self):
        return LiquidGold()

class Object(Item):
    def __init__(self, name, description):
        super().__init__(name, 'object')
        self.description = description

class LiquidGold(Object):
    def __init__(self):
        super().__init__("Liquid Gold", "A valuable substance that can be sold at the shop.")

    def get_value(self, player):
        weapon = player.weapon
        if weapon:
            weapon_dps = (weapon.min_damage + weapon.max_damage) / 2
        else:
            weapon_dps = 0
        return 150 + 5 * weapon_dps + 10 * (player.cash // 50)

WEAPON_TYPES = [
    {'name': 'dagger', 'min_dmg': 1, 'max_dmg': 4},
    {'name': 'club', 'min_dmg': 2, 'max_dmg': 6},
    {'name': 'short bow', 'min_dmg': 3, 'max_dmg': 8},
    {'name': 'mace', 'min_dmg': 4, 'max_dmg': 10},
    {'name': 'longbow', 'min_dmg': 5, 'max_dmg': 12},
    {'name': 'battleaxe', 'min_dmg': 6, 'max_dmg': 14},
    {'name': 'flail', 'min_dmg': 7, 'max_dmg': 16},
    {'name': 'halberd', 'min_dmg': 8, 'max_dmg': 18},
    {'name': 'greatsword', 'min_dmg': 9, 'max_dmg': 20},
    {'name': 'godsword', 'min_dmg': 10, 'max_dmg': 22}
]

SHIELD_TYPES = [
    {'name': 'buckler', 'min_def': 1, 'max_def': 4},
    {'name': 'targe', 'min_def': 2, 'max_def': 6},
    {'name': 'round shield', 'min_def': 3, 'max_def': 8},
    {'name': 'heater shield', 'min_def': 4, 'max_def': 10},
    {'name': 'kite shield', 'min_def': 5, 'max_def': 12},
    {'name': 'tower shield', 'min_def': 6, 'max_def': 14},
    {'name': 'pavise', 'min_def': 7, 'max_def': 16},
    {'name': 'spiked shield', 'min_def': 8, 'max_def': 18},
    {'name': 'barrier shield', 'min_def': 9, 'max_def': 20},
    {'name': 'aegis', 'min_def': 10, 'max_def': 22}
]

rarity_adjectives = {
    'common': {
        'prefix': ['Plain', 'Simple', 'Basic'],
        'suffix': ['']
    },
    'uncommon': {
        'prefix': ['Sturdy', 'Polished', 'Reinforced'],
        'suffix': ['of Quality', 'of Precision']
    },
    'magic': {
        'prefix': ['Enchanted', 'Mystic', 'Arcane'],
        'suffix': ['of Power', 'of Sorcery']
    },
    'rare': {
        'prefix': ['Ancient', 'Exquisite', 'Ethereal'],
        'suffix': ['of Legends', 'of the Ancients']
    },
    'lengendairy': {
        'prefix': ['Mythic', 'Astral', 'Ethereal'],
        'suffix': ['of the Ancients', 'of Eons']
    }
}

def get_modified_name(base_name, rarity, item_type):
    if item_type not in ['weapon', 'shield']:
        raise ValueError("Invalid item_type: must be 'weapon' or 'shield'")

    prefix_or_suffix = random.choice(['prefix', 'suffix'])
    adjective = random.choice(RARITY_ADJECTIVES[rarity][prefix_or_suffix])
    return f'{adjective} {base_name}'.strip() if prefix_or_suffix == 'prefix' else f'{base_name} {adjective}'.strip()

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

def random_tool_roll():
    tools = [CowBell(), Bucket()]
    return random.choice(tools)

def random_object_roll():
    objects = [LiquidGold()]
    return random.choice(objects)

def random_item_roll():
    item_type = random.choices(
        ['weapon', 'shield', 'tool', 'object'],
        weights=[50, 34, 15, 1]
    )[0]
    if item_type == 'weapon':
        return random_weapon_roll(less_likely=True)
    elif item_type == 'shield':
        return random_shield_roll(less_likely=True)
    elif item_type == 'tool':
        return random_tool_roll()
    else:
        return random_object_roll()

def roll_weapon_dmg(weapon) -> int:
    if not weapon:
        return 0

    min_dmg = weapon.min_dmg + int(weapon.min_dmg * weapon.scale * 0.1)
    max_dmg = weapon.max_dmg + int(weapon.max_dmg * weapon.scale * 0.15)
    return random.randint(min_dmg, max_dmg)
