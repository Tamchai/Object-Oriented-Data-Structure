class Pokemon:
    def __init__(self, name, level=None):
        pass
    def attack(self, move, defender):
        pass
    def take_damage(self, amount):
        pass
    def level_up(self):
        pass
    def evolve(self):
        pass
    def is_fainted(self):
        pass

class Move:
    def __init__(self, name, power, type_):
        pass
    def use_move(self, attacker, defender):
        pass
    def calculate_damage(self, attacker, defender):
        pass
    def get_type_multiplier(self, defender_type):
        pass

class Item:
    def __init__(self, name):
        pass
    def use(self):
        pass

class Pokeball(Item):
    def __init__(self, name, catch_rate):
        pass
    def use(self):
        pass
    def attempt_catch(self, pokemon):
        pass

class Potion(Item):
    def __init__(self, name):
        pass
    def use(self):
        pass
