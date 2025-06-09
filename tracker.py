# tracker.py
import pandas as pd
import os
from datetime import datetime

LEVELS = [
    (0, "Wretch"),
    (250, "Lost Soul"),
    (500, "Training Dummy"),
    (1000, "Nokken"),
    (1500, "Nightmare"),
    (2000, "Thrall"),
    (3000, "Shadow"),
    (4000, "Legionnaire"),
    (5000, "Draugr"),
    (7500, "Hel-Walker"),
    (10000, "Reaver"),
    (12500, "Stalker"),
    (15000, "Berserker"),
    (17500, "Seidr Mage"),
    (20000, "Einherjar"),
    (25000, "Tatzelwurm"),
    (30000, "Valkyrie"),
    (35000, "Ogre"),
    (40000, "Champion of Midgard"),
    (45000, "Ancient"),
    (50000, "Demi-God"),
    (60000, "God of War"),
    (80000, "Allfather Slayer"),
    (100000, "Ragnarök Incarnate")
]

def update_log_and_stats(entry, log_path):
    try:
        if os.path.exists(log_path):
            df = pd.read_excel(log_path, engine="openpyxl")
            if df.empty or df.columns.empty:
                df = pd.DataFrame(columns=list(entry.keys()))
        else:
            raise FileNotFoundError
    except Exception:
        df = pd.DataFrame(columns=list(entry.keys()))

    for col in entry.keys():
        if col not in df.columns:
            df[col] = None

    df.loc[len(df)] = entry
    df.to_excel(log_path, index=False, engine="openpyxl")

def get_summary_stats(log_path):
    if not os.path.exists(log_path):
        return {}, []

    df = pd.read_excel(log_path, engine="openpyxl")
    if df.empty:
        return {}, []

    def calc_volume(row):
        try:
            sets, reps = map(int, row['Battle Plan'].split('x'))
            return sets * reps * float(row['Weight (kg)'])
        except:
            return 0

    df['Volume'] = df.apply(calc_volume, axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    df['DateStr'] = df['Date'].dt.strftime('%Y-%m-%d')

    total_volume = df['Volume'].sum()
    days_logged = df['DateStr'].nunique()
    avg_volume = round(total_volume / days_logged, 2) if days_logged else 0

    current_title = LEVELS[0][1]
    next_title = None
    to_next = None
    xp_percent = 0
    prev_threshold = 0

    for threshold, title in LEVELS:
        if total_volume >= threshold:
            current_title = title
            prev_threshold = threshold
        else:
            next_title = title
            to_next = threshold - total_volume
            xp_percent = int(((total_volume - prev_threshold) / (threshold - prev_threshold)) * 100)
            break

    stats = {
        "total_volume": int(total_volume),
        "days_logged": days_logged,
        "avg_per_day": avg_volume,
        "current_title": current_title,
        "next_title": next_title,
        "to_next": int(to_next) if to_next else None,
        "xp_percent": xp_percent
    }

    daily = df.groupby('DateStr')['Volume'].sum().reset_index()
    chart_data = daily.to_dict(orient='records')

    return stats, chart_data
