"""
data_loader.py
================
Phase 1a: Pull real Formula 1 race data using the FastF1 package.

FastF1 wraps the official F1 timing API. It needs an internet connection
to fetch data the first time -- after that it caches locally so repeat
runs are instant.

WHAT THIS FILE DOES:
  1. Enables a local cache (so we don't re-download every time)
  2. Loads a specific race session (year, Grand Prix, session type)
  3. Pulls the lap-by-lap data: lap time, tire compound, tire age, and
     whether the lap was "clean" (not affected by pit stops, safety
     cars, etc. -- we need clean laps to measure tire degradation
     accurately, otherwise a slow in/out lap would look like a tire
     falling apart when really it was just a pit stop)

Run this file directly to sanity-check that data loads correctly:
    python data_loader.py
"""

import fastf1
import pandas as pd
import os

# Cache directory -- change this path if you want the cache elsewhere.
# First run will download data (~seconds to a minute); every run after
# that reads from disk and is fast.
os.makedirs('f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('f1_cache')


def load_race_laps(year: int, grand_prix: str, session_type: str = 'R') -> pd.DataFrame:
    """
    Load lap data for a given race.

    Parameters
    ----------
    year : e.g. 2023
    grand_prix : e.g. 'Bahrain', 'Monza', 'Silverstone' (matches FastF1's
                 event naming -- see fastf1.get_event_schedule(year) if
                 a name doesn't match)
    session_type : 'R' = Race, 'Q' = Qualifying, 'FP1'/'FP2'/'FP3' = Practice

    Returns
    -------
    A pandas DataFrame with one row per lap, per driver, including:
        Driver, LapNumber, LapTime, Compound, TyreLife, IsAccurate
    """
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()  # this is the step that needs internet access

    laps = session.laps

    # IsAccurate: FastF1's own flag for laps that are representative
    # (excludes laps with track limit violations, safety car laps, etc.)
    # We additionally drop pit-in/pit-out laps ourselves below, since
    # those are slow for reasons unrelated to tire degradation.
    clean_laps = laps[
        laps['PitInTime'].isna() &
        laps['PitOutTime'].isna() &
        laps['IsAccurate']
    ].copy()

    # Keep only the columns we actually need downstream
    clean_laps = clean_laps[[
        'Driver', 'LapNumber', 'LapTime', 'Compound', 'TyreLife'
    ]]

    # LapTime comes in as a pandas Timedelta -- convert to seconds
    # (float) since that's much easier to do math with later.
    clean_laps['LapTimeSeconds'] = clean_laps['LapTime'].dt.total_seconds()

    return clean_laps.dropna(subset=['LapTimeSeconds', 'Compound', 'TyreLife'])


if __name__ == '__main__':
    # Quick manual test -- pick any real race here.
    df = load_race_laps(2023, 'Bahrain', 'R')
    print(f"Loaded {len(df)} clean laps.")
    print(df.head(10))
    print("\nCompounds seen:", df['Compound'].unique())
