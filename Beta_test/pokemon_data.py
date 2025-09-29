# pokemon_data.py

POKEMON_DATA = {
    # ----- Bulbasaur Evolution Line -----
    "Bulbasaur": {
        "level": 5,
        "type": ["Grass", "Poison"],
        "evolve_level": 16,
        "evolves_to": "Ivysaur",
        "base_stats": {"hp": 45, "attack": 49, "defense": 49, "speed": 45},
        "moves": {
            1: ["Tackle", "Growl"],
            5: ["Vine Whip"],
            7: ["Leech Seed"],
            10: ["Poison Powder"],
        },
    },
    "Ivysaur": {
        "level": 16,
        "type": ["Grass", "Poison"],
        "evolve_level": 32,
        "evolves_to": "Venusaur",
        "base_stats": {"hp": 60, "attack": 62, "defense": 63, "speed": 60},
        "moves": {
            1: ["Tackle", "Growl", "Vine Whip", "Leech Seed"],
            15: ["Razor Leaf"],
            22: ["Sweet Scent"],
            32: ["Solar Beam"],
        },
    },
    "Venusaur": {
        "level": 32,
        "type": ["Grass", "Poison"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 80, "attack": 82, "defense": 83, "speed": 80},
        "moves": {
            1: ["Tackle", "Growl", "Vine Whip", "Leech Seed", "Razor Leaf", "Sweet Scent"],
            46: ["Solar Beam"],
            54: ["Petal Blizzard"],
        },
    },

    # ----- Charmander Evolution Line -----
    "Charmander": {
        "level": 5,
        "type": ["Fire"],
        "evolve_level": 16,
        "evolves_to": "Charmeleon",
        "base_stats": {"hp": 39, "attack": 52, "defense": 43, "speed": 65},
        "moves": {
            1: ["Scratch", "Growl"],
            5: ["Ember"],
            7: ["Smokescreen"],
            10: ["Dragon Rage"],
        },
    },
    "Charmeleon": {
        "level": 16,
        "type": ["Fire"],
        "evolve_level": 36,
        "evolves_to": "Charizard",
        "base_stats": {"hp": 58, "attack": 64, "defense": 58, "speed": 80},
        "moves": {
            1: ["Scratch", "Growl", "Ember", "Smokescreen"],
            17: ["Flame Burst"],
            24: ["Slash"],
            36: ["Flamethrower"],
        },
    },
    "Charizard": {
        "level": 36,
        "type": ["Fire", "Flying"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 78, "attack": 84, "defense": 78, "speed": 100},
        "moves": {
            1: ["Scratch", "Growl", "Ember", "Smokescreen", "Flame Burst", "Slash"],
            46: ["Flamethrower"],
            54: ["Fire Spin"],
        },
    },

    # ----- Squirtle Evolution Line -----
    "Squirtle": {
        "level": 5,
        "type": ["Water"],
        "evolve_level": 16,
        "evolves_to": "Wartortle",
        "base_stats": {"hp": 44, "attack": 48, "defense": 65, "speed": 43},
        "moves": {
            1: ["Tackle", "Tail Whip"],
            5: ["Water Gun"],
            7: ["Withdraw"],
            10: ["Bubble"],
        },
    },
    "Wartortle": {
        "level": 16,
        "type": ["Water"],
        "evolve_level": 36,
        "evolves_to": "Blastoise",
        "base_stats": {"hp": 59, "attack": 63, "defense": 80, "speed": 58},
        "moves": {
            1: ["Tackle", "Tail Whip", "Water Gun", "Withdraw"],
            17: ["Bite"],
            24: ["Rapid Spin"],
            36: ["Hydro Pump"],
        },
    },
    "Blastoise": {
        "level": 36,
        "type": ["Water"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 79, "attack": 83, "defense": 100, "speed": 78},
        "moves": {
            1: ["Tackle", "Tail Whip", "Water Gun", "Withdraw", "Bite", "Rapid Spin"],
            46: ["Hydro Pump"],
            54: ["Skull Bash"],
        },
    },
    
    # ----- Caterpie Line -----
    "Caterpie": {
        "level": 3,
        "type": ["Bug"],
        "evolve_level": 7,
        "evolves_to": "Metapod",
        "base_stats": {"hp": 45, "attack": 30, "defense": 35, "speed": 45},
        "moves": {1: ["Tackle", "String Shot"]},
    },
    "Metapod": {
        "level": 7,
        "type": ["Bug"],
        "evolve_level": 10,
        "evolves_to": "Butterfree",
        "base_stats": {"hp": 50, "attack": 20, "defense": 55, "speed": 30},
        "moves": {1: ["Harden"]},
    },
    "Butterfree": {
        "level": 10,
        "type": ["Bug", "Flying"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 60, "attack": 45, "defense": 50, "speed": 70},
        "moves": {
            1: ["Confusion"],
            15: ["Gust"],
            20: ["Psybeam"],
        },
    },

    # ----- Weedle Line -----
    "Weedle": {
        "level": 3,
        "type": ["Bug", "Poison"],
        "evolve_level": 7,
        "evolves_to": "Kakuna",
        "base_stats": {"hp": 40, "attack": 35, "defense": 30, "speed": 50},
        "moves": {1: ["Poison Sting", "String Shot"]},
    },
    "Kakuna": {
        "level": 7,
        "type": ["Bug", "Poison"],
        "evolve_level": 10,
        "evolves_to": "Beedrill",
        "base_stats": {"hp": 45, "attack": 25, "defense": 50, "speed": 35},
        "moves": {1: ["Harden"]},
    },
    "Beedrill": {
        "level": 10,
        "type": ["Bug", "Poison"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 65, "attack": 90, "defense": 40, "speed": 75},
        "moves": {
            1: ["Fury Attack"],
            15: ["Twineedle"],
            25: ["Rage"],
        },
    },

    # ----- Pidgey Line -----
    "Pidgey": {
        "level": 5,
        "type": ["Normal", "Flying"],
        "evolve_level": 18,
        "evolves_to": "Pidgeotto",
        "base_stats": {"hp": 40, "attack": 45, "defense": 40, "speed": 56},
        "moves": {1: ["Tackle", "Sand Attack"], 9: ["Gust"]},
    },
    "Pidgeotto": {
        "level": 18,
        "type": ["Normal", "Flying"],
        "evolve_level": 36,
        "evolves_to": "Pidgeot",
        "base_stats": {"hp": 63, "attack": 60, "defense": 55, "speed": 71},
        "moves": {1: ["Gust", "Quick Attack"], 20: ["Wing Attack"]},
    },
    "Pidgeot": {
        "level": 36,
        "type": ["Normal", "Flying"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 83, "attack": 80, "defense": 75, "speed": 101},
        "moves": {1: ["Wing Attack", "Quick Attack"], 40: ["Hurricane"]},
    },

    # ----- Rattata Line -----
    "Rattata": {
        "level": 4,
        "type": ["Normal"],
        "evolve_level": 20,
        "evolves_to": "Raticate",
        "base_stats": {"hp": 30, "attack": 56, "defense": 35, "speed": 72},
        "moves": {1: ["Tackle", "Tail Whip"], 10: ["Quick Attack"]},
    },
    "Raticate": {
        "level": 20,
        "type": ["Normal"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 55, "attack": 81, "defense": 60, "speed": 97},
        "moves": {1: ["Quick Attack", "Hyper Fang"], 30: ["Super Fang"]},
    },

    # ----- Spearow Line -----
    "Spearow": {
        "level": 5,
        "type": ["Normal", "Flying"],
        "evolve_level": 20,
        "evolves_to": "Fearow",
        "base_stats": {"hp": 40, "attack": 60, "defense": 30, "speed": 70},
        "moves": {1: ["Peck", "Growl"], 9: ["Leer"]},
    },
    "Fearow": {
        "level": 20,
        "type": ["Normal", "Flying"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 65, "attack": 90, "defense": 65, "speed": 100},
        "moves": {1: ["Peck", "Fury Attack"], 25: ["Drill Peck"]},
    },

    # ----- Ekans Line -----
    "Ekans": {
        "level": 6,
        "type": ["Poison"],
        "evolve_level": 22,
        "evolves_to": "Arbok",
        "base_stats": {"hp": 35, "attack": 60, "defense": 44, "speed": 55},
        "moves": {1: ["Wrap", "Leer"], 10: ["Poison Sting"]},
    },
    "Arbok": {
        "level": 22,
        "type": ["Poison"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 60, "attack": 95, "defense": 69, "speed": 80},
        "moves": {1: ["Poison Sting", "Bite"], 30: ["Acid"]},
    },

    # ----- Pikachu Line -----
    "Pikachu": {
        "level": 5,
        "type": ["Electric"],
        "evolve_level": 30,
        "evolves_to": "Raichu",
        "base_stats": {"hp": 35, "attack": 55, "defense": 30, "speed": 90},
        "moves": {1: ["Thunder Shock", "Growl"], 10: ["Quick Attack"], 18: ["Thunderbolt"]},
    },
    "Raichu": {
        "level": 30,
        "type": ["Electric"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 60, "attack": 90, "defense": 55, "speed": 110},
        "moves": {1: ["Thunder Shock", "Quick Attack"], 30: ["Thunderbolt"], 40: ["Thunder"]},
    },

    # ----- Sandshrew Line -----
    "Sandshrew": {
        "level": 8,
        "type": ["Ground"],
        "evolve_level": 22,
        "evolves_to": "Sandslash",
        "base_stats": {"hp": 50, "attack": 75, "defense": 85, "speed": 40},
        "moves": {1: ["Scratch", "Defense Curl"], 10: ["Sand Attack"]},
    },
    "Sandslash": {
        "level": 22,
        "type": ["Ground"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 75, "attack": 100, "defense": 110, "speed": 65},
        "moves": {1: ["Scratch", "Sand Attack"], 25: ["Slash"]},
    },

    # ----- Nidoran♀ Line -----
    "Nidoran_f": {
        "level": 5,
        "type": ["Poison"],
        "evolve_level": 16,
        "evolves_to": "Nidorina",
        "base_stats": {"hp": 55, "attack": 47, "defense": 52, "speed": 41},
        "moves": {1: ["Growl", "Scratch"], 10: ["Poison Sting"]},
    },
    "Nidorina": {
        "level": 16,
        "type": ["Poison"],
        "evolve_level": 25,
        "evolves_to": "Nidoqueen",
        "base_stats": {"hp": 70, "attack": 62, "defense": 67, "speed": 56},
        "moves": {1: ["Scratch", "Poison Sting"], 20: ["Bite"]},
    },
    "Nidoqueen": {
        "level": 25,
        "type": ["Poison", "Ground"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 90, "attack": 82, "defense": 87, "speed": 76},
        "moves": {1: ["Scratch", "Bite"], 35: ["Body Slam"]},
    },
        # ----- Nidoran♂ Line -----
    "Nidoran_m": {
        "level": 5,
        "type": ["Poison"],
        "evolve_level": 16,
        "evolves_to": "Nidorino",
        "base_stats": {"hp": 46, "attack": 57, "defense": 40, "speed": 50},
        "moves": {1: ["Leer", "Peck"], 10: ["Poison Sting"]},
    },
    "Nidorino": {
        "level": 16,
        "type": ["Poison"],
        "evolve_level": 25,
        "evolves_to": "Nidoking",
        "base_stats": {"hp": 61, "attack": 72, "defense": 57, "speed": 65},
        "moves": {1: ["Peck", "Poison Sting"], 20: ["Horn Attack"]},
    },
    "Nidoking": {
        "level": 25,
        "type": ["Poison", "Ground"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 81, "attack": 102, "defense": 77, "speed": 85},
        "moves": {1: ["Horn Attack", "Poison Sting"], 35: ["Thrash"]},
    },

    # ----- Clefairy Line -----
    "Clefairy": {
        "level": 10,
        "type": ["Fairy"],
        "evolve_level": 25,
        "evolves_to": "Clefable",
        "base_stats": {"hp": 70, "attack": 45, "defense": 48, "speed": 35},
        "moves": {1: ["Pound", "Growl"], 15: ["Sing"]},
    },
    "Clefable": {
        "level": 25,
        "type": ["Fairy"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 95, "attack": 70, "defense": 73, "speed": 60},
        "moves": {1: ["Pound", "Sing"], 30: ["Metronome"]},
    },

    # ----- Vulpix Line -----
    "Vulpix": {
        "level": 10,
        "type": ["Fire"],
        "evolve_level": 25,
        "evolves_to": "Ninetales",
        "base_stats": {"hp": 38, "attack": 41, "defense": 40, "speed": 65},
        "moves": {1: ["Ember", "Tail Whip"], 15: ["Quick Attack"]},
    },
    "Ninetales": {
        "level": 25,
        "type": ["Fire"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 73, "attack": 76, "defense": 75, "speed": 100},
        "moves": {1: ["Ember", "Quick Attack"], 35: ["Flamethrower"]},
    },

    # ----- Jigglypuff Line -----
    "Jigglypuff": {
        "level": 10,
        "type": ["Normal", "Fairy"],
        "evolve_level": 25,
        "evolves_to": "Wigglytuff",
        "base_stats": {"hp": 115, "attack": 45, "defense": 20, "speed": 20},
        "moves": {1: ["Sing", "Pound"], 15: ["Defense Curl"]},
    },
    "Wigglytuff": {
        "level": 25,
        "type": ["Normal", "Fairy"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 140, "attack": 70, "defense": 45, "speed": 45},
        "moves": {1: ["Sing", "Pound"], 30: ["Double-Edge"]},
    },

    # ----- Zubat Line -----
    "Zubat": {
        "level": 6,
        "type": ["Poison", "Flying"],
        "evolve_level": 22,
        "evolves_to": "Golbat",
        "base_stats": {"hp": 40, "attack": 45, "defense": 35, "speed": 55},
        "moves": {1: ["Leech Life"], 10: ["Bite"]},
    },
    "Golbat": {
        "level": 22,
        "type": ["Poison", "Flying"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 75, "attack": 80, "defense": 70, "speed": 90},
        "moves": {1: ["Leech Life", "Bite"], 30: ["Wing Attack"]},
    },

    # ----- Oddish Line -----
    "Oddish": {
        "level": 5,
        "type": ["Grass", "Poison"],
        "evolve_level": 21,
        "evolves_to": "Gloom",
        "base_stats": {"hp": 45, "attack": 50, "defense": 55, "speed": 30},
        "moves": {1: ["Absorb"], 7: ["Poison Powder"]},
    },
    "Gloom": {
        "level": 21,
        "type": ["Grass", "Poison"],
        "evolve_level": 35,
        "evolves_to": "Vileplume",
        "base_stats": {"hp": 60, "attack": 65, "defense": 70, "speed": 40},
        "moves": {1: ["Absorb", "Poison Powder"], 25: ["Acid"]},
    },
    "Vileplume": {
        "level": 35,
        "type": ["Grass", "Poison"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 75, "attack": 80, "defense": 85, "speed": 50},
        "moves": {1: ["Acid", "Poison Powder"], 40: ["Petal Dance"]},
    },

    # ----- Paras Line -----
    "Paras": {
        "level": 10,
        "type": ["Bug", "Grass"],
        "evolve_level": 24,
        "evolves_to": "Parasect",
        "base_stats": {"hp": 35, "attack": 70, "defense": 55, "speed": 25},
        "moves": {1: ["Scratch", "Stun Spore"], 15: ["Leech Life"]},
    },
    "Parasect": {
        "level": 24,
        "type": ["Bug", "Grass"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 60, "attack": 95, "defense": 80, "speed": 30},
        "moves": {1: ["Stun Spore", "Leech Life"], 30: ["Spore"]},
    },

    # ----- Venonat Line -----
    "Venonat": {
        "level": 10,
        "type": ["Bug", "Poison"],
        "evolve_level": 31,
        "evolves_to": "Venomoth",
        "base_stats": {"hp": 60, "attack": 55, "defense": 50, "speed": 45},
        "moves": {1: ["Tackle", "Disable"], 20: ["Psybeam"]},
    },
    "Venomoth": {
        "level": 31,
        "type": ["Bug", "Poison"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 70, "attack": 65, "defense": 60, "speed": 90},
        "moves": {1: ["Psybeam", "Stun Spore"], 35: ["Sleep Powder"]},
    },

    # ----- Diglett Line -----
    "Diglett": {
        "level": 8,
        "type": ["Ground"],
        "evolve_level": 26,
        "evolves_to": "Dugtrio",
        "base_stats": {"hp": 10, "attack": 55, "defense": 25, "speed": 95},
        "moves": {1: ["Scratch", "Growl"], 15: ["Dig"]},
    },
    "Dugtrio": {
        "level": 26,
        "type": ["Ground"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 35, "attack": 100, "defense": 50, "speed": 120},
        "moves": {1: ["Scratch", "Dig"], 30: ["Earthquake"]},
    },

    # ----- Meowth Line -----
    "Meowth": {
        "level": 10,
        "type": ["Normal"],
        "evolve_level": 28,
        "evolves_to": "Persian",
        "base_stats": {"hp": 40, "attack": 45, "defense": 35, "speed": 90},
        "moves": {1: ["Scratch", "Growl"], 15: ["Bite"]},
    },
    "Persian": {
        "level": 28,
        "type": ["Normal"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 65, "attack": 70, "defense": 60, "speed": 115},
        "moves": {1: ["Scratch", "Bite"], 35: ["Slash"]},
    },

    # ----- Psyduck Line -----
    "Psyduck": {
        "level": 10,
        "type": ["Water"],
        "evolve_level": 33,
        "evolves_to": "Golduck",
        "base_stats": {"hp": 50, "attack": 52, "defense": 48, "speed": 55},
        "moves": {1: ["Scratch", "Water Gun"], 20: ["Confusion"]},
    },
    "Golduck": {
        "level": 33,
        "type": ["Water"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 80, "attack": 82, "defense": 78, "speed": 85},
        "moves": {1: ["Scratch", "Water Gun"], 40: ["Hydro Pump"]},
    },

    # ----- Mankey Line -----
    "Mankey": {
        "level": 10,
        "type": ["Fighting"],
        "evolve_level": 28,
        "evolves_to": "Primeape",
        "base_stats": {"hp": 40, "attack": 80, "defense": 35, "speed": 70},
        "moves": {1: ["Scratch", "Leer"], 15: ["Karate Chop"]},
    },
    "Primeape": {
        "level": 28,
        "type": ["Fighting"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 65, "attack": 105, "defense": 60, "speed": 95},
        "moves": {1: ["Karate Chop", "Fury Swipes"], 35: ["Seismic Toss"]},
    },

    # ----- Growlithe Line -----
    "Growlithe": {
        "level": 10,
        "type": ["Fire"],
        "evolve_level": 30,
        "evolves_to": "Arcanine",
        "base_stats": {"hp": 55, "attack": 70, "defense": 45, "speed": 60},
        "moves": {1: ["Bite", "Roar"], 15: ["Ember"]},
    },
    "Arcanine": {
        "level": 30,
        "type": ["Fire"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 90, "attack": 110, "defense": 80, "speed": 95},
        "moves": {1: ["Ember", "Bite"], 40: ["Flamethrower"]},
    },

    # ----- Poliwag Line -----
    "Poliwag": {
        "level": 5,
        "type": ["Water"],
        "evolve_level": 25,
        "evolves_to": "Poliwhirl",
        "base_stats": {"hp": 40, "attack": 50, "defense": 40, "speed": 90},
        "moves": {1: ["Bubble"], 15: ["Hypnosis"]},
    },
    "Poliwhirl": {
        "level": 25,
        "type": ["Water"],
        "evolve_level": 35,
        "evolves_to": "Poliwrath",
        "base_stats": {"hp": 65, "attack": 65, "defense": 65, "speed": 90},
        "moves": {1: ["Bubble", "Hypnosis"], 30: ["Body Slam"]},
    },
    "Poliwrath": {
        "level": 35,
        "type": ["Water", "Fighting"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 90, "attack": 95, "defense": 95, "speed": 70},
        "moves": {1: ["Body Slam", "Hypnosis"], 40: ["Hydro Pump"]},
    },
    # ----- Abra Line -----
    "Abra": {
        "level": 5,
        "type": ["Psychic"],
        "evolve_level": 16,
        "evolves_to": "Kadabra",
        "base_stats": {"hp": 25, "attack": 20, "defense": 15, "speed": 90},
        "moves": {1: ["Teleport"]},
    },
    "Kadabra": {
        "level": 16,
        "type": ["Psychic"],
        "evolve_level": 36,
        "evolves_to": "Alakazam",
        "base_stats": {"hp": 40, "attack": 35, "defense": 30, "speed": 105},
        "moves": {1: ["Teleport", "Confusion"], 20: ["Psybeam"]},
    },
    "Alakazam": {
        "level": 36,
        "type": ["Psychic"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 55, "attack": 50, "defense": 45, "speed": 120},
        "moves": {1: ["Confusion", "Psybeam"], 40: ["Psychic"]},
    },

    # ----- Machop Line -----
    "Machop": {
        "level": 10,
        "type": ["Fighting"],
        "evolve_level": 28,
        "evolves_to": "Machoke",
        "base_stats": {"hp": 70, "attack": 80, "defense": 50, "speed": 35},
        "moves": {1: ["Low Kick", "Leer"], 15: ["Karate Chop"]},
    },
    "Machoke": {
        "level": 28,
        "type": ["Fighting"],
        "evolve_level": 40,
        "evolves_to": "Machamp",
        "base_stats": {"hp": 80, "attack": 100, "defense": 70, "speed": 45},
        "moves": {1: ["Low Kick", "Karate Chop"], 30: ["Seismic Toss"]},
    },
    "Machamp": {
        "level": 40,
        "type": ["Fighting"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 90, "attack": 130, "defense": 80, "speed": 55},
        "moves": {1: ["Karate Chop", "Seismic Toss"], 40: ["Submission"]},
    },

    # ----- Geodude Line -----
    "Geodude": {
        "level": 8,
        "type": ["Rock", "Ground"],
        "evolve_level": 25,
        "evolves_to": "Graveler",
        "base_stats": {"hp": 40, "attack": 80, "defense": 100, "speed": 20},
        "moves": {1: ["Tackle", "Defense Curl"], 15: ["Rock Throw"]},
    },
    "Graveler": {
        "level": 25,
        "type": ["Rock", "Ground"],
        "evolve_level": 40,
        "evolves_to": "Golem",
        "base_stats": {"hp": 55, "attack": 95, "defense": 115, "speed": 35},
        "moves": {1: ["Tackle", "Rock Throw"], 30: ["Self-Destruct"]},
    },
    "Golem": {
        "level": 40,
        "type": ["Rock", "Ground"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 80, "attack": 120, "defense": 130, "speed": 45},
        "moves": {1: ["Rock Throw", "Self-Destruct"], 45: ["Earthquake"]},
    },

    # ----- Gastly Line -----
    "Gastly": {
        "level": 5,
        "type": ["Ghost", "Poison"],
        "evolve_level": 25,
        "evolves_to": "Haunter",
        "base_stats": {"hp": 30, "attack": 35, "defense": 30, "speed": 80},
        "moves": {1: ["Lick", "Night Shade"], 15: ["Confuse Ray"]},
    },
    "Haunter": {
        "level": 25,
        "type": ["Ghost", "Poison"],
        "evolve_level": 40,
        "evolves_to": "Gengar",
        "base_stats": {"hp": 45, "attack": 50, "defense": 45, "speed": 95},
        "moves": {1: ["Lick", "Night Shade", "Confuse Ray"], 30: ["Hypnosis"]},
    },
    "Gengar": {
        "level": 40,
        "type": ["Ghost", "Poison"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 60, "attack": 65, "defense": 60, "speed": 110},
        "moves": {1: ["Night Shade", "Hypnosis"], 45: ["Dream Eater"]},
    },

    # ----- Onix -----
    "Onix": {
        "level": 10,
        "type": ["Rock", "Ground"],
        "evolve_level": None,
        "evolves_to": None, 
        "base_stats": {"hp": 35, "attack": 45, "defense": 160, "speed": 70},
        "moves": {1: ["Tackle", "Bind"], 15: ["Rock Throw"]},
    },

    # ----- Drowzee Line -----
    "Drowzee": {
        "level": 10,
        "type": ["Psychic"],
        "evolve_level": 26,
        "evolves_to": "Hypno",
        "base_stats": {"hp": 60, "attack": 48, "defense": 45, "speed": 42},
        "moves": {1: ["Pound", "Hypnosis"], 15: ["Confusion"]},
    },
    "Hypno": {
        "level": 26,
        "type": ["Psychic"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 85, "attack": 73, "defense": 70, "speed": 67},
        "moves": {1: ["Pound", "Hypnosis", "Confusion"], 35: ["Psychic"]},
    },

    # ----- Krabby Line -----
    "Krabby": {
        "level": 10,
        "type": ["Water"],
        "evolve_level": 28,
        "evolves_to": "Kingler",
        "base_stats": {"hp": 30, "attack": 105, "defense": 90, "speed": 50},
        "moves": {1: ["Bubble", "Vice Grip"], 15: ["Mud Shot"]},
    },
    "Kingler": {
        "level": 28,
        "type": ["Water"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 55, "attack": 130, "defense": 115, "speed": 75},
        "moves": {1: ["Bubble", "Vice Grip"], 35: ["Crabhammer"]},
    },

    # ----- Tentacool Line -----
    "Tentacool": {
        "level": 5,
        "type": ["Water", "Poison"],
        "evolve_level": 30,
        "evolves_to": "Tentacruel",
        "base_stats": {"hp": 40, "attack": 40, "defense": 35, "speed": 70},
        "moves": {1: ["Bubble", "Poison Sting"], 15: ["Supersonic"]},
    },
    "Tentacruel": {
        "level": 30,
        "type": ["Water", "Poison"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 80, "attack": 70, "defense": 65, "speed": 100},
        "moves": {1: ["Bubble", "Poison Sting", "Supersonic"], 35: ["Hydro Pump"]},
    },

    # ----- Seel Line -----
    "Seel": {
        "level": 10,
        "type": ["Water"],
        "evolve_level": 34,
        "evolves_to": "Dewgong",
        "base_stats": {"hp": 65, "attack": 45, "defense": 55, "speed": 45},
        "moves": {1: ["Headbutt", "Growl"], 20: ["Aurora Beam"]},
    },
    "Dewgong": {
        "level": 34,
        "type": ["Water", "Ice"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 90, "attack": 70, "defense": 80, "speed": 70},
        "moves": {1: ["Headbutt", "Aurora Beam"], 40: ["Ice Beam"]},
    },

    # ----- BOSS POKEMON -----
    "BossMon": {
        "level": 20,
        "type": ["Normal"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 60, "attack": 56, "defense": 35, "speed": 72},
        "moves": {
            1: ["Tackle", "Quick Attack"],
            10: ["Bite"],
            20: ["Hyper Fang"]
        },
    },
    "BossMon_Form1": {
        "level": 20,
        "type": ["Fairy"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 70, "attack": 45, "defense": 48, "speed": 35},
        "moves": {
            1: ["Pound", "Sing"],
            15: ["Double Slap"],
            20: ["Moonblast"]
        },
    },
    "BossMon_Form2": {
        "level": 40,
        "type": ["Normal"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 160, "attack": 110, "defense": 65, "speed": 30},
        "moves": {
            1: ["Headbutt", "Rest"],
            20: ["Body Slam"],
            30: ["Crunch"],
            40: ["Hyper Beam"]
        },
    },
    "BossMon_Form3": {
        "level": 50,
        "type": ["Water", "Ice"],
        "evolve_level": None,
        "evolves_to": None,
        "base_stats": {"hp": 130, "attack": 85, "defense": 80, "speed": 60},
        "moves": {
            1: ["Water Gun", "Sing"],
            20: ["Ice Beam"],
            30: ["Body Slam"],
            40: ["Surf"],
            50: ["Blizzard"]
        },
    },

}