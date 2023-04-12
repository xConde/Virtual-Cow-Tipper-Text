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
        self.type = 'weapon'

    def stats(self):
        return f"{self.name} (L: {self.min_damage}, H: {self.max_damage}, Rarity: {self.rarity})"

    def is_upgrade(self, player, item):
        if not player.weapon or player.weapon and find_median_stat(item) > find_median_stat(player.weapon):
            return True
        return False


class Shield(Item):
    def __init__(self, name, min_defense, max_defense, rarity):
        super().__init__(name, 'shield')
        self.min_defense = min_defense
        self.max_defense = max_defense
        self.rarity = rarity
        self.type = 'shield'

    def stats(self):
        return f"{self.name} (L: {self.min_defense}, H: {self.max_defense}, Rarity: {self.rarity})"

    def is_upgrade(self, player, item):
        if not player.shield or player.shield and find_median_stat(item) > find_median_stat(player.shield):
            return True
        return False


class Tool(Item):
    def __init__(self, name, action):
        super().__init__(name, 'tool')
        self.action = action
        self.type = 'utility'


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
        self.type = 'product'


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

RARITY_ADJECTIVES = {
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
    prefix_or_suffix = random.choice(['prefix', 'suffix'])
    adjective = random.choice(RARITY_ADJECTIVES[rarity][prefix_or_suffix])
    return f'{adjective} {base_name}'.strip() if prefix_or_suffix == 'prefix' else f'{base_name} {adjective}'.strip()


def build_item(item_type: str, less_likely: bool = False):
    if item_type not in ['weapon', 'shield', 'tool', 'object']:
        raise ValueError('Invalid item type.')

    item_list = WEAPON_TYPES if item_type == 'weapon' else SHIELD_TYPES
    item_weights = [35, 28, 24, 15, 12, 9, 6, 4, 2, 1] if not less_likely else [
        40, 30, 20, 10, 5, 3, 2, 1, 1, 1]
    item_index = random.choices(range(len(item_list)), weights=item_weights)[0]
    base_item = item_list[item_index]

    weights = [60, 35, 10, 4, 1] if not less_likely else [72, 32, 3, 2, 1]
    scale = random.choices([1, 2, 3, 4, 5], weights=weights)[0]
    rarity = list(RARITY_ADJECTIVES.keys())[scale - 1]

    stat_key = 'min_dmg' if item_type == 'weapon' else 'min_def'
    min_stat = base_item[stat_key]
    max_stat = min(base_item['max_' + stat_key[-3:]], min_stat + scale)

    item = Weapon(base_item['name'], min_stat, max_stat, rarity) if item_type == 'weapon' else Shield(
        base_item['name'], min_stat, max_stat, rarity)
    item.name = get_modified_name(item.name, rarity, item_type)

    return item


def find_median_stat(item):
    stat_key = 'min_dmg' if item.type == 'weapon' else 'min_def'
    min_stat = base_item[stat_key]
    max_stat = min(base_item['max_' + stat_key[-3:]], min_stat + scale)

    min_item_ = item.min_damage + int(item.min_damage * item.rarity * 0.1)
    max_item_ = item.max_damage + int(item.max_damage * item.rarity * 0.15)
    median_item_ = (min_item_ + max_item_) // 2
    return median_item_ / 3


def roll_weapon_dmg(weapon) -> int:
    if not weapon:
        return 0

    min_dmg = weapon.min_damage + int(weapon.min_damage * weapon.rarity * 0.1)
    max_dmg = weapon.max_damage + int(weapon.max_damage * weapon.rarity * 0.15)
    return random.randint(min_dmg, max_dmg)


def random_item_roll(less_likely):
    weights = [35, 30, 32, 3] if not less_likely else [63, 15, 20, 2]
    item_type = random.choices(
        ['weapon', 'shield', 'tool', 'object'], weights=weights)[0]
    if item_type == 'weapon':
        return build_item('weapon', less_likely)
    elif item_type == 'shield':
        return build_item('shield', less_likely)
    elif item_type == 'tool':
        return random_tool_roll()
    else:
        return random_object_roll()


def get_shop_items(cow_mood: str, player_cash: float, isLucky: bool):
    price = random.randint(20, 25) + 3 * int(player_cash // 50)
    price_multiplier = 1 if cow_mood != 'upset' else 2
    less_likely = False if isLucky and cow_mood != 'neutral' else True
    items = [
        {"label": "random item", "item": random_item_roll(
            less_likely), "price_multiplier": 1 * price_multiplier},
        {"label": "random weapon", "item": build_item(
            'weapon', less_likely=False), "price_multiplier": 1.5 * price_multiplier},
        {"label": "random shield", "item": build_item(
            'shield', less_likely=False), "price_multiplier": 2 * price_multiplier},
    ]

    for item in items:
        item["price"] = price * item["price_multiplier"]

    return items


def random_tool_roll():
    tools = [CowBell(), Bucket()]
    return random.choice(tools)


def random_object_roll():
    objects = [LiquidGold()]
    return random.choice(objects)
