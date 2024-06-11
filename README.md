Zenerus
zenerus
Dostępny

Retsam — 09.06.2024 18:44
Obraz
Obraz
Obraz
Retsam — 09.06.2024 19:27
Obraz
Zenerus — 09.06.2024 20:34
znajdz mi jakieś obrazki na towery
Retsam — 09.06.2024 20:39
Obraz
Obraz
Retsam — 09.06.2024 22:30
Obraz
Obraz
Zenerus — Wczoraj o 15:29
czyli we trójke jednak robimy i guess
Retsam — Wczoraj o 15:31
Ehh no mówił że robię sam więc noo
Zenerus — Wczoraj o 15:49
mi się wydaje że to że on dzieli to na 2 osoby jest bo to żeby studenci debili mieli problem z botem xddddd
Retsam — Wczoraj o 15:50
xD
Retsam — Wczoraj o 17:54
Jak zjem od razu wbijam na dc
Zenerus — Wczoraj o 17:55
ok
Zenerus — Wczoraj o 19:06
import pygame
import os
import math
import json
import threading
import time
Rozwiń
message.txt
17 KB
Retsam — Wczoraj o 19:55
Typ załącznika: acrobat
Sprawozdanie_SO2_projekt.pdf
110.16 KB
Retsam — Wczoraj o 20:10
Obraz
Obraz
Retsam — Wczoraj o 21:08
Obraz
Zenerus — Wczoraj o 21:18
Obraz
Retsam — Wczoraj o 21:23
# Systemy Operacyjne 2 Projekt

## Wydział Informatyki i Telekomunikacji

### Autorzy:
- Michał Kucharek - 264169
Rozwiń
README_2.md
4 KB
Zenerus — Wczoraj o 22:10
Przemek ma 6 wątków
i nie zalicza do tych wątków wątku na muzykę
siedzimy do rana
Retsam — Wczoraj o 22:11
No ale nie mówił ile ma być wątków, miały być dwa to są
Poza tym jakie ma wątki
Zenerus — Wczoraj o 22:12
wątki na wieżę
na hp
i na hajs
i jebac
jak będzie działać to zostawiamy
jak nie będą takie jakie Szandala chce to huj
jest jest
na szybko coś wykombinuje
zrobię se coś do jedzenia i mogę dalej dodać do tego
Retsam — Wczoraj o 22:18
To trzeba będzie jeszcze to readme zmienić, pamiętaj
Zenerus — Wczoraj o 22:25
to dam ci kod co został zmieniony
później
Zenerus — Wczoraj o 23:11
możesz zobaczyć jeszcze threading.set czy coś takiego
Retsam — Wczoraj o 23:16
Już chwila
Szczerze to nie wiem, bot mówi że niby nie można no ale do locka też tak mówił
Ale z drugiej strony bot to powiedział
threading.settrace służy do zupełnie innych celów niż synchronizacja dostępu do sekcji krytycznych. Jest to narzędzie do monitorowania i analizowania zachowania wątków, a nie do bezpiecznego zarządzania współbieżnością.
Zenerus — Wczoraj o 23:23
whatever w takim razie
Zenerus — Dziś o 00:03
import pygame
import os
import math
import json
import threading
import time
Rozwiń
message.txt
22 KB
Retsam — Dziś o 00:14
Tam gdzie jest scr to usuń tę linijkę i w jej miejsce przeciagnij tego scr to się samo doda
Bot dodał jeszcze do tego wątku życie jakieś metody, myślę że to niepotrzebne bo w innych tego nie ma ale z drugiej strony fajnie wygląda więc nie wiem czy to zostawić, jak coś to po prostu usuń te 4 linijki
Na górze jest tjeszcze ta jakby strona tytułowa to nie wiem czy ją zostawiamy czy nie
# Systemy Operacyjne 2 Projekt

## Wydział Informatyki i Telekomunikacji

### Autorzy:
- Michał Kucharek - 264169
Rozwiń
README.md
5 KB
No i najlepiej to po prostu otwórz to readme co masz u siebie w projekcie i skopiuj to co ci wysłałem i tam wklej
Zenerus — Dziś o 00:15
dodał te linijki bo ten wątek to klasa która ma tam jakieś metody
zobaczy się
jutro to zrobię
Retsam — Dziś o 00:16
Okej
﻿
# Systemy Operacyjne 2 Projekt

## Wydział Informatyki i Telekomunikacji

### Autorzy:
- Michał Kucharek - 264169
- Michał Ćwirko - 269178

### Prowadzący:
dr inż. Tomasz Szandała

---

## Tower Defense

Gra została stworzona przy użyciu języka Python, biblioteki Pygame oraz wątków. Celem gry jest ochrona swojej bazy przed wrogami, budując wieże obronne. Wrogowie pojawiają się co pewien czas falami i poruszają się po wyznaczonej ścieżce. Gracz zdobywa pieniądze za pokonywanie wrogów, które może przeznaczyć na budowę dodatkowych wież. Gra oferuje prostą, ale wciągającą mechanikę, która wymaga szybkiego myślenia i skutecznej strategii.

