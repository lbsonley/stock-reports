from pathlib import Path
import pandas as pd
from lib.utils import *
from lib.makereport import *


def outperformers(start, end, interval, period):
    returns_label = ""
    chart_interval = ""

    match period:
        case "1w":
            returns_label = "1 Week ∆"
            chart_interval = "30m"
        case "1q":
            returns_label = "13 Week ∆"
            chart_interval = "Daily"
        case "1y":
            returns_label = "52 Week ∆"
            chart_interval = "Weekly"
        case "5y":
            returns_label = "5 Year ∆"
            chart_interval = "Monthly"

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
    indices_history.to_csv("history/indices-history.csv")
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
            % (index_name, symbol, period, chart_interval),
            strategy="outperformers",
            filename="%s/indices/%s-%s" % (format_date(end), symbol, period),
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
            title=f"{sector_name} ({symbol}) - {period} ({chart_interval})",
            strategy="outperformers",
            filename=f"{format_date(end)}/sectors/{symbol}-{period}",
        )

    spx_return = indices_returns.loc[
        indices_returns["Symbol"] == "SPY", returns_label
    ].values[0]

    outperforming_sectors = sector_returns[
        sector_returns[returns_label] > spx_return
    ]
    outperforming_sector_names = outperforming_sectors.loc[:, "Name"].to_list()

    make_report(
        date=end,
        category="Sectors",
        report_name="sectors",
        symbols=sector_symbols,
    )

    # ##############
    # # Securities #
    # ##############
    # sp500_constituents = pd.read_csv("data/sp500-constituents.csv")

    # for name in outperforming_sector_names:
    #     constituents = sp500_constituents.loc[
    #         sp500_constituents["GICS Sector"] == name
    #     ]
    #     constituent_symbols = constituents.loc[:, "Symbol"].to_list()

    #     print("load stocks for sector: %s" % name)
    #     constituent_history = load_stocks(
    #         constituent_symbols, interval, start, end
    #     )

    #     constituent_returns = get_returns(
    #         constituent_history, constituents, returns_label
    #     )

    #     sector_return = sector_returns.loc[
    #         sector_returns["Name"] == name, returns_label
    #     ].values[0]

    #     outperforming_stocks = constituent_returns[
    #         constituent_returns[returns_label] > sector_return
    #     ]
    #     outperforming_stocks.to_csv(
    #         "pages/assets/outperformers/returns/%s/%s-%s.csv"
    #         % (format_date(end), name.lower().replace(" ", "-"), period),
    #         index=False,
    #     )
    #     outperforming_stock_symbols = outperforming_stocks.loc[
    #         :, "Symbol"
    #     ].to_list()

    #     for symbol in outperforming_stock_symbols:
    #         stock_history = constituent_history.loc[:, symbol]
    #         stock_name = constituents.loc[
    #             constituents["Symbol"] == symbol, "Name"
    #         ].values[0]

    #         # make sure index column has proper name and type
    #         if stock_history.index.name == None:
    #             stock_history.index.name = "Datetime"

    #         if (
    #             type(stock_history.index)
    #             != "<class 'pandas.core.indexes.datetimes.DatetimeIndex'>"
    #         ):
    #             stock_history.index = pd.to_datetime(stock_history.index)

    #         make_chart(
    #             df=stock_history,
    #             title="%s (%s) - %s" % (stock_name, symbol, period),
    #             strategy="outperformers",
    #             filename="%s/%s-%s" % (format_date(end), symbol, period),
    #         )
