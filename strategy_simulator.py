from dataclasses import dataclass


# =====================
# CONFIGURATION
# =====================

TOTAL_LAPS = 57
PIT_LOSS = 22.0
FUEL_EFFECT = 0.03


# =====================
# TYRE MODEL
# =====================

@dataclass
class Compound:
    name: str
    base_pace: float
    degradation: float


SOFT = Compound(
    name="SOFT",
    base_pace=90.0,
    degradation=0.10
)

MEDIUM = Compound(
    name="MEDIUM",
    base_pace=90.4,
    degradation=0.07
)

HARD = Compound(
    name="HARD",
    base_pace=90.8,
    degradation=0.04
)


# =====================
# STINT SIMULATION
# =====================

def simulate_stint(compound, laps, race_lap_start):

    total_time = 0

    for tyre_age in range(laps):

        current_race_lap = race_lap_start + tyre_age

        fuel_remaining = TOTAL_LAPS - current_race_lap

        lap_time = (
            compound.base_pace
            + tyre_age * compound.degradation
            + fuel_remaining * FUEL_EFFECT
        )

        total_time += lap_time

    return total_time


# =====================
# FULL RACE
# =====================

def race_time(strategy):

    total_time = 0
    current_race_lap = 0

    for i, (compound, stint_length) in enumerate(strategy):

        total_time += simulate_stint(
            compound,
            stint_length,
            current_race_lap
        )

        current_race_lap += stint_length

        if i < len(strategy) - 1:
            total_time += PIT_LOSS

    return total_time


# =====================
# FIND BEST ONE STOP
# =====================

best_one_stop_time = float("inf")
best_one_stop_lap = None

for stop_lap in range(10, 45):

    strategy = [
        (MEDIUM, stop_lap),
        (HARD, TOTAL_LAPS - stop_lap)
    ]

    t = race_time(strategy)

    if t < best_one_stop_time:
        best_one_stop_time = t
        best_one_stop_lap = stop_lap


# =====================
# FIND BEST TWO STOP
# =====================

best_two_stop_time = float("inf")
best_two_stop_strategy = None

for stop1 in range(8, 25):

    for stop2 in range(stop1 + 10, 50):

        strategy = [
            (SOFT, stop1),
            (MEDIUM, stop2 - stop1),
            (SOFT, TOTAL_LAPS - stop2)
        ]

        t = race_time(strategy)

        if t < best_two_stop_time:
            best_two_stop_time = t
            best_two_stop_strategy = (stop1, stop2)


# =====================
# RESULTS
# =====================

print("\n========== RESULTS ==========\n")

print(
    f"Best one-stop: Pit lap {best_one_stop_lap}"
)

print(
    f"Race time: {best_one_stop_time:.2f} s\n"
)

print(
    f"Best two-stop: Pit laps {best_two_stop_strategy[0]}"
    f" and {best_two_stop_strategy[1]}"
)

print(
    f"Race time: {best_two_stop_time:.2f} s\n"
)

if best_one_stop_time < best_two_stop_time:
    print(" One-stop strategy wins")
else:
    print(" Two-stop strategy wins")
print("\nLap    Time")

for stop_lap in range(10, 45):

    strategy = [
        (MEDIUM, stop_lap),
        (HARD, TOTAL_LAPS - stop_lap)
    ]

    t = race_time(strategy)

    print(f"{stop_lap:<5} {t:.2f}")
from degradation_model import fit_degradation_models
from data_loader import load_race_laps

laps = load_race_laps(2023, "Bahrain", "R")
models = fit_degradation_models(laps)
SOFT.degradation = models["SOFT"].degradation_rate
MEDIUM.degradation = models["MEDIUM"].degradation_rate
HARD.degradation = models["HARD"].degradation_rate
for compound, model in models.items():

    if model.n_laps_used < 30:
        print(
            f"Warning: {compound} has limited data "
            f"({model.n_laps_used} laps)"
        )
    # =====================
# REAL DATA CONNECTION
# =====================

from degradation_model import fit_degradation_models
from data_loader import load_race_laps

race_laps = load_race_laps(2023, "Bahrain", "R")
models = fit_degradation_models(race_laps)

SOFT.degradation = models["SOFT"].degradation_rate
MEDIUM.degradation = models["MEDIUM"].degradation_rate
HARD.degradation = models["HARD"].degradation_rate

for compound, model in models.items():
    if model.n_laps_used < 30:
        print(
            f"Warning: {compound} has limited data "
            f"({model.n_laps_used} laps)"
        )


# =====================
# STRATEGY CURVE PLOT
# =====================

import matplotlib.pyplot as plt

pit_laps = []
race_times = []

for stop_lap in range(10, 45):

    strategy = [
        (MEDIUM, stop_lap),
        (HARD, TOTAL_LAPS - stop_lap)
    ]

    t = race_time(strategy)

    pit_laps.append(stop_lap)
    race_times.append(t)

plt.figure(figsize=(8, 5))

plt.plot(
    pit_laps,
    race_times,
    marker="o"
)

plt.xlabel("Pit Stop Lap")
plt.ylabel("Total Race Time (s)")
plt.title("One-Stop Strategy Optimisation")

plt.grid(True)

plt.savefig("strategy_curve.png")

print("\nGraph saved as strategy_curve.png")