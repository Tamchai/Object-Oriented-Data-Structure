# main.py
import pygame
import random
import time
import os
from game import build_pokemon_from_species, generate_rival_team, Game, Enemy
from pokemon import Pokemon, Move, Pokeball, Potion
from areas import get_area_for_stage, encounter
from data_structures import Queue, Menu2DLinkedList, AreaTree

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Roguelike")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 26)
small_font = pygame.font.SysFont("Arial", 20)
tiny_font = pygame.font.SysFont("Arial", 16)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def asset_path(*parts):
    return os.path.join(BASE_DIR, "assets", *parts)


# ----- Load Images -----
def load_image(path, size=None):
    try:
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        # Return placeholder surface if image not found
        surf = pygame.Surface(size if size else (100, 100))
        surf.fill((200, 200, 200))
        pygame.draw.rect(surf, (100, 100, 100), surf.get_rect(), 2)
        return surf

# Load backgrounds
backgrounds = {
    "Forest": load_image(asset_path("backgrounds", "forest.png"), (WIDTH, HEIGHT)),
    "Cave": load_image(asset_path("backgrounds", "cave.png"), (WIDTH, HEIGHT)),
    "Tower": load_image(asset_path("backgrounds", "tower.png"), (WIDTH, HEIGHT)),
    "Beach": load_image(asset_path("backgrounds", "beach.png"), (WIDTH, HEIGHT)),
    "Menu": load_image(asset_path("backgrounds", "menu-2.png"), (WIDTH, HEIGHT)),
}

# Load item images
item_images = {
    "Pokeball": load_image(asset_path("items", "Pokeball.png"), (40, 40)),
    "Potion": load_image(asset_path("items", "Potion.png"), (40, 40)),
    "Rare Candy": load_image(asset_path("items", "Rare-Candy.png"), (40, 40)),
    "Revive": load_image(asset_path("items", "Revive.png"), (40, 40)),
    "Heal": load_image(asset_path("items", "Heal.png"), (40, 40)),
}

# Load rival image
rival_image = load_image(asset_path("trainer", "rival.png"), (150, 150))

# Pokemon image cache
pokemon_image_cache = {}

def get_pokemon_image(name, size=(120, 120), front=True):
    cache_key = (name, size, front)
    if cache_key in pokemon_image_cache:
        return pokemon_image_cache[cache_key]

    # --- Enemy sprite (front) ---
    if front:
        path = asset_path("pokemon", f"{name.lower()}_front.png")
        if os.path.exists(path):
            img = load_image(path, size)
        else:
            img = load_image(asset_path("pokemon", "placeholder_front.png"), size)

    # --- Player sprite (back) ---
    else:
        back_path = asset_path("pokemon", f"{name.lower()}_back.png")
        front_path = asset_path("pokemon", f"{name.lower()}_front.png")
        if os.path.exists(back_path):
            img = load_image(back_path, size)
        elif os.path.exists(front_path):
            img = load_image(front_path, size)
            img = pygame.transform.flip(img, True, False)  # flip front → back
        else:
            img = load_image(asset_path("pokemon", "placeholder_back.png"), size)

    pokemon_image_cache[cache_key] = img
    return img

        
