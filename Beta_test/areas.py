# areas.py
import random
from pokemon_data import POKEMON_DATA

# -----------------------
# Define Areas and Pokémon
# -----------------------
AREAS = {
    "Forest": ["Bulbasaur", "Caterpie", "Pidgey", "Rattata", "Pikachu"],
    "Cave": ["Zubat", "Geodude", "Onix", "Machop", "Graveler"],
    "Tower": ["Gastly", "Haunter", "Drowzee", "Hypno", "Gengar"],
    "Beach": ["Squirtle", "Psyduck", "Krabby", "Tentacool", "Seel"]
}

# -----------------------
# Wild Pokémon Class
# -----------------------
class WildPokemon:
    def __init__(self, name, level):
        self.name = name
        self.level = level

# -----------------------
# Encounter System
# -----------------------
def encounter(area_name, max_level=5):
    if area_name not in AREAS:
        raise ValueError(f"No such area: {area_name}")
    
    pokemon_name = random.choice(AREAS[area_name])
    base_level = POKEMON_DATA.get(pokemon_name, {}).get("level", 1)
    level = random.randint(base_level, min(base_level + 3, max_level))
    
    return WildPokemon(pokemon_name, level)

# -----------------------
# Area Sequence (Stage order)
# -----------------------
def get_area_for_stage(stage_number):
    if 1 <= stage_number <= 10:
        return "Forest"
    elif 11 <= stage_number <= 20:
        return "Cave"
    elif 21 <= stage_number <= 30:
        return "Tower"
    elif 31 <= stage_number <= 40:
        return "Beach"
    elif 41 <= stage_number <= 50:
        return "Tower"
    else:
        return "Unknown"