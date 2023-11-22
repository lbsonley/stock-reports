from pathlib import Path
from datetime import *
from dateutil.relativedelta import *
from lib.analyze import *
from lib.utils import get_dates

dates = get_dates()

print("Fetching data for:")
print("Strategy: Outperformers")
print("Period: 1 Week")
outperformers_index_sector(
    start=dates["last_monday"],
    end=dates["last_friday"],
    interval="30m",
    period="1w",
)

print("Fetching data for:")
print("Strategy: Outperformers")
print("Period: 1q")
outperformers_index_sector(
    start=dates["last_quarter"],
    end=dates["last_friday"],
    interval="1d",
    period="1q",
)

print("Fetching data for:")
print("Strategy: Outperformers")
print("Period: 1y")
outperformers_index_sector(
    start=dates["last_year"],
    end=dates["last_friday"],
    interval="1wk",
    period="1y",
)

print("Fetching data for:")
print("Strategy: Outperformers")
print("Period: 5y")
outperformers_index_sector(
    start=dates["last_5_year"],
    end=dates["last_friday"],
    interval="1mo",
    period="5y",
)

outperformers_stocks("1y")
