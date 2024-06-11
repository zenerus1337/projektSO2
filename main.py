import pygame
import os
import math
import json
import threading
import time

# Initialize Pygame
pygame.init()

# Constants
screen_width, screen_height = 960, 960
FPS = 60

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
laser_color = red  # Color of the laser

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Tower Defense Game")

base_folder = os.path.join(os.getcwd(), 'resources')
map_image = pygame.image.load(os.path.join(base_folder, 'map.png')).convert_alpha()


# Load the path from a json file
with open(os.path.join(base_folder, 'dzialajpls.tmj')) as file:
    world_data = json.load(file)

# Game state
game_over = False
enemies = []
towers = []
lasers = []
spikes = []
money = 400
lives = 20
current_wave = 0
selected_tower_position = None
selected_tower_type = None
win = False
spawn_event = threading.Event()

# Lock and flag for the enemies list
lock = threading.Lock()
game_over_flag = threading.Event()



class Enemy:
    def __init__(self, path, health, speed, reward):
        self.path = path
        self.waypoints = [pygame.math.Vector2(p) for p in path]
        self.pos = pygame.math.Vector2(self.waypoints[0])
        self.health = health
        self.initial_health = health  
        self.speed = speed
        self.alive = True
        self.reward = reward
        self.target_waypoint = 1
        self.movement = pygame.math.Vector2(0, 0)
    
    def move(self):
        if self.target_waypoint < len(self.waypoints):
            target = self.waypoints[self.target_waypoint]
            self.movement = target - self.pos
        else:
            self.alive = False
            return True  

        dist = self.movement.length()
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

        return False

    def draw(self):
        screen.blit(self.image, (int(self.pos.x), int(self.pos.y)))
        self.draw_health_bar()  

    def draw_health_bar(self):
        bar_width = 20
        bar_height = 5
        fill = (self.health / self.initial_health) * bar_width
        health_bar_background = pygame.Rect(self.pos.x, self.pos.y - 10, bar_width, bar_height)
        health_bar_fill = pygame.Rect(self.pos.x, self.pos.y - 10, fill, bar_height)

        # Rysowanie paska zdrowia
        pygame.draw.rect(screen, red, health_bar_background)
        pygame.draw.rect(screen, green, health_bar_fill)

class FastEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path, health=45, speed=5, reward=20)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "fast_enemy.png")), (40, 40))

class StrongEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path, health=60, speed=2, reward=20)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "strong_enemy.png")), (40, 40))

class Boss(Enemy):
    def __init__(self, path):
        super().__init__(path, health=1000, speed=3, reward = 100)  
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "boss.png")), (60, 60))

class ArmoredEnemy(Enemy):
    def __init__(self, path):
        super().__init__(path, health=200, speed=3, reward = 50)  
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "armored_enemy.png")), (40, 40))



class Tower:
    def __init__(self, pos, range, damage, cooldown, cost):
        self.pos = pygame.math.Vector2(pos)
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self.cost = cost
        self.last_shot = 0

    def in_range(self, enemy):
        return (self.pos - enemy.pos).length() <= self.range

    def shoot(self, enemies, lasers):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.cooldown:
            for enemy in enemies:
                if self.in_range(enemy):
                    self.attack(enemy, lasers)
                    self.last_shot = current_time
                    break

    def attack(self, enemy, lasers):
        enemy.health -= self.damage
        if enemy.health <= 0:
            enemy.alive = False
        lasers.append((self.pos, enemy.pos))

    def draw(self):
        if self.image:
            screen.blit(self.image, (int(self.pos.x - 30), int(self.pos.y - 30)))

class SniperTower(Tower):
    icon = pygame.image.load(os.path.join(base_folder, "sniper_tower.png")).convert_alpha()
    cost = 150
    range = 150
    def __init__(self, pos):
        super().__init__(pos, range=150, damage=20, cooldown=1000, cost=150)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "sniper_tower.png")), (60, 60))

class LaserTower(Tower):
    icon = pygame.image.load(os.path.join(base_folder, "laser_tower.png")).convert_alpha()
    cost = 250
    range = 150
    def __init__(self, pos):
        super().__init__(pos, range=150, damage=40, cooldown=2000, cost=250)
        self.area_effect_radius = 150
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "laser_tower.png")), (60, 60))

    def shoot(self, enemies, lasers):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.cooldown:
            primary_target = None
            for enemy in enemies:
                if self.in_range(enemy):
                    primary_target = enemy
                    break
            if primary_target:
                self.attack(primary_target, enemies, lasers)
                self.last_shot = current_time

    def attack(self, primary_target, enemies, lasers):
        for enemy in enemies:
            if (enemy.pos - primary_target.pos).length() <= self.area_effect_radius:
                enemy.health -= self.damage
                if enemy.health <= 0:
                    enemy.alive = False
                lasers.append((self.pos, enemy.pos))

