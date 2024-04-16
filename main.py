import pygame as pg
import constants as c
import json
import time
import threading
from enemy import Enemy
from world import World

# Inicjalizacja pygame
pg.init()

# Odświeżanie gry
clock = pg.time.Clock()

# Tworzenie okienka gry
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Załaduj obrazy
map_image = pg.image.load('assets/maps/map.png').convert_alpha()
enemy_image = pg.image.load('assets/enemies/enemy1.png').convert_alpha()

# Załaduj plik json ze ścieżką
with open('assets/maps/dzialajpls.tmj') as file:
    world_data = json.load(file)

# Tworzenie mapy
world = World(world_data, map_image)
world.process_data()

# Tworzenie grupy przeciwników
enemy_group = pg.sprite.Group()

# Czas pojawienia się pierwszego przeciwnika
enemy_spawn_timer = 0
enemy_spawn_interval = 2000  # 2000 milisekund (2 sekundy) między pojawieniami się przeciwników

def play_music(sciezka_do_pliku):
    # Inicjalizacja biblioteki pygame
    pg.init()

    # Odtwarzanie muzyki
    pg.mixer.music.load(sciezka_do_pliku)
    pg.mixer.music.play()
    pg.mixer.music.set_volume(0)

sciezka_do_pliku = "muzyka.mp3"  # Ścieżka do pliku audio

# Tworzenie wątku do odtwarzania muzyki
music_thread = threading.Thread(target=play_music, args=(sciezka_do_pliku,))
music_thread.start()

# Game loop
run = True
while run:
    # Zegar kontrolujący FPS
    clock.tick(c.FPS)

    # Oblicz czas od ostatniego pojawienia się przeciwnika
    enemy_spawn_timer += clock.get_time()
    if enemy_spawn_timer >= enemy_spawn_interval:
        enemy = Enemy(world.waypoints, enemy_image)
        enemy_group.add(enemy)
        enemy_spawn_timer = 0  # Resetowanie timera

    # Rysowanie i inne operacje
    screen.fill("grey100")
    world.draw(screen)
    enemy_group.update()
    enemy_group.draw(screen)

    # Obsługa zdarzeń
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Aktualizacja wyświetlanego obrazu
    pg.display.flip()

pg.quit()
