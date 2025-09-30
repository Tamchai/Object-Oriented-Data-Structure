# pokemon.py
import random
import math
from pokemon_data import POKEMON_DATA

# -----------------------
# Type Chart (Pokemon-style type effectiveness)
# -----------------------
TYPE_CHART = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
    "Water": {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
    "Electric": {"Water": 2, "Electric": 0.5, "Grass": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dark": 2, "Steel": 2, "Fairy": 0.5},
    "Poison": {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Fairy": 2},
    "Ground": {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
    "Flying": {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
    "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Fighting": 0.5, "Psychic": 2, "Ghost": 2, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2, "Rock": 2, "Steel": 0.5, "Fairy": 2},
    "Fairy": {"Fire": 0.5, "Fighting": 2, "Poison": 0.5, "Dragon": 2, "Dark": 2, "Steel": 0.5}
}

# -----------------------
# Move Class with Enhanced Damage Calculation
# -----------------------
class Move:
    def __init__(self, name, power, type_, accuracy=100, category="Physical", pp=20):
        self.name = name
        self.power = power
        self.type = type_
        self.accuracy = accuracy
        self.category = category
        self.pp = pp
        self.max_pp = pp

    def use_move(self, attacker, defender):
        # Check accuracy
        if random.random() * 100 > self.accuracy:
            print(f"{attacker.name}'s {self.name} missed!")
            return 0
        
        # Calculate damage
        damage = self.calculate_damage(attacker, defender)
        defender.take_damage(damage)
        
        # Critical hit message
        if hasattr(self, '_was_critical') and self._was_critical:
            print(f"Critical hit!")
        
        # Type effectiveness message
        if hasattr(self, '_effectiveness'):
            if self._effectiveness > 1:
                print(f"It's super effective!")
            elif self._effectiveness < 1 and self._effectiveness > 0:
                print(f"It's not very effective...")
            elif self._effectiveness == 0:
                print(f"It doesn't affect {defender.name}...")
        
        print(f"{attacker.name} used {self.name}! It dealt {damage} damage.")
        
        if defender.is_fainted():
            print(f"{defender.name} fainted!")
            exp_gain = self.calculate_exp_gain(attacker, defender)
            attacker.gain_exp(exp_gain)
        
        return damage

    def calculate_damage(self, attacker, defender):
        # Status moves don't do damage
        if self.category == "Status" or self.power == 0:
            return 0
        
        # Get stats based on move category
        if self.category == "Physical":
            attack_stat = attacker.get_stat("attack")
            defense_stat = defender.get_stat("defense")
        else:  # Special
            attack_stat = attacker.get_stat("sp_attack")
            defense_stat = defender.get_stat("sp_defense")
        
        # Pokemon damage formula
        level = attacker.level
        
        # Base damage calculation (Pokemon formula)
        damage = ((2 * level + 10) / 250) * (attack_stat / defense_stat) * self.power + 2
        
        # STAB (Same Type Attack Bonus)
        stab = 1.5 if self.type in attacker.types else 1.0
        
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(defender.types)
        self._effectiveness = effectiveness
        
        # Critical hit (1/16 chance)
        critical = 1.0
        if random.random() < 0.0625:
            critical = 1.5
            self._was_critical = True
        else:
            self._was_critical = False
        
        random_factor = random.uniform(0.85, 1.0)
        
        other_modifiers = 1.0
        
        # Final damage calculation
        final_damage = damage * stab * effectiveness * critical * random_factor * other_modifiers
        
        return max(1, int(final_damage))

    def get_type_effectiveness(self, defender_types):
        effectiveness = 1.0
        for def_type in defender_types:
            if self.type in TYPE_CHART and def_type in TYPE_CHART[self.type]:
                effectiveness *= TYPE_CHART[self.type][def_type]
        return effectiveness

    def calculate_exp_gain(self, winner, loser):
        base_exp = 50
        level_diff = max(1, loser.level - winner.level + 5)
        exp = base_exp * loser.level * level_diff // 5
        return max(1, exp)

# -----------------------
# Enhanced Pokemon Class
# -----------------------
class Pokemon:
    def __init__(self, name, level=None):
        data = POKEMON_DATA.get(name, {})
        self.name = name
        self.level = level if level else data.get("level", 1)
        self.types = data.get("type", ["Normal"])  # Changed from type to types
        self.evolve_level = data.get("evolve_level")
        self.evolves_to = data.get("evolves_to")
        
        # Base stats (these grow with level)
        self.base_stats = data.get("base_stats", {}).copy()
        
        # IVs (Individual Values) - random for each Pokemon (0-31)
        self.ivs = {
            "hp": random.randint(0, 31),
            "attack": random.randint(0, 31),
            "defense": random.randint(0, 31),
            "sp_attack": random.randint(0, 31),
            "sp_defense": random.randint(0, 31),
            "speed": random.randint(0, 31)
        }
        
        # EVs (Effort Values) - gained through battle
        self.evs = {
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "sp_attack": 0,
            "sp_defense": 0,
            "speed": 0
        }
        
        # Calculate actual stats
        self.calculate_stats()
        self.hp = self.max_hp
        
        # Experience
        self._exp = 0
        self.exp_to_next = self.calculate_exp_needed()
        
        # Moves
        self.moves = self.get_available_moves()
        
        # Status conditions
        self.status = None  # None, "burn", "poison", "paralysis", "sleep", "freeze"
        self.status_counter = 0
        
        self.catch_rate = self.default_catch_rate

    def calculate_stats(self):
        base_hp = self.base_stats.get("hp", 50)
        iv_hp = self.ivs.get("hp", 0)
        ev_hp = self.evs.get("hp", 0)
        self.max_hp = ((2 * base_hp + iv_hp + ev_hp // 4) * self.level // 100) + self.level + 10
        
        base_attack = self.base_stats.get("attack", 50)
        iv_attack = self.ivs.get("attack", 0)
        ev_attack = self.evs.get("attack", 0)
        self.attack_power = ((2 * base_attack + iv_attack + ev_attack // 4) * self.level // 100) + 5
        
        for stat in ["defense", "speed"]:
            base = self.base_stats.get(stat, 50)
            iv = self.ivs.get(stat, 0)
            ev = self.evs.get(stat, 0)
            value = ((2 * base + iv + ev // 4) * self.level // 100) + 5
            setattr(self, stat, value)
        
        self.sp_attack = self.base_stats.get("sp_attack", self.base_stats.get("attack", 50))
        self.sp_defense = self.base_stats.get("sp_defense", self.base_stats.get("defense", 50))

    def get_stat(self, stat_name):
        if stat_name == "attack":
            base_value = self.attack_power
        else:
            base_value = getattr(self, stat_name, 50)
        
        if self.status == "burn" and stat_name == "attack":
            return int(base_value * 0.5)
        elif self.status == "paralysis" and stat_name == "speed":
            return int(base_value * 0.25)
        
        return base_value

    def get_available_moves(self):
        data = POKEMON_DATA.get(self.name, {})
        available = []
        
        for lvl, moves in data.get("moves", {}).items():
            if lvl <= self.level:
                for move_name in moves:
                    # Determine move properties based on name
                    power, move_type, category, accuracy = self.get_move_properties(move_name)
                    move = Move(move_name, power, move_type, accuracy, category)
                    available.append(move)
        
        return available[-4:] if len(available) > 4 else available

    def get_move_properties(self, move_name):
        move_db = {
            # Normal moves
            "Tackle": (40, "Normal", "Physical", 100),
            "Scratch": (40, "Normal", "Physical", 100),
            "Pound": (40, "Normal", "Physical", 100),
            "Quick Attack": (40, "Normal", "Physical", 100),
            "Slash": (70, "Normal", "Physical", 100),
            "Hyper Beam": (150, "Normal", "Special", 90),
            "Body Slam": (85, "Normal", "Physical", 100),
            "Double-Edge": (120, "Normal", "Physical", 100),
            "Hyper Fang": (80, "Normal", "Physical", 90),
            "Super Fang": (1, "Normal", "Physical", 90),  # Special damage calc
            "Skull Bash": (130, "Normal", "Physical", 100),
            
            # Fire moves
            "Ember": (40, "Fire", "Special", 100),
            "Flamethrower": (90, "Fire", "Special", 100),
            "Fire Blast": (110, "Fire", "Special", 85),
            "Fire Spin": (35, "Fire", "Special", 85),
            "Flame Burst": (70, "Fire", "Special", 100),
            
            # Water moves
            "Water Gun": (40, "Water", "Special", 100),
            "Bubble": (40, "Water", "Special", 100),
            "Hydro Pump": (110, "Water", "Special", 80),
            "Tsunami": (120, "Water", "Special", 85),
            
            # Grass moves
            "Vine Whip": (45, "Grass", "Physical", 100),
            "Razor Leaf": (55, "Grass", "Physical", 95),
            "Solar Beam": (120, "Grass", "Special", 100),
            "Leech Seed": (0, "Grass", "Status", 90),
            "Petal Blizzard": (90, "Grass", "Physical", 100),
            "Petal Dance": (120, "Grass", "Special", 100),
            "Absorb": (20, "Grass", "Special", 100),
            "Spore": (0, "Grass", "Status", 100),
            
            # Electric moves
            "Thunder Shock": (40, "Electric", "Special", 100),
            "Thunderbolt": (90, "Electric", "Special", 100),
            "Thunder": (110, "Electric", "Special", 70),
            "Zap Cannon": (120, "Electric", "Special", 50),
            
            # Fighting moves
            "Low Kick": (50, "Fighting", "Physical", 100),
            "Karate Chop": (50, "Fighting", "Physical", 100),
            "Seismic Toss": (60, "Fighting", "Physical", 100),
            "Submission": (80, "Fighting", "Physical", 80),
            
            # Poison moves
            "Poison Sting": (15, "Poison", "Physical", 100),
            "Poison Powder": (0, "Poison", "Status", 75),
            "Acid": (40, "Poison", "Special", 100),
            
            # Ground moves
            "Sand Attack": (0, "Ground", "Status", 100),
            "Dig": (80, "Ground", "Physical", 100),
            "Earthquake": (100, "Ground", "Physical", 100),
            "Mud Shot": (55, "Ground", "Special", 95),
            
            # Flying moves
            "Gust": (40, "Flying", "Special", 100),
            "Wing Attack": (60, "Flying", "Physical", 100),
            "Hurricane": (110, "Flying", "Special", 70),
            "Peck": (35, "Flying", "Physical", 100),
            "Drill Peck": (80, "Flying", "Physical", 100),
            
            # Psychic moves
            "Confusion": (50, "Psychic", "Special", 100),
            "Psybeam": (65, "Psychic", "Special", 100),
            "Psychic": (90, "Psychic", "Special", 100),
            "Hypnosis": (0, "Psychic", "Status", 60),
            "Dream Eater": (100, "Psychic", "Special", 100),
            "Teleport": (0, "Psychic", "Status", 100),
            
            # Bug moves
            "String Shot": (0, "Bug", "Status", 95),
            "Leech Life": (80, "Bug", "Physical", 100),
            "Twineedle": (25, "Bug", "Physical", 100),
            "Fury Attack": (15, "Normal", "Physical", 85),
            
            # Rock moves
            "Rock Throw": (50, "Rock", "Physical", 90),
            "Rock Slide": (75, "Rock", "Physical", 90),
            "Self-Destruct": (200, "Normal", "Physical", 100),
            
            # Ghost moves
            "Lick": (30, "Ghost", "Physical", 100),
            "Night Shade": (50, "Ghost", "Special", 100),
            "Confuse Ray": (0, "Ghost", "Status", 100),
            
            # Dragon moves
            "Dragon Rage": (40, "Dragon", "Special", 100),
            "Dragon Claw": (80, "Dragon", "Physical", 100),
            "Outrage": (120, "Dragon", "Physical", 100),
            
            # Ice moves
            "Aurora Beam": (65, "Ice", "Special", 100),
            "Ice Beam": (90, "Ice", "Special", 100),
            
            # Status moves
            "Growl": (0, "Normal", "Status", 100),
            "Tail Whip": (0, "Normal", "Status", 100),
            "Leer": (0, "Normal", "Status", 100),
            "Defense Curl": (0, "Normal", "Status", 100),
            "Harden": (0, "Normal", "Status", 100),
            "Smokescreen": (0, "Normal", "Status", 100),
            "Withdraw": (0, "Water", "Status", 100),
            "Roar": (0, "Normal", "Status", 100),
            "Bind": (15, "Normal", "Physical", 85),
            "Wrap": (15, "Normal", "Physical", 90),
            "Bite": (60, "Dark", "Physical", 100),
            "Rapid Spin": (50, "Normal", "Physical", 100),
            "Sing": (0, "Normal", "Status", 55),
            "Supersonic": (0, "Normal", "Status", 55),
            "Disable": (0, "Normal", "Status", 100),
            "Stun Spore": (0, "Grass", "Status", 75),
            "Sleep Powder": (0, "Grass", "Status", 75),
            "Sweet Scent": (0, "Normal", "Status", 100),
            "Metronome": (0, "Normal", "Status", 100),
            "Rage": (20, "Normal", "Physical", 100),
            "Horn Attack": (65, "Normal", "Physical", 100),
            "Thrash": (120, "Normal", "Physical", 100),
            "Vice Grip": (55, "Normal", "Physical", 100),
            "Crabhammer": (100, "Water", "Physical", 90),
            "Headbutt": (70, "Normal", "Physical", 100),
            "Fury Swipes": (18, "Normal", "Physical", 80),
        }
        
        if move_name in move_db:
            return move_db[move_name]
        else:
            # Default: moderate power physical move of Pokemon's primary type
            return (50, self.types[0] if self.types else "Normal", "Physical", 100)

    def attack(self, move, defender):
        """Attack another Pokemon with a move"""
        return move.use_move(self, defender)

    def take_damage(self, amount):
        """Take damage and apply status effects"""
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def gain_exp(self, exp):
        """Gain experience and potentially level up"""
        print(f"{self.name} gains {exp} EXP!")
        self._exp += exp
        
        while self._exp >= self.exp_to_next:
            self._exp -= self.exp_to_next
            self.level_up()

    def level_up(self):
        self.level += 1
        old_max_hp = self.max_hp
        old_hp = self.hp
        self.calculate_stats()

        # ปรับ HP ตามสัดส่วน
        if old_hp > 0:
            ratio = old_hp / old_max_hp if old_max_hp > 0 else 1
            self.hp = int(self.max_hp * ratio)
            self.hp = min(self.hp, self.max_hp)
        else:
            self.hp = 0

        self.exp_to_next = self.calculate_exp_needed()

        # --- เช็คสกิลใหม่ ---
        self.pending_new_moves = []  # reset ทุกครั้งเวลาเลเวลอัพ
        data = POKEMON_DATA.get(self.name, {})
        for lvl, moves in data.get("moves", {}).items():
            if lvl == self.level:  # ได้สกิลใหม่พอดี
                for move_name in moves:
                    if move_name not in [m.name for m in self.moves]:
                        power, move_type, category, accuracy = self.get_move_properties(move_name)
                        self.pending_new_moves.append(Move(move_name, power, move_type, accuracy, category))

        # --- เช็คการ evolve ---
        if self.evolve_level and self.level >= self.evolve_level:
            self.evolve()

    def calculate_exp_needed(self):
        """Calculate experience needed for next level"""
        # Using Medium Fast growth rate (similar to many Pokemon)
        return int(self.level ** 3)

    def evolve(self):
        """Evolve into the next form"""
        if self.evolves_to and self.evolves_to in POKEMON_DATA:
            print(f"What? {self.name} is evolving!")
            
            old_name = self.name
            new_data = POKEMON_DATA[self.evolves_to]
            
            # Update Pokemon data
            self.name = self.evolves_to
            self.types = new_data.get("type", ["Normal"])
            self.evolve_level = new_data.get("evolve_level")
            self.evolves_to = new_data.get("evolves_to")
            self.base_stats = new_data.get("base_stats", {}).copy()
            
            # Recalculate stats with new base stats
            self.calculate_stats()
            self.hp = self.max_hp  # Full heal on evolution
            
            # Get new moves
            self.moves = self.get_available_moves()
            
            print(f"{old_name} evolved into {self.name}!")

    def is_fainted(self):
        """Check if Pokemon has fainted"""
        return self.hp <= 0

    def default_catch_rate(self):
        """Calculate catch rate based on HP"""
        hp_factor = self.hp / self.max_hp
        base_catch = 0.3  # Base 30% chance
        
        # Lower HP = higher catch rate
        if hp_factor <= 0.1:
            modifier = 3.0
        elif hp_factor <= 0.25:
            modifier = 2.0
        elif hp_factor <= 0.5:
            modifier = 1.5
        else:
            modifier = 1.0
        
        catch_chance = min(base_catch * modifier, 0.95)  # Max 95% chance
        return random.random() < catch_chance

# -----------------------
# Items
# -----------------------
class Item:
    def __init__(self, name):
        self.name = name

    def use(self):
        pass

class Pokeball(Item):
    def __init__(self, name="Pokeball", catch_rate_modifier=1.0):
        super().__init__(name)
        self.catch_rate_modifier = catch_rate_modifier

    def use(self):
        print(f"{self.name} was thrown!")

    def attempt_catch(self, pokemon):
        # Modified catch rate formula
        hp_factor = pokemon.hp / pokemon.max_hp
        status_bonus = 1.5 if pokemon.status else 1.0
        
        # Base catch rate depends on Pokemon and ball type
        base_rate = 0.3 * self.catch_rate_modifier
        
        # Calculate final catch chance
        catch_chance = base_rate * (2 - hp_factor) * status_bonus
        catch_chance = min(catch_chance, 0.95)  # Cap at 95%
        
        # Shake animation (3 shakes before capture)
        for i in range(3):
            if random.random() > catch_chance:
                print(f"The ball shook {i+1} time(s)...")
                print(f"{pokemon.name} broke free!")
                return False
        
        print(f"Gotcha! {pokemon.name} was caught!")
        return True

class Potion(Item):
    def __init__(self, name="Potion", heal_amount=20):
        super().__init__(name)
        self.heal_amount = heal_amount

    def use(self, pokemon):
        if pokemon.hp >= pokemon.max_hp:
            print(f"{pokemon.name} is already at full HP!")
            return False
        
        old_hp = pokemon.hp
        pokemon.hp = min(pokemon.hp + self.heal_amount, pokemon.max_hp)
        healed = pokemon.hp - old_hp
        print(f"{pokemon.name} recovered {healed} HP!")
        return True

# -----------------------
# Encounter
# -----------------------
def encounter(area_pokemon_list, max_level=10):
    """Generate a wild Pokemon encounter"""
    if not area_pokemon_list:
        raise ValueError("Area has no Pokemon!")
    
    poke_name = random.choice(area_pokemon_list)
    
    if poke_name not in POKEMON_DATA:
        # Fallback to a default Pokemon
        poke_name = "Rattata"
    
    data = POKEMON_DATA[poke_name]
    base_level = data.get("level", 1)
    
    # Random level within range
    level = random.randint(base_level, min(base_level + 5, max_level))
    
    pkm = Pokemon(poke_name, level=level)
    return pkm

# -----------------------
# Enemy Classes
# -----------------------
class Enemy:
    def __init__(self, name, team):
        self.name = name
        self.team = team

    def choose_pokemon(self):
        """Select first available Pokemon"""
        for p in self.team:
            if p.hp > 0:
                return p
        return None

    def make_decision(self, my_pokemon, player_pokemon):
        """AI decision making for battles"""
        # Simple AI: choose most effective move
        if not my_pokemon.moves:
            return None
        
        best_move = None
        best_effectiveness = 0
        
        for move in my_pokemon.moves:
            if move.power > 0:  # Only consider damaging moves
                effectiveness = move.get_type_effectiveness(player_pokemon.types)
                if effectiveness > best_effectiveness:
                    best_effectiveness = effectiveness
                    best_move = move
        
        # If no super effective move, choose highest power
        if not best_move:
            damaging_moves = [m for m in my_pokemon.moves if m.power > 0]
            if damaging_moves:
                best_move = max(damaging_moves, key=lambda m: m.power)
            else:
                best_move = my_pokemon.moves[0]
        
        return best_move

class WildPokemon(Enemy):
    def __init__(self, pokemon):
        super().__init__(f"Wild {pokemon.name}", [pokemon])