class MotherNature(Tower):
    icon = pygame.image.load(os.path.join(base_folder, "mother_nature.png")).convert_alpha()
    cost = 400
    range = 120
    def __init__(self, pos):
        super().__init__(pos, range=120, damage=25, cooldown=1500, cost=300)  
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "mother_nature.png")), (60, 60))
        self.spikes_duration = 1000  

    def shoot(self, enemies, spikes, lasers):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.cooldown:
            for enemy in enemies:
                if self.in_range(enemy):
                    self.attack(enemy, spikes, lasers)
                    self.last_shot = current_time
                    break

    def attack(self, enemy, spikes, lasers):
        enemy.health -= self.damage
        if enemy.health <= 0:
            enemy.alive = False
        spikes.append((pygame.math.Vector2(enemy.pos), pygame.time.get_ticks()))  
        lasers.append((self.pos, enemy.pos))

class Minigun(Tower):
    icon = pygame.image.load(os.path.join(base_folder, "minigun.png")).convert_alpha()
    cost = 500
    range = 150
    def __init__(self, pos):
        super().__init__(pos, range=150, damage=5, cooldown=50, cost = 500)  
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "minigun.png")), (60, 60))

    def shoot(self, enemies, lasers):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.cooldown:
            for enemy in enemies:
                if self.in_range(enemy):
                    self.attack(enemy, lasers)
                    self.last_shot = current_time
                    break  

    def attack(self, enemy, lasers):
        enemy.health -= self.damage
        if enemy.health <= 0:
            enemy.alive = False
        lasers.append((self.pos, enemy.pos))  



class World():
    def __init__(self, data, map_image):
        self.waypoints = []
        self.level_data = data
        self.image = map_image
    
    def process_data(self):
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                for obj in layer ["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

                    
    def process_waypoints(self,data):
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x,temp_y))

    def draw(self,surface):
        surface.blit(self.image, (0,0))



class LifeManager(threading.Thread):
    def __init__(self, lives, game_over_event, lock):
        super().__init__()
        self.lives = lives
        self.game_over_event = game_over_event
        self.lock = lock
        self.running = True

    def run(self):
        while self.running and not self.game_over_event.is_set():
            time.sleep(0.1)

    def get_lives(self):
        with self.lock:
            return self.lives
        
    def set_lives(self):
        with self.lock:
            self.lives = lives

    def decrease_lives(self, amount):
        with self.lock:
            self.lives -= amount

    def stop(self):
        self.running = False


# Function to spawn enemies in a separate thread
def spawn_enemies(enemies, path, stop_event, game_over_flag):
    wave = waves[current_wave]
    for segment in wave:
        EnemyType = segment["enemy"]
        count = segment["count"]
        spawn_time = segment["spawn_time"]
        for _ in range(count):
            if stop_event.is_set() or game_over_flag.is_set():
                return
            new_enemy = EnemyType(path)
            with lock:
                enemies.append(new_enemy)
            time.sleep(spawn_time)
    stop_event.set()

# Function for playing music
def play_music(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.0)

file_path = os.path.join(base_folder, "muzyka.mp3")

# Draw tower selection menu function
def draw_tower_buttons():
    font = pygame.font.Font(None, 24)  
    for tower_cls, (x, y) in tower_buttons.items():
        button_rect = pygame.Rect(x, y, 40, 40)
        pygame.draw.rect(screen, blue if selected_tower_type == tower_cls else white, button_rect)
        tower_icon = pygame.transform.scale(tower_cls.icon, (40, 40))
        screen.blit(tower_icon, (x, y))
        cost_text = font.render(f"${tower_cls.cost}", True, black)
        screen.blit(cost_text, (x, y + 45))  

