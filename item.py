import random


class Item:
    def __init__(self, name, item_type):
        self.name = name
        self.item_type = item_type


class Potion(Item):
    def __init__(self, name, stat, boost_amount, duration=None):
        super().__init__(name, 'potion')
        self.stat = stat
        self.boost_amount = boost_amount
        self.duration = duration
        self.type = 'potion'

class Weapon(Item):
    def __init__(self, name, min_damage, max_damage, rarity, scale):
        super().__init__(name, 'weapon')
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.rarity = rarity
        self.scale = scale
        self.type = 'weapon'

    def stats(self):
        return f"{self.name} (L: {self.min_damage}, H: {self.max_damage}, Rarity: {self.rarity})"

    def is_upgrade(self, player, item):
        if not player.weapon or player.weapon and find_median_stat(item) > find_median_stat(player.weapon):
            return True
        return False


class Shield(Item):
    def __init__(self, name, min_defence, max_defence, rarity, scale):
        super().__init__(name, 'shield')
        self.min_defence = min_defence
        self.max_defence = max_defence
        self.rarity = rarity
        self.scale = scale
        self.type = 'shield'

    def stats(self):
        return f"{self.name} (L: {self.min_defence}, H: {self.max_defence}, Rarity: {self.rarity})"

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
    {'name': 'dagger', 'min_damage': 1, 'max_damage': 4},
    {'name': 'club', 'min_damage': 2, 'max_damage': 6},
    {'name': 'short bow', 'min_damage': 3, 'max_damage': 8},
    {'name': 'mace', 'min_damage': 4, 'max_damage': 10},
    {'name': 'longbow', 'min_damage': 5, 'max_damage': 12},
    {'name': 'battleaxe', 'min_damage': 6, 'max_damage': 14},
    {'name': 'flail', 'min_damage': 7, 'max_damage': 16},
    {'name': 'halberd', 'min_damage': 8, 'max_damage': 18},
    {'name': 'greatsword', 'min_damage': 9, 'max_damage': 20},
    {'name': 'godsword', 'min_damage': 10, 'max_damage': 22}
]

SHIELD_TYPES = [
    {'name': 'buckler', 'min_defence': 1, 'max_defence': 4},
    {'name': 'targe', 'min_defence': 2, 'max_defence': 6},
    {'name': 'round shield', 'min_defence': 3, 'max_defence': 8},
    {'name': 'heater shield', 'min_defence': 4, 'max_defence': 10},
    {'name': 'kite shield', 'min_defence': 5, 'max_defence': 12},
    {'name': 'tower shield', 'min_defence': 6, 'max_defence': 14},
    {'name': 'pavise', 'min_defence': 7, 'max_defence': 16},
    {'name': 'spiked shield', 'min_defence': 8, 'max_defence': 18},
    {'name': 'barrier shield', 'min_defence': 9, 'max_defence': 20},
    {'name': 'aegis', 'min_defence': 10, 'max_defence': 22}
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

    stat_key = 'min_damage' if item_type == 'weapon' else 'min_defence'
    min_stat = base_item[stat_key]
    max_stat = min(base_item['max_' + stat_key[4:]], min_stat)

    item_obj = {'name': base_item['name'], str(stat_key): min_stat, str('max_' + stat_key[4:]): max_stat, 'rarity': rarity, 'scale': scale}
    item = Weapon(**item_obj) if item_type == 'weapon' else Shield(**item_obj)
    item.name = get_modified_name(item.name, rarity, item_type)

    return item


def find_median_stat(item):
    stat_key = 'min_damage' if item.type == 'weapon' else 'min_defence'
    min_stat = getattr(item, stat_key)
    max_stat = min(getattr(item, 'max_' + stat_key[4:]), min_stat + item.scale)

    min_item_ = item.min_damage + int(item.min_damage * item.scale * 0.25)
    max_item_ = item.max_damage + int(item.max_damage * item.scale * 0.6)
    median_item_ = (min_item_ + max_item_) // 2
    return median_item_ / 3


def roll_weapon_dmg(weapon) -> int:
    if not weapon:
        return 0

    min_damage = weapon.min_damage + int(weapon.min_damage * weapon.scale * 0.25)
    max_damage = weapon.max_damage + int(weapon.max_damage * weapon.scale * 0.6)
    return random.randint(min_damage, max_damage)


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
