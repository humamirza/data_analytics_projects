# transform.py — Step T in ETL
# Takes raw DataFrame, returns clean enriched DataFrame

import pandas as pd

def transform_weather(df):
    print(f"Transforming {len(df)} records...")

    # ── 1. DROP BAD ROWS ─────────────────────────────────────
    # If temperature is missing the row is useless, drop it
    df = df.dropna(subset=["temp_c", "city"])

    # ── 2. ROUND NUMBERS ─────────────────────────────────────
    # API gives many decimal places — round to 1 for readability
    df["temp_c"]     = df["temp_c"].round(1)
    df["feels_like"] = df["feels_like"].round(1)
    df["wind_speed"] = df["wind_speed"].round(1)

    # ── 3. HEAT CATEGORY ─────────────────────────────────────
    # Create a human-readable category for how hot it is
    # This is a new column you are deriving from existing data
    def heat_category(temp):
        if   temp >= 42: return "Extreme Heat"
        elif temp >= 38: return "Very Hot"
        elif temp >= 30: return "Hot"
        elif temp >= 20: return "Warm"
        else:            return "Mild"

    df["heat_category"] = df["temp_c"].apply(heat_category)

    # ── 4. HEAT INDEX ────────────────────────────────────────
    # How much hotter it feels because of humidity
    # Formula: felt_heat = temp + (humidity / 100) * 10
    # This is simplified but gives a useful extra metric
    df["felt_heat_index"] = (
        df["temp_c"] + (df["humidity"] / 100) * 10
    ).round(1)

    # ── 5. HIGH WIND FLAG ────────────────────────────────────
    # True/False column: is wind above normal for UAE?
    # 7.5 m/s = about 27 km/h, noticeable wind in desert
    df["high_wind_alert"] = df["wind_speed"] > 7.5

    # ── 6. CLEAN TEXT ────────────────────────────────────────
    # Capitalise description: "clear sky" → "Clear Sky"
    df["description"] = df["description"].str.title()

    print(f"Transform complete. Columns: {list(df.columns)}")
    return df