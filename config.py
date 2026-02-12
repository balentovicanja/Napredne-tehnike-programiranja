from __future__ import annotations

from pathlib import Path
from typing import Final


DATA_DIR: Final[Path] = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Putanja do datoteke s podacima
DATA_FILE: Final[Path] = DATA_DIR / "expenses.json"

# Kategorije
CATEGORIES: Final[list[str]] = [
    "Hrana",
    "Transport",
    "Zabava",
    "Stanovanje",
    "Zdravstvo",
    "Obrazovanje",
    "Plaća",
    "Ostalo"
]

# Format datuma
DATE_FORMAT: Final[str] = "%Y-%m-%d"

# Početna valuta
CURRENCY: Final[str] = "EUR"

# Interval za automatsko spremanje podataka (sekunde)
AUTO_SAVE_INTERVAL: Final[int] = 30

# Interval za recalculation statistike (sekunde)
STATS_RECALC_INTERVAL: Final[int] = 5
