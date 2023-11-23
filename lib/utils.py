from datetime import *
from dateutil.relativedelta import *
import pandas as pd
import yfinance as yf
import mplfinance as mpf


def get_dates():
    # Dates
    today = datetime.now()
    last_friday = (today + relativedelta(weekday=FR(-1))).replace(
        hour=23, minute=59, second=59
    )
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

    return {
        "today": today,
        "last_friday": last_friday,
        "last_monday": last_monday,
        "last_quarter": last_quarter,
        "last_year": last_year,
        "last_5_year": last_5_year,
    }


def format_date(date):
    return date.strftime("%y-%m-%d")


def load_stocks(symbols, interval, start, end):
    df = yf.download(
        symbols,
        interval=interval,
        start=start,
        end=end,
        group_by="ticker",
    )

    return df


def get_returns(history, constituents, label):
    returns = []

    for symbol in constituents.loc[:, "Symbol"].to_list():
        last_year_close = history[symbol]["Close"].iloc[0]
        last_week_close = history[symbol]["Close"].iloc[-1]

        yoy_return = (last_week_close - last_year_close) / last_year_close

        name = constituents.loc[
            constituents["Symbol"] == symbol, "Name"
        ].values[0]

        returns.append([symbol, name, yoy_return])

    df = pd.DataFrame(
        returns,
        columns=[
            "Symbol",
            "Name",
            label,
        ],
    )
    df.sort_values(by=[label], inplace=True, ascending=False)

    return df


def make_chart(df, title, strategy, filename):
    print("making chart for: %s" % title)

    mc = mpf.make_marketcolors(
        up="tab:green",
        down="tab:red",
        edge={"up": "green", "down": "red"},
        wick={"up": "green", "down": "red"},
        volume={"up": "green", "down": "red"},
    )

    s = mpf.make_mpf_style(
        y_on_right=True,
        marketcolors=mc,
    )

    mpf.plot(
        df,
        title=title,
        type="candle",
        # volume=True,
        style=s,
        datetime_format="%y-%b-%d",
        scale_padding={"top": 0.5, "left": 0.2, "bottom": 1, "right": 1},
        savefig="pages/assets/%s/charts/%s.webp" % (strategy, filename),
    )
