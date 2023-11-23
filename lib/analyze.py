from pathlib import Path
import pandas as pd
from lib.dicts import *
from lib.utils import *
from lib.makereport import *


def outperformers_stocks(period):
    dates = get_dates()

    returns_label = returns_labels_by_period[period]
    chart_interval = chart_intervals_by_period[period]
    chart_interval_label = chart_interval_labels_by_period[period]
    outperform_start = start_dates_by_period[period]

    indices_returns = pd.read_csv(
        f'pages/assets/outperformers/returns/{format_date(dates["last_friday"])}/indices-{period}.csv'
    )
    sector_returns = pd.read_csv(
        f'pages/assets/outperformers/returns/{format_date(dates["last_friday"])}/sectors-{period}.csv'
    )

    spx_return = indices_returns.loc[
        indices_returns["Symbol"] == "SPY", returns_label
    ].values[0]

    outperforming_sectors = sector_returns[
        sector_returns[returns_label] > spx_return
    ]
    outperforming_sector_names = outperforming_sectors.loc[:, "Name"].to_list()

    ##############
    # Securities #
    ##############
    sp500_constituents = pd.read_csv("data/sp500-constituents.csv")

    for name in outperforming_sector_names:
        # make directory for charts
        chart_path = f'pages/assets/outperformers/charts/{format_date(dates["last_friday"])}/{name.lower().replace(" ", "-")}'
        Path(chart_path).mkdir(parents=True, exist_ok=True)

        constituents = sp500_constituents.loc[
            sp500_constituents["GICS Sector"] == name
        ]
        constituent_symbols = constituents.loc[:, "Symbol"].to_list()

        constituent_history = load_stocks(
            constituent_symbols,
            chart_interval,
            outperform_start,
            dates["last_friday"],
        )

        constituent_returns = get_returns(
            constituent_history, constituents, returns_label
        )

        sector_return = sector_returns.loc[
            sector_returns["Name"] == name, returns_label
        ].values[0]

        outperforming_stocks = constituent_returns[
            constituent_returns[returns_label] > sector_return
        ]
        outperforming_stocks.to_csv(
            f'pages/assets/outperformers/returns/{format_date(dates["last_friday"])}/{name.lower().replace(" ", "-")}-{period}.csv',
            index=False,
        )
        outperforming_stock_symbols = outperforming_stocks.loc[
            :, "Symbol"
        ].to_list()

        time_frame_configs = [
            ("1wk", "30m", dates["last_monday"]),
            ("1q", "1d", dates["last_quarter"]),
            ("1y", "1wk", dates["last_year"]),
            ("5y", "1mo", dates["last_5_year"]),
        ]

        print("load stocks for sector: %s" % name)
        for period, interval, start in time_frame_configs:
            print(f"load history for interval: {interval}")
            constituent_history = load_stocks(
                outperforming_stock_symbols,
                interval,
                start,
                dates["last_friday"],
            )

            stock_return_label = returns_labels_by_period[period]

            constituent_returns_for_table = get_returns(
                constituent_history,
                outperforming_stocks,
                stock_return_label,
            )
            constituent_returns_for_table.to_csv(
                f'pages/assets/outperformers/returns/{format_date(dates["last_friday"])}/{name.lower().replace(" ", "-")}-{period}.csv',
                index=False,
            )

            for symbol in outperforming_stock_symbols:
                stock_history = constituent_history.loc[:, symbol]
                stock_name = constituents.loc[
                    constituents["Symbol"] == symbol, "Name"
                ].values[0]

                # make sure index column has proper name and type
                if stock_history.index.name == None:
                    stock_history.index.name = "Datetime"

                if (
                    type(stock_history.index)
                    != "<class 'pandas.core.indexes.datetimes.DatetimeIndex'>"
                ):
                    stock_history.index = pd.to_datetime(stock_history.index)

                make_chart(
                    df=stock_history,
                    title="%s (%s) - %s" % (stock_name, symbol, period),
                    strategy="outperformers",
                    filename=f'{format_date(dates["last_friday"])}/{name.lower().replace(" ", "-")}/{symbol}-{period}',
                )
        make_report(
            dates["last_friday"],
            "Securities",
            name.lower().replace(" ", "-"),
            outperforming_stock_symbols,
        )


def outperformers_index_sector(start, end, interval, period):
    returns_label = returns_labels_by_period[period]
    chart_interval_label = chart_interval_labels_by_period[period]

    ###########
    # Indices #
    ###########
    # make directory for charts
    chart_path = "pages/assets/outperformers/charts/%s/indices" % format_date(
        end
    )
    Path(chart_path).mkdir(parents=True, exist_ok=True)

    indices = pd.read_csv("data/indices.csv")
    index_symbols = indices.loc[:, "Symbol"].to_list()

    indices_history = load_stocks(index_symbols, interval, start, end)
    indices_returns = get_returns(indices_history, indices, returns_label)
    indices_returns.to_csv(
        "pages/assets/outperformers/returns/%s/indices-%s.csv"
        % (format_date(end), period),
        index=False,
    )

    for symbol in index_symbols:
        index_history = indices_history.loc[:, symbol]
        index_name = indices.loc[indices["Symbol"] == symbol, "Name"].values[0]
        make_chart(
            df=index_history,
            title="%s (%s) - %s (%s)"
            % (index_name, symbol, period, chart_interval_label),
            strategy="outperformers",
            filename=f"{format_date(end)}/indices/{symbol}-{period}",
        )

    make_report(
        date=end,
        category="Indices",
        report_name="indices",
        symbols=index_symbols,
    )

    ###########
    # Sectors #
    ###########
    # make directory for charts
    chart_path = "pages/assets/outperformers/charts/%s/sectors" % format_date(
        end
    )
    Path(chart_path).mkdir(parents=True, exist_ok=True)

    sectors = pd.read_csv("data/sectors.csv")
    sector_symbols = sectors.loc[:, "Symbol"].to_list()

    sectors_history = load_stocks(sector_symbols, interval, start, end)
    sector_returns = get_returns(sectors_history, sectors, returns_label)
    sector_returns.to_csv(
        "pages/assets/outperformers/returns/%s/sectors-%s.csv"
        % (format_date(end), period),
        index=False,
    )

    for symbol in sector_symbols:
        print(f"making charts for: {symbol}")
        sector_history = sectors_history.loc[:, symbol]
        sector_name = sectors.loc[sectors["Symbol"] == symbol, "Name"].values[0]
        make_chart(
            df=sector_history,
            title=f"{sector_name} ({symbol}) - {period} ({chart_interval_label})",
            strategy="outperformers",
            filename=f"{format_date(end)}/sectors/{symbol}-{period}",
        )

    make_report(
        date=end,
        category="Sectors",
        report_name="sectors",
        symbols=sector_symbols,
    )