### Zrzut ekranu z gry
![image](https://github.com/zenerus1337/projektSO2/assets/101291038/277bdfbb-c285-4458-b90c-187201fa8533)



### Wątki:
#### 1. Wątek `SpawnEnemy`
- **Reprezentacja**: Wątek ten jest odpowiedzialny za ciągłe tworzenie przeciwników zdefiniowanych w falach. Przeciwnicy są generowani w interwałach określonych dla każdej fali i są dodawani do listy `enemies`, którą wykorzystuje główny wątek gry do zarządzania interakcjami i logiką przeciwników.

- **Inicjacja**: Wątek jest uruchamiany za każdym razem, gdy rozpoczyna się nowa fala przeciwników, co jest kontrolowane przez `spawn_event`. Nowy wątek jest tworzony i startowany z funkcji `spawn_enemies`.

- **Zależności i synchronizacja**:
  - Używa `enemies_lock` do synchronizacji dostępu do listy przeciwników, co zapobiega konfliktom i błędom związanym z jednoczesnym modyfikowaniem tej listy przez różne wątki.
  - Odczytuje flagę `game_over_flag` oraz `stop_event`, aby sprawdzić, czy gra została zakończona lub czy wątek powinien zakończyć działanie przed rozpoczęciem nowej fali.

- **Typ**: Standardowy wątek z Pythona (threading.Thread).

#### 2. Wątek `MusicThread`
- **Reprezentacja**: Odpowiada za odtwarzanie muzyki w tle gry.

- **Inicjacja**: Jest uruchamiany raz podczas startu gry, aby zapętlić odtwarzanie ścieżki dźwiękowej.

- **Zależności i synchronizacja**:
  - Operuje niezależnie od innych wątków, ponieważ zarządzanie muzyką nie wpływa bezpośrednio na mechanikę gry i jest odseparowane od głównego przepływu logiki.
  - Nie używa żadnych mechanizmów synchronizacji z innymi wątkami, ponieważ jego zadania są izolowane.

- **Typ**: Standardowy wątek z Pythona (threading.Thread).

#### 3. Wątek Zarządzania Życiem `LifeManager`
- **Reprezentacja**: Odpowiada za monitorowanie i aktualizację liczby życia gracza. Reaguje na zmiany w grze, które wpływają na życie, takie jak dotarcie przeciwników do bazy.

- **Inicjacja**: Uruchamiany na początku gry, pracuje w tle monitorując i aktualizując życia.

- **Zależności i synchronizacja**:
  - Wykorzystuje `lives_lock` do bezpiecznej zmiany stanu życia.
  - Słucha `game_over_event`, aby zakończyć działanie po zakończeniu gry.

- **Metody**:
  - `decrease_lives(amount)`: Zmniejsza liczbę życia gracza.
  - `get_lives()`: Zwraca aktualną liczbę życia.
  - -`set_live()`: Ustawia życie przy resecie.
  - `stop()`: Bezpiecznie zatrzymuje wątek po zakończeniu rozgrywki.
  
- **Typ**: Standardowy wątek z Pythona (`threading.Thread`).

### Sekcje Krytyczne:
#### 1. Modyfikacja listy przeciwników
- **Opis**: W funkcji `spawn_enemies`, przeciwnicy są tworzeni i dodawani do listy `enemies`. Wątek odpowiedzialny za generowanie przeciwników musi uzyskać blokadę (enemies_lock) przed modyfikacją listy, aby zapewnić, że żaden inny wątek (np. główny wątek gry podczas aktualizacji stanu przeciwników) nie będzie modyfikować listy jednocześnie.

- **Typ Blokady**: Mutex (threading.Lock).

#### 2. Przeglądanie i modyfikacja listy przeciwników
- **Opis**: W głównym wątku gry, podczas rysowania i aktualizacji stanu przeciwników, lista `enemies` jest iterowana, a przeciwnicy są aktualizowani, rysowani lub usuwani. Ta operacja również wymaga blokady, ponieważ w innym przypadku mogą wystąpić konflikty z wątkiem generującym przeciwników.

- **Typ Blokady**: Mutex (threading.Lock).

#### 3. Flagi synchronizacyjne
- 1. **Flaga `spawn_event`**: Kontroluje kiedy nowi przeciwnicy powinni być generowani. Wątek generujący przeciwników czeka na to zdarzenie, aby rozpocząć generowanie nowej fali przeciwników, i ustawia je na zakończenie fali, informując główny wątek gry o możliwości rozpoczęcia nowej fali.
- 2. **Flaga `game_over_flag`**: Ustawiana, gdy gra się kończy (np. gracz przegrywa wszystkie życia). Ta flaga jest sprawdzana przez różne wątki, aby zdecydować, czy kontynuować działanie, czy zakończyć i oczyścić zasoby.
- **Typ**: Zdarzenia (`threading.Event`).
README.md
5 KB
