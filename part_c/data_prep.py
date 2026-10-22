"""Shared, explicit title aggregation for the Part C notebook and explorers."""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data/Video_games_dataset.csv"
SALES = ["GlobalSales", "NASales", "EUSales", "JapanSales", "OtherSales"]
CATEGORY_NAMES = ["Failure", "Moderate success", "Success", "Major Hit", "Blockbuster"]
THRESHOLDS = {
    "GlobalSales": [10, 50, 100, 500],
    "NASales": [5, 20, 50, 200],
    "EUSales": [5, 15, 40, 150],
    "JapanSales": [2, 10, 30, 100],
}
BINARY = [
    "Online", "Multiplayer", "Licensed", "Handheld", "Anime", "Arcade",
    "Fighting", "MedievalFantasy", "Puzzle", "RealTime", "SciFi", "Shooter",
    "FirstPerson", "Isometric", "SideScrolling", "TopDown", "ThirdPerson",
]


def add_success(frame):
    frame = frame.copy()
    for col, limits in THRESHOLDS.items():
        cents = np.rint(frame[col] * 100).astype(int)
        # searchsorted(left) keeps exact boundaries in the lower category
        codes = np.searchsorted(limits, cents, side="left")
        frame[col + "TierCode"] = codes
        frame[col + "Tier"] = pd.Categorical.from_codes(
            codes, categories=CATEGORY_NAMES, ordered=True
        )
        frame[col + "Success"] = (codes >= 2).astype(int)
    return frame


def load_data():
    raw = pd.read_csv(SOURCE)
    raw["Multiplayer"] = (raw.MaxPlayers >= 2).astype(int)
    genre_names = sorted({g.strip() for text in raw.Genre for g in text.split(",")})
    genre_cols = []
    for genre in genre_names:
        col = "Genre: " + genre
        raw[col] = raw.Genre.map(lambda text: int(genre in [g.strip() for g in text.split(",")]))
        genre_cols.append(col)
    grouped = raw.groupby("Title", sort=True)
    titles = pd.DataFrame(index=grouped.size().index)
    titles["RecordedConsoles"] = grouped.Console.nunique()
    titles["ConsoleNames"] = grouped.Console.agg(lambda v: " | ".join(sorted(v)))
    titles["YearReleased"] = grouped.YearReleased.min()
    titles["LastRecordedYear"] = grouped.YearReleased.max()
    titles["ReviewScore"] = grouped.ReviewScore.mean()
    titles["ReviewMin"] = grouped.ReviewScore.min()
    titles["ReviewMax"] = grouped.ReviewScore.max()
    titles["Rating"] = grouped.Rating.agg(lambda v: v.iloc[0] if v.nunique() == 1 else "Mixed")
    for col in SALES:
        cents = raw.assign(_cents=np.rint(raw[col] * 100).astype(int)).groupby("Title")._cents.sum()
        titles[col] = cents / 100
    for col in BINARY + genre_cols:
        lower, upper = grouped[col].min(), grouped[col].max()
        titles[col] = lower.where(lower == upper, np.nan)
        titles[col + "Any"] = upper
        titles[col + "All"] = lower
    titles["ReachGroup"] = np.where(titles.RecordedConsoles == 1, "1 console", "2+ consoles")
    titles["Cohort"] = pd.cut(titles.YearReleased, [2003, 2006, 2008, 2010], labels=["2004-06", "2007-08", "2009-10"])
    titles["ReviewBand"] = pd.cut(
        titles.ReviewScore, [-np.inf, 20, 50, 75, 90, np.inf], right=False,
        labels=["Below 20", "20-49", "50-74", "75-89", "90-100"],
    )
    return raw, add_success(titles), genre_cols
