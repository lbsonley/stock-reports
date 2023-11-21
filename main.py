from pathlib import Path
from datetime import *
from dateutil.relativedelta import *
from lib.analyze import outperformers

# Dates
today = datetime.now()
last_friday = today + relativedelta(weekday=FR(-1))
last_monday = (last_friday + relativedelta(weekday=MO(-1))).replace(
    hour=0, minute=0, second=0, microsecond=0
)
last_quarter = (last_friday + relativedelta(weeks=-13)).replace(
    hour=0, minute=0, second=0, microsecond=0
)
last_year = (last_friday + relativedelta(weeks=-52)).replace(
    hour=0, minute=0, second=0, microsecond=0
)
last_5_year = (last_friday + relativedelta(weeks=-260)).replace(
    hour=0, minute=0, second=0, microsecond=0
)

print("Fetching data for:")
print("Strategy: Outperformers")
print("Period: 1 Week")
outperformers(
    start=last_monday,
    end=last_friday,
    interval="30m",
    period="1w",
)

print("Fetching data for:")
print("Strategy: Outperformers")
print("Period: 1q")
outperformers(
    start=last_quarter,
    end=last_friday,
    interval="1d",
    period="1q",
)

print("Fetching data for:")
print("Strategy: Outperformers")
print("Period: 1y")
outperformers(
    start=last_year,
    end=last_friday,
    interval="1wk",
    period="1y",
)

print("Fetching data for:")
print("Strategy: Outperformers")
print("Period: 5y")
outperformers(
    start=last_5_year,
    end=last_friday,
    interval="1mo",
    period="5y",
)
