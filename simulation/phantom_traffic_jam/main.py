# Trödeln und zu frühes Abbremsen führt zum Phantomstau
# Trödelwahrscheinlichkeit simuliert menschliches Verhalten:
# - kurze Unaufmerksamkeit
# - vorsichtiges Fahren
# - spätes Reagieren
# - kleine Störungen im Verkehrsfluss

import random
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
matplotlib.use("TkAgg")

# Parameter
L = 20          # Länge der Straße in Zellen
n_cars = 5      # Anzahl Autos
v_max = 5       # Maximalgeschwindigkeit
p = 0.3         # Trödelwahrscheinlichkeit liegt bei 30%. Wenn Auftritt dann wir die Geschwindigkeit um 1 reduziert v = v -1
steps = 1000      # Simulationsschritte

cars = [
    {"pos": 0, "v": 0},    # Auto mit Index 0
    {"pos": 4, "v": 0},    # Auto mit Index 1
    {"pos": 8, "v": 0},    # Auto mit Index 2
    {"pos": 12, "v": 0},   # Auto mit Index 3
    {"pos": 16, "v": 0},   # Auto mit Index 4
]

def distance_to_next_car(car_index, cars, L):
    current_pos = cars[car_index]["pos"]

    next_index = (car_index + 1) % len(cars) # Wenn letzte Position/ Index dann Modular 
                                             # Rest 0 also Position/ Index 0
    next_pos = cars[next_index]["pos"]

    distance = (next_pos - current_pos) % L
    gap = distance - 1

    return gap

def update(cars, L, v_max, p):
    new_cars = []

    for i, car in enumerate(cars):
        v = car["v"]

        # 1. Beschleunigen
        v = min(v + 1, v_max) # maximale Geschwindigkeit darf nicht überschritten werden

        # 2. Bremsen wegen Abstand
        gap = distance_to_next_car(i, cars, L)
        v = min(v, gap)

        # 3. Trödeln
        if v > 0 and random.random() < p:
            v -= 1

        new_cars.append({
            "pos": car["pos"],
            "v": v
        })

    # 4. Alle Autos gleichzeitig bewegen
    for car in new_cars:
        car["pos"] = (car["pos"] + car["v"]) % L

    return new_cars

def print_road(cars, L):
    road = ["."] * L

    for car in cars:
        road[car["pos"]] = str(car["v"])

    print("".join(road))

################################################################################
# Animation/ Simulation/ Visualisierung
history = []

fig, (ax_road, ax_history) = plt.subplots(1, 2, figsize=(12, 4))


def draw(frame):
    global cars, history

    # aktuellen Zustand speichern
    road_state = [0] * L
    for car in cars:
        road_state[car["pos"]] = 1
    history.append(road_state)

    # linke Grafik: Straße
    ax_road.clear()
    ax_road.set_xlim(-1, L)
    ax_road.set_ylim(-1, 1)
    ax_road.set_yticks([])
    ax_road.set_xlabel("Position")
    ax_road.set_title(f"Straße | Schritt {frame}")

    for x in range(L):
        ax_road.plot(
            x, 0,
            marker="s",
            markersize=14,
            markerfacecolor="white",
            markeredgecolor="black"
        )

    for car in cars:
        ax_road.plot(
            car["pos"], 0,
            marker="s",
            markersize=14
        )
        ax_road.text(
            car["pos"], 0,
            str(car["v"]),
            ha="center",
            va="center",
            color="white"
        )

    # rechte Grafik: Zeit-Ort-Diagramm
    ax_history.clear()
    ax_history.imshow(history, aspect="auto", interpolation="nearest")
    ax_history.set_xlabel("Position")
    ax_history.set_ylabel("Zeitschritt")
    ax_history.set_title("Zeit-Ort-Diagramm")
    ax_history.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19])

    # Simulation einen Schritt weiter
    cars = update(cars, L, v_max, p)


animation = FuncAnimation(
    fig,
    draw,
    frames=steps,
    interval=500,
    repeat=False
)

plt.tight_layout()
plt.show()