import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class CompoundModel:
    compound: str
    base_pace: float
    degradation_rate: float
    n_laps_used: int


def fit_degradation_models(laps: pd.DataFrame):

    models = {}

    for compound, group in laps.groupby("Compound"):

        group = group[
            (group["LapTimeSeconds"] > 60)
            & (group["LapTimeSeconds"] < 130)
        ].copy()

        print(f"{compound}: {len(group)} laps")

        if len(group) < 5:
            continue

        driver_medians = (
            group.groupby("Driver")["LapTimeSeconds"]
            .transform("median")
        )

        group["NormalizedLapTime"] = (
            group["LapTimeSeconds"] - driver_medians
        )

        x = group["TyreLife"].astype(float).to_numpy()
        y = group["NormalizedLapTime"].astype(float).to_numpy()

        slope, intercept = np.polyfit(x, y, 1)

        models[compound] = CompoundModel(
            compound=compound,
            base_pace=float(intercept),
            degradation_rate=float(slope),
            n_laps_used=len(group)
        )

    return models


def print_models(models):

    print("\nResults")
    print("-" * 40)

    for model in models.values():
        print(
            f"{model.compound:10}"
            f"{model.degradation_rate:10.4f}"
            f"{model.n_laps_used:10}"
        )


if __name__ == "__main__":

    from data_loader import load_race_laps

    laps = load_race_laps(2023, "Bahrain", "R")

    models = fit_degradation_models(laps)

    print_models(models) 
    if model.n_laps_used < 30:
    print(
        f"Warning: {compound} has limited data"
    )
    