class PokemonGame:
    def __init__(self):
        # ----- Core -----
        self.state = "MENU"
        self.game_core = Game()
        self.enemy = None
        self.catch_candidate = None
        self.message = ""
        self.starters = ["Bulbasaur", "Charmander", "Squirtle"]
        self.stage_number = 1
        self.catch_candidate = None
        self.catch_start_time = 0
        self.selected_index = 0
        self.menu_options = []
        self.saved_index = 0
        self.stage_wild_history = []
        self.current_area = "Forest"
        self.pending_move = None
        self.pending_pokemon = None
        self.pokemon_queue = Queue()
        self.battle_menu = Menu2DLinkedList()
        self.move_menu = Menu2DLinkedList()
        self.area_tree = AreaTree()

        # ----- Player initialization -----
        self.player = {
            "team": [],
            "items": {
                "Pokeball": [Pokeball() for _ in range(5)],
                "Potion": [Potion() for _ in range(3)]
            }
        }

        # ----- Reward Phase -----
        self.reward_options = ["Revive", "Pokéball +5", "Potion +1", "Heal", "Rare Candy"]
        self.reward_selected_index = 0
        self.reward_select_list = []
        self.reward_action = ""

        # ----- Boss & Rival -----
        self.boss_stages = [10,20,30,40,50]
        self.rival_stages = [5,15,25,35,45]

    # ---------- helper draw ----------
    def draw_text(self, text, x, y, color=(255,255,255), font_=None):
        f = font_ if font_ else font
        label = f.render(text, True, color)
        screen.blit(label, (x, y))

    def draw_health_bar(self, pkm, x, y, width=150, height=10):
        hp_ratio = max(pkm.hp / pkm.max_hp, 0)
        if hp_ratio > 0.5:
            color = (0, 255, 0)
        elif hp_ratio > 0.2:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height))
        pygame.draw.rect(screen, color, (x, y, int(width * hp_ratio), height))

    # ----------------------- MENU -----------------------
    def draw_menu(self):
        if backgrounds.get("Menu"):
            screen.blit(backgrounds["Menu"], (0, 0))
        else:
            screen.fill((30,30,60))
        
        # Title
        title_surf = font.render("Pokémon Roguelike", True, (255,255,0))
        title_rect = title_surf.get_rect(center=(WIDTH//2, 80))
        screen.blit(title_surf, title_rect)
        
        self.draw_text("Choose your starter:", WIDTH//2 - 100, 150)
        
        # Draw starter Pokemon with images
        for i, starter in enumerate(self.starters):
            y_pos = 220 + i * 120
            
            # Selection box
            if self.selected_index == i:
                pygame.draw.rect(screen, (255, 255, 0), (230, y_pos - 15, 440, 90), 3)
            
            # Pokemon image
            poke_img = get_pokemon_image(starter, (80, 80))
            screen.blit(poke_img, (250, y_pos - 10))
            
            # Name and info
            color = (255,255,0) if self.selected_index == i else (255,255,255)
            self.draw_text(starter, 360, y_pos + 10, color)
            self.draw_text("Lv 5", 360, y_pos + 40, (200,200,200), small_font)

    def start_game(self, starter):
        pkm = build_pokemon_from_species(starter, level=5)
        self.player["team"].append(pkm)
        self.stage_number = 1
        self.next_stage()

    # ----------------------- NEW MOVE -----------------------
    def draw_new_move(self):
        screen.fill((0, 0, 50))

        pkm = self.pending_pokemon
        new_move = self.pending_move

        if pkm is None or new_move is None:
            self.draw_text("Error: no pending move.", 70, 120, (255, 0, 0))
            self.draw_text("Press Z to continue", 70, 160)
            return

        # กล่องข้อความ
        panel = pygame.Surface((800, 400))
        panel.set_alpha(230)
        panel.fill((30, 30, 60))
        screen.blit(panel, (50, 100))
        pygame.draw.rect(screen, (255, 255, 255), (50, 100, 800, 400), 3)

        self.draw_text(f"{pkm.name} wants to learn {new_move.name}!", 70, 120, (255, 255, 0))

        # แสดงท่าเก่า + cancel
        options = [m.name for m in pkm.moves] + [f"Cancel (keep old moves)"]
        for i, opt in enumerate(options):
            color = (255, 255, 0) if self.selected_index == i else (255, 255, 255)
            self.draw_text(opt, 100, 180 + i * 50, color)


    # ----------------------- STAGE -----------------------
    def next_stage(self):
        self.stage_wild_history = []

        if self.stage_number > 50:
            self.state = "WIN"
            self.message = "Congratulations! You completed all 50 stages!"
            return

        # Boss Stage
        if self.stage_number in self.boss_stages:
            boss_level = min(50, self.stage_number + 10)
            self.enemy = build_pokemon_from_species("BossMon", level=boss_level)
            self.enemy.hp = int(self.enemy.max_hp * 1.8)
            self.enemy.max_hp = self.enemy.hp
            self.enemy.base_stats["attack"] = int(self.enemy.base_stats["attack"] * 1.3)
            self.state = "BATTLE"
            self.message = f"Stage {self.stage_number}: Boss {self.enemy.name} appeared!"
            self.selected_index = 0
            self.current_area = "Tower"
            return

        # Rival Stage
        if self.stage_number in self.rival_stages:
            rival_enemy = generate_rival_team(stage_level=self.stage_number)
            for p in rival_enemy.team:
                p.hp = int(p.max_hp * 1.2)
                p.max_hp = p.hp
                p.base_stats["attack"] = int(p.base_stats["attack"] * 1.1)
            self.enemy = rival_enemy
            self.state = "BATTLE"
            self.message = f"Stage {self.stage_number}: Rival appeared!"
            self.selected_index = 0
            self.current_area = "Tower"
            return

        # Normal Stage
        area = self.area_tree.get_area_for_stage(self.stage_number)
        self.current_area = area
        max_level = min(5 + self.stage_number // 2, 50)
        attempts = 0
        while True:
            wild_encounter = encounter(area, max_level=max_level)
            wild_species = build_pokemon_from_species(wild_encounter.name, wild_encounter.level)
            pair = (wild_species.name, wild_species.level)
            already_in_team = any(p.name == wild_species.name and p.level == wild_species.level for p in self.player["team"])
            if not already_in_team and pair not in self.stage_wild_history:
                break
            attempts += 1
            if attempts > 200:
                break
        
        self.stage_wild_history.append((wild_species.name, wild_species.level))
        self.enemy = wild_species
        self.state = "BATTLE"
        self.message = f"Stage {self.stage_number} - {area}: A wild {self.enemy.name} appeared!"
        self.selected_index = 0

    def draw_stage_info(self):
        area = get_area_for_stage(self.stage_number - 1) if self.stage_number > 1 else "Forest"
        if backgrounds.get(area):
            screen.blit(backgrounds[area], (0, 0))
        else:
            screen.fill((0,50,0))
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        self.draw_text(self.message, 150, 250, (0,255,0))
        self.draw_text("Press Z to continue", 300, 350)

    # ----------------------- BATTLE -----------------------
    def draw_battle(self):
        # Draw background
        if backgrounds.get(self.current_area):
            screen.blit(backgrounds[self.current_area], (0, 0))
        else:
            screen.fill((0, 0, 50))
        
        player_pokemon = self.player["team"][0] if self.player["team"] else None
        if not player_pokemon:
            self.message = "No Pokémon in team!"
            return

        # Get enemy Pokemon
        enemy_pkms = []
        is_rival = False
        if isinstance(self.enemy, Pokemon):
            enemy_pkms = [self.enemy]
        elif isinstance(self.enemy, Enemy):
            enemy_pkms = [p for p in self.enemy.team if p.hp > 0]
            is_rival = self.enemy.name == "Rival"
        elif isinstance(self.enemy, list):
            enemy_pkms = self.enemy

        # DRAW PLAYER POKEMON (bottom left)
        if player_pokemon:
            player_img = get_pokemon_image(player_pokemon.name, (160, 160), front=False)
            screen.blit(player_img, (100, HEIGHT - 200))
            
            panel = pygame.Surface((250, 80))
            panel.set_alpha(200)
            panel.fill((40, 40, 40))
            screen.blit(panel, (WIDTH - 300, HEIGHT - 160))  # ขวาล่าง
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 300, HEIGHT - 160, 250, 80), 2)
            
            self.draw_text(f"{player_pokemon.name}", WIDTH - 290, HEIGHT - 155, (255,255,255))
            self.draw_text(f"Lv{player_pokemon.level}", WIDTH - 90, HEIGHT - 155, (255,255,0), small_font)
            self.draw_health_bar(player_pokemon, WIDTH - 290, HEIGHT - 125, 230, 15)
            self.draw_text(f"{player_pokemon.hp}/{player_pokemon.max_hp}", WIDTH - 290, HEIGHT - 105, (255,255,255), small_font)

        # DRAW ENEMY POKEMON (top right)
        if is_rival and enemy_pkms:
            # Rival trainer sprite
            screen.blit(rival_image, (WIDTH - 250, 40)) 
            
            if enemy_pkms:
                pkm = enemy_pkms[0]
                enemy_img = get_pokemon_image(pkm.name, (180, 180), front=True)
                # Pokémon ของ Rival อยู่ขวากลางบน (เลื่อนลงมาหน่อย)
                screen.blit(enemy_img, (WIDTH - 320, HEIGHT // 3))  

                # HP panel (เลื่อนลงมาจาก 20 → 120)
                panel = pygame.Surface((250, 80))
                panel.set_alpha(200)
                panel.fill((40, 40, 40))
                screen.blit(panel, (WIDTH - 320, 120))
                pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 320, 120, 250, 80), 2)

                # ข้อความบนกล่อง HP
                self.draw_text(f"{pkm.name}", WIDTH - 310, 125, (255,255,255))
                self.draw_text(f"Lv{pkm.level}", WIDTH - 110, 125, (255,255,0), small_font)
                self.draw_health_bar(pkm, WIDTH - 310, 155, 230, 15)
                self.draw_text(f"{pkm.hp}/{pkm.max_hp}", WIDTH - 310, 175, (255,255,255), small_font)

                # Team count (ขยับตามลงมา)
                alive_count = len([p for p in self.enemy.team if p.hp > 0])
                self.draw_text(f"Team: {alive_count}/{len(self.enemy.team)}", WIDTH - 250, 200, (255,255,0), tiny_font)

        else:
            # Wild Pokémon (กลางขวา)
            if enemy_pkms:
                y = HEIGHT // 3   # ศัตรูอยู่ประมาณกลางจอ
                for i, pkm in enumerate(enemy_pkms[:3]):
                    enemy_img = get_pokemon_image(pkm.name, (140, 140), front=True)
                    screen.blit(enemy_img, (WIDTH - 320, y))

                    panel = pygame.Surface((220, 70))
                    panel.set_alpha(200)
                    panel.fill((40, 40, 40))
                    screen.blit(panel, (40, y - 20))
                    pygame.draw.rect(screen, (255, 255, 255), (40, y - 20, 220, 70), 2)

                    self.draw_text(f"{pkm.name}", 50, y - 15, (255,255,255), small_font)
                    self.draw_text(f"Lv{pkm.level}", 200, y - 15, (255,255,0), tiny_font)
                    self.draw_health_bar(pkm, 50, y + 10, 180, 12)
                    self.draw_text(f"{pkm.hp}/{pkm.max_hp}", 50, y + 28, (255,255,255), tiny_font)

                    if i < 2:
                        y += 120

        # MESSAGE BOX
        msg_panel = pygame.Surface((850, 70))
        msg_panel.set_alpha(220)
        msg_panel.fill((0, 0, 0))
        screen.blit(msg_panel, (25, 20))
        pygame.draw.rect(screen, (255, 255, 255), (25, 20, 850, 70), 3)
        
        # Word wrap for long messages
        words = self.message.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < 800:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        for i, line in enumerate(lines[:2]):
            self.draw_text(line.strip(), 40, 30 + i * 25, (255, 255, 0), small_font)

        # MENU OPTIONS
        self.battle_menu.create_battle_menu() 
        menu_panel = pygame.Surface((850, 60))
        menu_panel.set_alpha(220)
        menu_panel.fill((20, 20, 40))
        screen.blit(menu_panel, (25, 520))
        pygame.draw.rect(screen, (255, 255, 255), (25, 520, 850, 60), 3)
        
        options = ["Fight", "Bag", "Pokémon", "Run"]
        self.menu_options = options
        for i, opt in enumerate(options):
            color = (255, 255, 0) if self.selected_index == i else (255, 255, 255)
            self.draw_text(opt, 80 + i * 200, 535, color)


    def draw_skill_selection(self):
        if backgrounds.get(self.current_area):
            screen.blit(backgrounds[self.current_area], (0, 0))
        else:
            screen.fill((0,0,50))
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        player_pokemon = self.player["team"][0]

        enemy_pkm = None
        if isinstance(self.enemy, Pokemon):
            enemy_pkm = self.enemy
        elif isinstance(self.enemy, Enemy):
            enemy_pkm = self.enemy.choose_pokemon()

        # Player Pokemon
        player_img = get_pokemon_image(player_pokemon.name, (100, 100), front=False)
        screen.blit(player_img, (50, 400))
        
        panel = pygame.Surface((300, 60))
        panel.set_alpha(220)
        panel.fill((40, 40, 40))
        screen.blit(panel, (30, 480))
        pygame.draw.rect(screen, (255, 255, 255), (30, 480, 300, 60), 2)
        self.draw_text(f"{player_pokemon.name} Lv{player_pokemon.level}", 40, 485, (255,255,255), small_font)
        self.draw_text(f"HP: {player_pokemon.hp}/{player_pokemon.max_hp}", 40, 510, (255,255,255), small_font)

        # Enemy Pokemon
        if enemy_pkm:
            enemy_img = get_pokemon_image(enemy_pkm.name, (100, 100), front=True)
            screen.blit(enemy_img, (700, 50))
            
            panel = pygame.Surface((250, 60))
            panel.set_alpha(220)
            panel.fill((40, 40, 40))
            screen.blit(panel, (580, 120))
            pygame.draw.rect(screen, (255, 255, 255), (580, 120, 250, 60), 2)
            self.draw_text(f"{enemy_pkm.name} Lv{enemy_pkm.level}", 590, 125, (255,255,255), small_font)
            self.draw_text(f"HP: {enemy_pkm.hp}/{enemy_pkm.max_hp}", 590, 150, (255,255,255), small_font)

        # Message
        msg_panel = pygame.Surface((850, 50))
        msg_panel.set_alpha(220)
        msg_panel.fill((0, 0, 0))
        screen.blit(msg_panel, (25, 20))
        pygame.draw.rect(screen, (255, 255, 255), (25, 20, 850, 50), 3)
        self.draw_text(self.message, 40, 35, (255,255,0), small_font)
        
        # Move panel
        move_panel = pygame.Surface((500, 250))
        move_panel.set_alpha(220)
        move_panel.fill((20, 20, 60))
        screen.blit(move_panel, (200, 200))
        pygame.draw.rect(screen, (255, 255, 255), (200, 200, 500, 250), 3)
        
        moves = [move.name for move in player_pokemon.moves[:4]]
        self.menu_options = moves
        positions = [(220,220),(420,220),(220,320),(420,320)]
        
        for i, move_name in enumerate(moves):
            if i < len(positions):
                btn_color = (100, 100, 0) if i == self.selected_index else (60, 60, 60)
                pygame.draw.rect(screen, btn_color, (positions[i][0], positions[i][1], 160, 70))
                pygame.draw.rect(screen, (255, 255, 0) if i == self.selected_index else (200, 200, 200), 
                               (positions[i][0], positions[i][1], 160, 70), 2)
                
                color = (255,255,0) if i == self.selected_index else (255,255,255)
                self.draw_text(move_name, positions[i][0] + 10, positions[i][1] + 10, color, tiny_font)
                
                move = player_pokemon.moves[i]
                self.draw_text(f"Pow:{move.power}", positions[i][0] + 10, positions[i][1] + 35, (200,200,200), tiny_font)
                self.draw_text(f"{move.type}", positions[i][0] + 10, positions[i][1] + 52, (150,200,255), tiny_font)

    def use_skill(self):
        player_pokemon = self.player["team"][0]

        enemy_pkm = None
        if isinstance(self.enemy, Pokemon):
            enemy_pkm = self.enemy
        elif isinstance(self.enemy, Enemy):
            enemy_pkm = self.enemy.choose_pokemon()

        if not enemy_pkm:
            self.state = "BATTLE"
            self.message = "No enemy to fight!"
            return

        if self.selected_index >= len(player_pokemon.moves):
            self.state = "BATTLE"
            self.message = "Invalid move selected!"
            self.selected_index = 0
            return

        move = player_pokemon.moves[self.selected_index]
        damage = player_pokemon.attack(move, enemy_pkm)
        self.message = f"{player_pokemon.name} used {move.name}! Dealt {damage} damage!"

        if enemy_pkm.is_fainted():
            self.message = f"You defeated {enemy_pkm.name}!"
            player_pokemon.gain_exp(50 + enemy_pkm.level * 2)
            self.handle_new_moves(player_pokemon)
            
            if isinstance(self.enemy, Enemy):
                self.enemy.team = [p for p in self.enemy.team if not p.is_fainted()]
                if not self.enemy.team:
                    self.reward_phase()
                    return
            else:
                self.reward_phase()
                return

        if isinstance(self.enemy, Pokemon) and not self.enemy.is_fainted():
            if self.enemy.moves:
                enemy_move = random.choice(self.enemy.moves)
                enemy_damage = self.enemy.attack(enemy_move, player_pokemon)
                self.message += f" {self.enemy.name} used {enemy_move.name}! Dealt {enemy_damage} damage!"
        elif isinstance(self.enemy, Enemy) and self.enemy.team:
            enemy_pkm2 = self.enemy.choose_pokemon()
            if enemy_pkm2 and enemy_pkm2.moves:
                enemy_move = random.choice(enemy_pkm2.moves)
                enemy_damage = enemy_pkm2.attack(enemy_move, player_pokemon)
                self.message += f" {enemy_pkm2.name} used {enemy_move.name}! Dealt {enemy_damage} damage!"

        if player_pokemon.is_fainted():
            if any(p.hp > 0 for p in self.player["team"][1:]):
                self.state = "SWITCH_PKM"
                self.message = "Your Pokémon fainted! Choose another to continue."
                for i, p in enumerate(self.player["team"]):
                    if i != 0 and p.hp > 0:
                        self.selected_index = i
                        break
            else:
                self.state = "GAME_OVER"
                self.message = "All your Pokémon fainted! Game Over."
        else:
            self.state = "BATTLE"
            self.selected_index = 0

    def set_skill_state(self):
        if not self.player["team"] or self.player["team"][0].hp <= 0:
            if any(p.hp > 0 for p in self.player["team"][1:]):
                self.state = "SWITCH_PKM"
                self.message = "Your Pokémon fainted! Choose another to continue."
                for i, p in enumerate(self.player["team"]):
                    if p.hp > 0:
                        self.selected_index = i
                        break
            else:
                self.state = "GAME_OVER"
                self.message = "All your Pokémon fainted! Game Over."
            return
        self.state = "BATTLE_SKILL_SELECT"
        self.message = "Choose a move:"

        player_pokemon = self.player["team"][0]
        self.move_menu.create_move_menu(player_pokemon.moves)
        
        self.selected_index = 0

    def handle_new_moves(self, pokemon):
        # ถ้าไม่มี attribute pending_new_moves ให้คืน (ปลอดภัย)
        if not hasattr(pokemon, "pending_new_moves"):
            return

        # ทำทีละท่าในคิว
        while pokemon.pending_new_moves:
            new_move = pokemon.pending_new_moves.pop(0)
            if len(pokemon.moves) < 4:
                pokemon.moves.append(new_move)
                self.message = f"{pokemon.name} learned {new_move.name}!"
                # อาจอยากมี delay / animation — ปรับได้
            else:
                # เตรียมเข้าสู่ NEW_MOVE UI (ให้ผู้เล่นเลือกท่าที่จะลืม)
                self.pending_move = new_move
                self.pending_pokemon = pokemon
                self.state = "NEW_MOVE"
                self.selected_index = 0
                self.message = f"{pokemon.name} wants to learn {new_move.name}!"
                # หยุด loop — รอให้ผู้เล่นเลือกผ่าน UI
                return


    # ----------------------- CATCH ANIMATION -----------------------
    def draw_catch_animation(self):
        if backgrounds.get(self.current_area):
            screen.blit(backgrounds[self.current_area], (0, 0))
        else:
            screen.fill((0,0,0))
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Show Pokemon
        if self.catch_candidate:
            poke_img = get_pokemon_image(self.catch_candidate.name, (150, 150), front=True)
            screen.blit(poke_img, (375, 200))
        
        # Show Pokeball
        screen.blit(item_images["Pokeball"], (430, 350))
        
        self.draw_text("Throwing Pokéball...", 320, 420, (255,255,0))
        
        elapsed = time.time() - self.catch_start_time
        if elapsed > 1.2:
            caught = False
            try:
                caught = self.catch_candidate.catch_rate()
            except Exception:
                caught = random.random() < 0.5
            if caught:
                if len(self.player["team"]) < 6:
                    self.player["team"].append(self.catch_candidate)
                    self.message = f"You caught {self.catch_candidate.name}!"
                else:
                    self.message = f"You caught {self.catch_candidate.name} but your team is full!"
                try:
                    self.stage_wild_history.append((self.catch_candidate.name, self.catch_candidate.level))
                except Exception:
                    pass
                self.catch_candidate = None
                self.reward_phase()
            else:
                self.message = f"{self.catch_candidate.name} broke free!"
                self.catch_candidate = None
                self.state = "BATTLE"
                self.selected_index = 0

    # ----------------------- REWARD PHASE -----------------------
    def reward_phase(self):
        self.state = "REWARD"
        self.reward_selected_index = 0
        self.message = "Choose a reward:"

    def draw_reward_phase(self):
        if backgrounds.get(self.current_area):
            screen.blit(backgrounds[self.current_area], (0, 0))
        else:
            screen.fill((50,50,100))
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        panel = pygame.Surface((600, 450))
        panel.set_alpha(230)
        panel.fill((40, 40, 80))
        screen.blit(panel, (150, 75))
        pygame.draw.rect(screen, (255, 255, 255), (150, 75, 600, 450), 4)
        
        self.draw_text(self.message, 300, 100, (255,255,0))
        
        for i, opt in enumerate(self.reward_options):
            y_pos = 170 + i * 60
            box_color = (80, 80, 0) if i == self.reward_selected_index else (60, 60, 80)
            pygame.draw.rect(screen, box_color, (200, y_pos - 10, 500, 50))
            border_color = (255, 255, 0) if i == self.reward_selected_index else (200, 200, 200)
            pygame.draw.rect(screen, border_color, (200, y_pos - 10, 500, 50), 3)
            
            # Draw item icon
            if opt == "Pokéball +5" and "Pokeball" in item_images:
                screen.blit(pygame.transform.scale(item_images["Pokeball"], (35, 35)), (215, y_pos - 5))
            elif opt == "Potion +1" and "Potion" in item_images:
                screen.blit(pygame.transform.scale(item_images["Potion"], (35, 35)), (215, y_pos - 5))
            elif opt == "Rare Candy" and "Rare Candy" in item_images:
                screen.blit(pygame.transform.scale(item_images["Rare Candy"], (35, 35)), (215, y_pos - 5))
            elif opt == "Revive" and "Revive" in item_images:
                screen.blit(pygame.transform.scale(item_images["Revive"], (35, 35)), (215, y_pos - 5))
            elif opt == "Heal" and "Heal" in item_images:
                screen.blit(pygame.transform.scale(item_images["Heal"], (35, 35)), (215, y_pos - 5))
            
            color = (255,255,0) if i == self.reward_selected_index else (255,255,255)
            self.draw_text(opt, 270, y_pos, color)

    def use_reward(self):
        choice = self.reward_options[self.reward_selected_index]
        if choice == "Revive":
            dead_pkm = [p for p in self.player["team"] if p.hp == 0]
            if dead_pkm:
                self.reward_select_list = dead_pkm
                self.reward_action = "Revive"
                self.state = "REWARD_SELECT"
                self.reward_selected_index = 0
            else:
                self.message = "No Pokémon to revive."
                self.stage_number += 1
                self.next_stage()
        elif choice == "Pokéball +5":
            for _ in range(5):
                self.player["items"]["Pokeball"].append(Pokeball())
            self.message = "Got 5 Pokéballs!"
            self.stage_number += 1
            self.next_stage()
        elif choice == "Potion +1":
            self.player["items"]["Potion"].append(Potion())
            self.message = "Got 1 Potion!"
            self.stage_number += 1
            self.next_stage()
        elif choice == "Heal":
            self.reward_select_list = [p for p in self.player["team"] if p.hp < p.max_hp]
            if self.reward_select_list:
                self.reward_action = "Heal"
                self.state = "REWARD_SELECT"
                self.reward_selected_index = 0
            else:
                self.message = "All Pokémon are at full health!"
                self.stage_number += 1
                self.next_stage()
        elif choice == "Rare Candy":
            self.reward_select_list = self.player["team"]
            self.reward_action = "Rare Candy"
            self.state = "REWARD_SELECT"
            self.reward_selected_index = 0

    def draw_reward_select(self):
        screen.fill((100,50,50))
        self.draw_text(f"Select Pokémon to {self.reward_action}:", 200, 50, (255,255,0))
        for i, pkm in enumerate(self.reward_select_list):
            color = (255,255,0) if i == self.reward_selected_index else (255,255,255)
            self.draw_text(f"{pkm.name} Lv{pkm.level} HP:{pkm.hp}/{pkm.max_hp}", 300, 150+i*50, color)

    def apply_reward(self):
        selected_pkm = self.reward_select_list[self.reward_selected_index]
        if self.reward_action == "Revive":
            selected_pkm.hp = selected_pkm.max_hp
            self.message = f"{selected_pkm.name} was revived!"
        elif self.reward_action == "Heal":
            heal_amount = ((self.stage_number-1)//10+1)*10
            selected_pkm.hp = min(selected_pkm.hp + heal_amount, selected_pkm.max_hp)
            self.message = f"{selected_pkm.name} healed {heal_amount} HP!"
        elif self.reward_action == "Rare Candy":
            selected_pkm.level_up()
            self.message = f"{selected_pkm.name} grew to Lv{selected_pkm.level}!"
            self.handle_new_moves(selected_pkm)
        
        self.stage_number += 1
        self.next_stage()

    # ----------------------- BAG, SWITCH, RUN, GAME OVER, WIN -----------------------
    def open_bag(self):
        self.saved_index = self.selected_index
        self.state = "BAG"
        self.selected_index = 0
        self.menu_options = list(self.player["items"].keys())

    def draw_bag(self):
        screen.fill((50,50,0))
        self.draw_text("Bag:", 100, 50, (255,255,0))
        y = 120
        for i, item_name in enumerate(self.player["items"]):
            color = (255,255,0) if self.selected_index == i else (255,255,255)
            self.draw_text(f"{item_name}: {len(self.player['items'][item_name])}", 120, y, color)
            y += 60
        self.draw_text("Press X to go back", 350, 500, (255,255,255))

    def use_item(self):
        item_name = self.menu_options[self.selected_index]
        player_pokemon = self.player["team"][0] if self.player["team"] else None
        if item_name == "Potion" and player_pokemon:
            if self.player["items"]["Potion"]:
                potion = self.player["items"]["Potion"].pop()
                potion.use(player_pokemon)
                self.message = f"{player_pokemon.name} healed!"
                self.state = "BATTLE"
                self.selected_index = 0
            else:
                self.message = "No Potions left!"
                self.state = "BATTLE"
                self.selected_index = 0
        elif item_name == "Pokeball" and isinstance(self.enemy, Pokemon):
            if self.player["items"]["Pokeball"]:
                self.player["items"]["Pokeball"].pop()
                self.catch_candidate = self.enemy
                self.catch_start_time = time.time()
                self.state = "CATCH_ANIMATION"
            else:
                self.message = "No Pokéballs left!"
                self.state = "BATTLE"
                self.selected_index = 0
        else:
            self.message = "Cannot use this item now!"
            self.state = "BATTLE"
            self.selected_index = 0

    def back_to_battle(self):
        self.state = "BATTLE"
        self.selected_index = self.saved_index

    def switch_pokemon(self):
        available_pokemon = [p for p in self.player["team"][1:] if p.hp > 0]
        if not available_pokemon:
            self.message = "No other Pokémon available to switch!"
            return
        
        self.saved_index = self.selected_index
        self.state = "SWITCH_PKM"
        self.message = "Select a Pokémon to switch:"
        self.selected_index = 1
        for i, p in enumerate(self.player["team"]):
            if i != 0 and p.hp > 0:
                self.selected_index = i
                break
        self.menu_options = self.player["team"]

    def draw_switch_pokemon(self):
        screen.fill((0,50,50))
        self.draw_text(self.message, 200, 50, (255,255,0))
        y = 120
        for i, pkm in enumerate(self.player["team"]):
            if i == 0:
                continue
            color = (255,255,0) if self.selected_index == i else (255,255,255)
            status = "FAINTED" if pkm.hp <= 0 else f"HP:{pkm.hp}/{pkm.max_hp}"
            self.draw_text(f"{pkm.name} Lv{pkm.level} {status}", 300, y, color)
            y += 60
        self.draw_text("Press X to cancel", 350, 500, (255,255,255))

    def perform_switch(self):
        idx = self.selected_index
        if idx >= len(self.player["team"]) or self.player["team"][idx].hp <= 0:
            self.message = f"Cannot switch to that Pokémon!"
            return
        self.player["team"][0], self.player["team"][idx] = self.player["team"][idx], self.player["team"][0]
        self.message = f"{self.player['team'][0].name} is now in battle!"
        self.state = "BATTLE"
        self.selected_index = 0

    def run_away(self):
        # Can't run from boss or rival battles
        if self.stage_number in self.boss_stages or self.stage_number in self.rival_stages:
            self.message = "Cannot run from this battle!"
            return
        
        available = [i for i, p in enumerate(self.player["team"]) if p.hp > 0]
        if available:
            if available[0] != 0:
                self.player["team"][0], self.player["team"][available[0]] = self.player["team"][available[0]], self.player["team"][0]
        self.message = f"You ran away! {self.player['team'][0].name} is now in battle."
        self.stage_number += 1
        self.next_stage()

    def draw_game_over(self):
        screen.fill((50,0,0))
        self.draw_text("Game Over!", 300, 200, (255,0,0))
        self.draw_text(f"You reached Stage {self.stage_number}/50", 280, 250)
        self.draw_text("Press Z to Restart", 350, 300)

    def draw_win(self):
        screen.fill((0,100,0))
        self.draw_text("Congratulations!", 280, 200, (255,255,0))
        self.draw_text("You completed all 50 stages!", 250, 250, (0,255,0))
        self.draw_text("You are the Pokemon Champion!", 230, 300, (255,255,0))
        self.draw_text("Press Z to Play Again", 320, 350)

    def restart(self):
        self.__init__()

# ------------------- Main Loop -------------------
game = PokemonGame()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # ---------------- MENU ----------------
            if game.state == "MENU":
                if event.key == pygame.K_DOWN:
                    game.selected_index = (game.selected_index+1) % len(game.starters)
                elif event.key == pygame.K_UP:
                    game.selected_index = (game.selected_index-1) % len(game.starters)
                elif event.key == pygame.K_z:
                    game.start_game(game.starters[game.selected_index])
            # ---------------- STAGE ----------------
            elif game.state == "STAGE":
                if event.key == pygame.K_z:
                    game.next_stage()
            # ---------------- BATTLE ----------------
            elif game.state == "BATTLE":
                if event.key == pygame.K_RIGHT:
                    game.selected_index = min(game.selected_index+1, len(game.menu_options)-1)
                elif event.key == pygame.K_LEFT:
                    game.selected_index = max(game.selected_index-1, 0)
                elif event.key == pygame.K_z:
                    choice = game.menu_options[game.selected_index]
                    if choice == "Fight":
                        game.set_skill_state()
                    elif choice == "Bag":
                        game.open_bag()
                    elif choice == "Pokémon":
                        game.switch_pokemon()
                    elif choice == "Run":
                        game.run_away()
            # ---------------- BATTLE_SKILL_SELECT ----------------
            elif game.state == "BATTLE_SKILL_SELECT":
                if event.key == pygame.K_RIGHT:
                    if game.selected_index % 2 == 0 and game.selected_index+1 < len(game.menu_options):
                        game.selected_index += 1
                elif event.key == pygame.K_LEFT:
                    if game.selected_index % 2 == 1:
                        game.selected_index -= 1
                elif event.key == pygame.K_DOWN:
                    if game.selected_index + 2 < len(game.menu_options):
                        game.selected_index += 2
                elif event.key == pygame.K_UP:
                    if game.selected_index - 2 >= 0:
                        game.selected_index -= 2
                elif event.key == pygame.K_z:
                    game.use_skill()
                elif event.key == pygame.K_x:
                    game.state = "BATTLE"
                    game.selected_index = 0
            # ---------------- BAG ----------------
            elif game.state == "BAG":
                if event.key == pygame.K_DOWN:
                    game.selected_index = (game.selected_index+1) % len(game.menu_options)
                elif event.key == pygame.K_UP:
                    game.selected_index = (game.selected_index-1) % len(game.menu_options)
                elif event.key == pygame.K_z:
                    game.use_item()
                elif event.key == pygame.K_x:
                    game.back_to_battle()
            # ---------------- SWITCH ----------------
            elif game.state == "SWITCH_PKM":
                if event.key == pygame.K_DOWN:
                    if game.selected_index +1 < len(game.player["team"]):
                        game.selected_index += 1
                elif event.key == pygame.K_UP:
                    if game.selected_index > 1:
                        game.selected_index -= 1
                elif event.key == pygame.K_z:
                    game.perform_switch()
                elif event.key == pygame.K_x:
                    game.state = "BATTLE"
                    game.selected_index = game.saved_index
            # ---------------- CATCH ----------------
            elif game.state == "CATCH_ANIMATION":
                pass
            # ---------------- REWARD ----------------
            elif game.state == "REWARD":
                if event.key == pygame.K_DOWN:
                    game.reward_selected_index = min(game.reward_selected_index+1, len(game.reward_options)-1)
                elif event.key == pygame.K_UP:
                    game.reward_selected_index = max(game.reward_selected_index-1, 0)
                elif event.key == pygame.K_z:
                    game.use_reward()
            elif game.state == "REWARD_SELECT":
                if event.key == pygame.K_DOWN:
                    game.reward_selected_index = min(game.reward_selected_index+1, len(game.reward_select_list)-1)
                elif event.key == pygame.K_UP:
                    game.reward_selected_index = max(game.reward_selected_index-1, 0)
                elif event.key == pygame.K_z:
                    game.apply_reward()
            # ---------------- NEW MOVE ----------------
            elif game.state == "NEW_MOVE":
                moves_count = len(game.pending_pokemon.moves) if game.pending_pokemon else 0
                total_options = moves_count + 1  # last = Cancel

                if event.key == pygame.K_DOWN:
                    game.selected_index = (game.selected_index + 1) % total_options
                elif event.key == pygame.K_UP:
                    game.selected_index = (game.selected_index - 1) % total_options
                elif event.key == pygame.K_z:
                    # safety check
                    if not game.pending_pokemon or not game.pending_move:
                        game.message = "No pending move."
                        game.state = "BATTLE"
                    else:
                        if game.selected_index < moves_count:
                            forgotten = game.pending_pokemon.moves[game.selected_index].name
                            game.pending_pokemon.moves[game.selected_index] = game.pending_move
                            game.message = f"{game.pending_pokemon.name} forgot {forgotten} and learned {game.pending_move.name}!"
                        else:  # Cancel
                            game.message = f"{game.pending_pokemon.name} did not learn {game.pending_move.name}."

                        # ถ้าการเรียกมาจาก Rare Candy (reward flow) กลับไป REWARD
                        if getattr(game, "reward_action", "") == "Rare Candy":
                            game.state = "REWARD"
                            # ล้าง reward_action เพื่อไม่ให้ติดข้ามรอบ
                            game.reward_action = ""
                        else:
                            game.state = "BATTLE"

                        game.pending_move = None
                        game.pending_pokemon = None
                        game.selected_index = 0
            # ---------------- GAME OVER / WIN ----------------
            elif game.state in ["GAME_OVER","WIN"]:
                if event.key == pygame.K_z:
                    game.restart()

    # ---------------- DRAW ----------------
    if game.state == "MENU":
        game.draw_menu()
    elif game.state == "STAGE":
        game.draw_stage_info()
    elif game.state == "BATTLE":
        game.draw_battle()
    elif game.state == "BATTLE_SKILL_SELECT":
        game.draw_skill_selection()
    elif game.state == "BAG":
        game.draw_bag()
    elif game.state == "SWITCH_PKM":
        game.draw_switch_pokemon()
    elif game.state == "CATCH_ANIMATION":
        game.draw_catch_animation()
    elif game.state == "REWARD":
        game.draw_reward_phase()
    elif game.state == "REWARD_SELECT":
        game.draw_reward_select()
    elif game.state == "NEW_MOVE":
        game.draw_new_move()
    elif game.state == "GAME_OVER":
        game.draw_game_over()
    elif game.state == "WIN":
        game.draw_win()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()