# game.py
import random
from typing import List, Optional
from pokemon import Pokemon, Move, Pokeball, Potion
from pokemon_data import POKEMON_DATA

# ---------- Stage / Area ----------
def get_area_for_stage(stage_number: int) -> str:
    if 1 <= stage_number <= 10: return "Forest"
    elif 11 <= stage_number <= 20: return "Cave"
    elif 21 <= stage_number <= 30: return "Tower"
    elif 31 <= stage_number <= 40: return "Beach"
    elif 41 <= stage_number <= 50: return "Tower"
    return "Unknown"

# ---------- Build Pokémon ----------
def build_pokemon_from_species(species_name: str, level: Optional[int] = None) -> Pokemon:
    data = POKEMON_DATA.get(species_name)
    if not data: raise ValueError(f"Unknown species: {species_name}")

    level = level or data.get("level", 1)
    
    moves_list = []
    for lvl, move_names in data.get("moves", {}).items():
        if lvl <= level:
            for mname in move_names:
                move_type = data["type"][0] if data.get("type") else "Normal"
                power = (len(mname) % 10) + 5
                moves_list.append(Move(mname, power, move_type))
    
    p = Pokemon(species_name, level)
    p.base_stats = data.get("base_stats", {"hp":10,"attack":5,"defense":5,"speed":5})
    p.types = data.get("type", ["Normal"])
    p.moves = moves_list
    p.max_hp = p.base_stats.get("hp", 10) + p.level * 2
    p.hp = p.max_hp
    p.catch_rate = lambda: random.random() < 0.9 * (1 - 0.5 * (p.hp/p.max_hp))
    return p

# ---------- Player ----------
class Player:
    def __init__(self, name: str):
        self.name = name
        self.team: List[Pokemon] = []
        self.items = {"Potion": 3, "Pokeball": 5}

    def has_available_pokemon(self) -> bool:
        return any(p.hp > 0 for p in self.team)

    def first_available_pokemon(self) -> Optional[Pokemon]:
        for p in self.team:
            if p.hp > 0: return p
        return None

    def add_pokemon(self, pokemon: Pokemon) -> bool:
        if len(self.team) >= 6: return False
        self.team.append(pokemon)
        return True

    def use_item(self, item_name: str, target: Optional[Pokemon] = None) -> bool:
        if self.items.get(item_name, 0) <= 0: return False
        if item_name == "Potion" and target:
            Potion().use(target)
        elif item_name == "Pokeball" and target:
            self.items[item_name] -= 1
            success = target.catch_rate()
            if success: self.add_pokemon(target)
            return success
        self.items[item_name] -= 1
        return True

# ---------- Enemy ----------
class Enemy:
    def __init__(self, name: str, team: List[Pokemon]):
        self.name = name
        self.team = team

    def choose_pokemon(self) -> Optional[Pokemon]:
        for p in self.team:
            if p.hp > 0: return p
        return None

class WildPokemon(Enemy):
    def __init__(self, pokemon: Pokemon):
        super().__init__(pokemon.name + " (wild)", [pokemon])

# ---------- Rival ----------
def generate_rival_team(stage_level: int, num_pokemon: int = 3) -> Enemy:
    species_list = list(POKEMON_DATA.keys())
    team = []
    selected_species = set()
    for _ in range(num_pokemon):
        available_species = [s for s in species_list if s not in selected_species]
        species = random.choice(available_species or species_list)
        selected_species.add(species)
        base_level = min(stage_level*2,50)
        level = max(1, min(int(base_level*0.4) + random.randint(-2,2),50))
        team.append(build_pokemon_from_species(species, level))
    return Enemy("Rival", team)

# ---------- Battle ----------
class Battle:
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy

    def start_battle(self):
        pkm = self.player.first_available_pokemon()
        ekm = self.enemy.choose_pokemon()
        if not pkm or not ekm: return "no_fighter"

        while pkm and ekm:
            # Player turn
            if pkm.moves:
                move = random.choice(pkm.moves)
                move.use_move(pkm, ekm)
            if ekm.hp <= 0:
                pkm.gain_exp(50)
                ekm = self.enemy.choose_pokemon()
                if not ekm: return "player_win"

            # Enemy turn
            if ekm and ekm.moves:
                move_e = random.choice(ekm.moves)
                move_e.use_move(ekm, pkm)
            if pkm.hp <= 0:
                pkm = self.player.first_available_pokemon()
                if not pkm: return "enemy_win"
        return "finished"

# ---------- Map Stage ----------
class MapStage:
    def __init__(self, stage_number: int):
        self.stage_number = stage_number
        self.location = get_area_for_stage(stage_number)

    def random_event(self) -> WildPokemon:
        wild_species_name = random.choice(list(POKEMON_DATA.keys()))
        level = random.randint(1, self.stage_number)
        return WildPokemon(build_pokemon_from_species(wild_species_name, level))

# ---------- Full Game Flow ----------
class Game:
    def __init__(self, player_name: str = "Player", total_stages: int = 50):
        self.player = Player(player_name)
        self.total_stages = total_stages
        self.stage_index = 1
        self.stages = [MapStage(i+1) for i in range(total_stages)]
        self.is_over = False
        self.boss_stages = [10,20,30,40,50]
        self.rival_stages = [5,15,25,35,45]

    def next_stage(self) -> Optional[Enemy]:
        if self.stage_index > self.total_stages:
            self.is_over = True
            return None

        # Boss Stage
        if self.stage_index in self.boss_stages:
            boss_map = {10:"BossMon_Form1", 20:"BossMon_Form2", 30:"BossMon_Form2",
                        40:"BossMon_Form3", 50:"BossMon_Form3"}
            boss_species = boss_map.get(self.stage_index, "BossMon_Form1")

            if boss_species not in POKEMON_DATA:
                POKEMON_DATA[boss_species] = {
                    "type":["Normal"],
                    "base_stats":{"hp":100,"attack":50,"defense":50,"speed":30},
                    "moves":{1:["Tackle"]},
                    "level":1
                }

            enemy = build_pokemon_from_species(boss_species, level=min(50,self.stage_index*2))
            enemy.max_hp = int(enemy.max_hp * 0.4)
            enemy.hp = enemy.max_hp
            self.stage_index += 1
            return Enemy("Boss", [enemy])

        # Rival Stage
        if self.stage_index in self.rival_stages:
            enemy = generate_rival_team(self.stage_index)
            for p in enemy.team:
                p.max_hp = int(p.max_hp * 0.4)
                p.hp = p.max_hp
            self.stage_index += 1
            return enemy

        # Normal Stage
        enemy = self.stages[self.stage_index-1].random_event()
        self.stage_index += 1
        return enemy