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
enemy1_image = pg.image.load('assets/enemies/enemy3.png').convert_alpha()
enemy2_image = pg.image.load('assets/enemies/enemy2.png').convert_alpha()

# Załaduj plik json ze ścieżką
with open('assets/maps/dzialajpls.tmj') as file:
    world_data = json.load(file)

# Tworzenie mapy
world = World(world_data, map_image)
world.process_data()

# Tworzenie grupy przeciwników
enemy_group = pg.sprite.Group()
group_lock = threading.Lock()  # Lock dla grupy

# Czas pojawienia się pierwszego przeciwnika
enemy_spawn_timer = 0
enemy_spawn_interval = 2000  # 2000 milisekund (2 sekundy) między pojawieniami się przeciwników

def play_music(sciezka_do_pliku):
    # Inicjalizacja biblioteki pygame
    pg.init()

    # Odtwarzanie muzyki
    pg.mixer.music.load(sciezka_do_pliku)
    pg.mixer.music.play()

sciezka_do_pliku = "muzyka.mp3"  # Ścieżka do pliku audio

# Tworzenie wątku do odtwarzania muzyki
#music_thread = threading.Thread(target=play_music, args=(sciezka_do_pliku,))
#music_thread.start()


def spawn_enemy(enemy_image):
    group_lock.acquire()
    enemy = Enemy(world.waypoints, enemy_image)
    group_lock.release()
    enemy_group.add(enemy)

    time.sleep(1)


# Uruchomienie wątków dla przeciwników
enemy1 = threading.Thread(target=spawn_enemy, args=(Enemy, ) ).start()  # Przeciwnik typu 1 co 2 sekundy
enemy2 = threading.Thread(target=spawn_enemy, args=(Enemy, ) ).start()  # Przeciwnik typu 2 co 2 sekundy


# Game loop
run = True
while run:
    # Zegar kontrolujący FPS
    clock.tick(c.FPS)

    # Rysowanie i inne operacje
    screen.fill("grey100")
    world.draw(screen)
    
    enemy1.join()
    enemy2.join()

    # Obsługa zdarzeń
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Aktualizacja wyświetlanego obrazu
    pg.display.flip()

pg.quit()