# Checking if towers are not overlapping with each other
def is_position_valid(pos, towers, tower_size=60):
    new_tower_rect = pygame.Rect(pos[0] - tower_size // 2, pos[1] - tower_size // 2, tower_size, tower_size)
    for tower in towers:
        existing_tower_rect = pygame.Rect(tower.pos.x - tower_size // 2, tower.pos.y - tower_size // 2, tower_size, tower_size)
        if new_tower_rect.colliderect(existing_tower_rect):
            return False
    return True

# Checking if towers are too close to path
def is_position_on_path(pos, path_points, tower_size=60, path_width=80):
    tower_rect = pygame.Rect(pos[0] - tower_size // 2, pos[1] - tower_size // 2, tower_size, tower_size)
    for i in range(len(path_points) - 1):
        start, end = path_points[i], path_points[i+1]
        if start[0] == end[0]:  
            path_rect = pygame.Rect(start[0] - path_width // 2, min(start[1], end[1]), path_width, abs(end[1] - start[1]))
        else: 
            path_rect = pygame.Rect(min(start[0], end[0]), start[1] - path_width // 2, abs(end[0] - start[0]), path_width)

        if tower_rect.colliderect(path_rect):
            return False  
    return True

# Draw start button
def draw_start_button():
    if current_wave == 0:  
        pygame.draw.rect(screen, green, start_button_rect)
        font = pygame.font.Font(None, 24)
        text = font.render(start_button_text, True, white)
        text_rect = text.get_rect(center=start_button_rect.center)
        screen.blit(text, text_rect)

# Types of tower available
tower_buttons = {
    SniperTower: (10, screen_height - 60),
    LaserTower: (60, screen_height - 60),  
    MotherNature: (110, screen_height - 60),
    Minigun: (160, screen_height - 60)
}

# Start button
start_button_pos = (screen_width - 90, screen_height - 40)
start_button_size = (80, 30)
start_button_rect = pygame.Rect(start_button_pos[0], start_button_pos[1], start_button_size[0], start_button_size[1])
start_button_text = 'Start'

# Create the world
world = World(world_data, map_image)
world.process_data()
ENEMY_PATH = world.waypoints

# Create a thread for playing music
music_thread = threading.Thread(target=play_music, args=(file_path,))
music_thread.start()

# Create a thread for lives
lives_lock = threading.Lock()
game_over_event = threading.Event()
life_manager = LifeManager(lives = lives, game_over_event=game_over_event, lock=lives_lock)
life_manager.start()

# Enemy waves definition
waves = [
    [
        {"enemy": StrongEnemy, "count": 5, "spawn_time": 0.3},
        {"enemy": FastEnemy, "count": 5, "spawn_time": 0.7}
    ],
    [
        {"enemy": StrongEnemy, "count": 10, "spawn_time": 0.8}
    ],
    [
        {"enemy": StrongEnemy, "count": 2, "spawn_time": 0.5},  
        {"enemy": FastEnemy, "count": 3, "spawn_time": 0.5},
        {"enemy": StrongEnemy, "count": 2, "spawn_time": 0.5},
        {"enemy": FastEnemy, "count": 3, "spawn_time": 0.5},
        {"enemy": StrongEnemy, "count": 2, "spawn_time": 0.5},
        {"enemy": FastEnemy, "count": 3, "spawn_time": 0.5},
        {"enemy": StrongEnemy, "count": 2, "spawn_time": 0.5},
        {"enemy": FastEnemy, "count": 3, "spawn_time": 0.5}

    ],
    [
        {"enemy": StrongEnemy, "count": 7, "spawn_time": 0.3},
        {"enemy": FastEnemy, "count": 8, "spawn_time": 0.6},
        {"enemy": StrongEnemy, "count": 7, "spawn_time": 0.3},
        {"enemy": FastEnemy, "count": 8, "spawn_time": 0.6}
    ],
    [
        {"enemy": ArmoredEnemy, "count": 5, "spawn_time": 0.5},
    ],
    [
        {"enemy": ArmoredEnemy, "count": 1, "spawn_time": 0.2},
        {"enemy": FastEnemy, "count": 5, "spawn_time": 0.5},
        {"enemy": ArmoredEnemy, "count": 1, "spawn_time": 0.2},
        {"enemy": FastEnemy, "count": 5, "spawn_time": 0.5},
        {"enemy": ArmoredEnemy, "count": 1, "spawn_time": 0.2},
        {"enemy": FastEnemy, "count": 5, "spawn_time": 0.5}
    ],
    [
        {"enemy": StrongEnemy, "count": 4, "spawn_time": 0.2},
        {"enemy": ArmoredEnemy, "count": 1, "spawn_time": 0.2},
        {"enemy": StrongEnemy, "count": 4, "spawn_time": 0.2},
        {"enemy": ArmoredEnemy, "count": 1, "spawn_time": 0.2},
        {"enemy": StrongEnemy, "count": 4, "spawn_time": 0.2},
        {"enemy": ArmoredEnemy, "count": 1, "spawn_time": 0.2},
        {"enemy": FastEnemy, "count": 10, "spawn_time": 0.2}
    ],
    [
        {"enemy": Boss, "count": 1, "spawn_time": 0.2}
    ]
]


# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(white)


    # Check for wave completion and start new wave
    if spawn_event.is_set() and len(enemies) == 0:
        if current_wave < len(waves) - 1:
            current_wave += 1
            spawn_event.clear()
            enemy_thread = threading.Thread(target=spawn_enemies, args=(enemies, ENEMY_PATH, spawn_event, game_over_flag))
            enemy_thread.start()

    if spawn_event.is_set() and len(enemies) == 0 and current_wave >= len(waves) - 1:
        win = True
        game_over = True  
        game_over_flag.set()


    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            spawn_event.set()

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(pos):
                if current_wave == 0 and not spawn_event.is_set():
                    current_wave += 1
                    spawn_event.clear()
                    enemy_thread = threading.Thread(target=spawn_enemies, args=(enemies, ENEMY_PATH, spawn_event, game_over_flag))
                    enemy_thread.start()
                continue

            if event.button == 1:  
                for tower_cls, (x, y) in tower_buttons.items():
                    if pygame.Rect(x, y, 40, 40).collidepoint(pos):
                        if money >= tower_cls.cost:
                            selected_tower_type = tower_cls
                            selected_tower_position = pos  
                        break
                else:
                    if selected_tower_type:
                        if money >= selected_tower_type.cost and selected_tower_position:
                            if is_position_valid(selected_tower_position, towers) and is_position_on_path(selected_tower_position, ENEMY_PATH):
                                towers.append(selected_tower_type(selected_tower_position))
                                money -= selected_tower_type.cost
                                selected_tower_type = None
                                selected_tower_position = None
            elif event.button == 3:  
                selected_tower_type = None
                selected_tower_position = None


        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            pos = pygame.mouse.get_pos()
            try_again_rect = pygame.Rect(screen_width // 2 - try_again_text.get_width() // 2, screen_height // 2 + 50, try_again_text.get_width(), try_again_text.get_height())
            if try_again_rect.collidepoint(pos):
                if enemy_thread.is_alive():
                    spawn_event.set()  
                    enemy_thread.join()  


                # Reset the game
                enemies.clear()
                towers.clear()
                lasers.clear()
                money = 500
                life_manager.set_lives()
                current_wave = 0
                game_over = False
                win = False
                game_over_flag.clear()  
                spawn_event.clear()  


    # Draw the world
    world.draw(screen)

    # Draw tower selection menu
    draw_tower_buttons()

    # Draw start button
    draw_start_button()

    # Draw tower range
    if selected_tower_type:
        selected_tower_position = pygame.mouse.get_pos()

    if selected_tower_position and selected_tower_type:
        pygame.draw.circle(screen, blue, selected_tower_position, selected_tower_type.range, 1)

    # Update and draw enemies
    with lock:
        for enemy in list(enemies):
            if not game_over: 
                reached_end = enemy.move()
            enemy.draw()
            if reached_end and not game_over:
                life_manager.decrease_lives(1)  
                enemies.remove(enemy)
            elif not enemy.alive:
                enemies.remove(enemy)
                money += enemy.reward
            if life_manager.get_lives() <= 0:
                game_over = True
                game_over_flag.set()

    # Update and draw towers
    lasers.clear()
    with lock:
        if not game_over: 
            for tower in towers:
                tower.draw()
                if isinstance(tower, MotherNature):
                    tower.shoot(enemies, spikes, lasers)  
                else:
                    tower.shoot(enemies, lasers)  
        else:
            for tower in towers:
                tower.draw()

    # Draw lasers and spikes
    for laser in lasers:
        pygame.draw.line(screen, laser_color, laser[0], laser[1], 2)

    for spike, start_time in list(spikes):
        if pygame.time.get_ticks() - start_time > 1000:  
            spikes.remove((spike, start_time))
        else:
            spike_image = pygame.transform.scale(pygame.image.load(os.path.join(base_folder, "spikes.png")), (30, 30))
            screen.blit(spike_image, (spike.x - 10, spike.y - 10))  

            for enemy in enemies:
                if enemy.pos.distance_to(spike) < 20:  
                    enemy.health -= 1  
                    if enemy.health <= 0:
                        enemy.alive = False

    # Display money, lives and waves
    font = pygame.font.Font(None, 36)
    money_text = font.render(f"Money: {money}", True, black)
    lives_text = font.render(f"Lives: {life_manager.get_lives()}", True, black)
    wave_text = font.render(f"Wave: {current_wave}/{len(waves)}", True, black)
    screen.blit(money_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(wave_text, (screen_width - wave_text.get_width() - 10, 10))

    # Display game over screen
    if game_over:
        if win:
            game_over_text = font.render("You win!", True, green)
        else:
            game_over_text = font.render("You lose!", True, red)
        
        try_again_text = font.render("Play again", True, green)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))
        screen.blit(try_again_text, (screen_width // 2 - try_again_text.get_width() // 2, screen_height // 2 + 50))



    # Update display and tick clock
    pygame.display.flip()
    clock.tick(FPS)

# Wait for the enemy spawning thread to finish before exiting
if enemy_thread.is_alive():
    spawn_event.set()
    enemy_thread.join()


if life_manager.is_alive():
    life_manager.stop()
    life_manager.join()
enemy_thread.join()
music_thread.join()
pygame.quit()
