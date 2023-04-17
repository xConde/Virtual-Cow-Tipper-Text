
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
