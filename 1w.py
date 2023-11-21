from datetime import *
from dateutil.relativedelta import *
import pandas as pd
from lib.utils import *

# Dates
today = datetime.now()
last_friday = today + relativedelta(weekday=FR(-1))
last_year = last_friday + relativedelta(weeks=-52)

###########
# Indices #
###########
indices = pd.read_csv("data/indices.csv")
index_symbols = indices.loc[:, "Symbol"].to_list()

index_history = load_stocks(index_symbols, "1wk", last_year, last_friday)
index_returns = get_returns(index_history, indices, "52 Week ∆")
index_returns.to_csv(
    "pages/assets/returns/%s/indices-1y.csv" % format_date(last_friday),
    index=False,
)

###########
# Sectors #
###########
sectors = pd.read_csv("data/sectors.csv")
sector_symbols = sectors.loc[:, "Symbol"].to_list()

sector_history = load_stocks(sector_symbols, "1wk", last_year, last_friday)
sector_returns = get_returns(sector_history, sectors, "52 Week ∆")
sector_returns.to_csv(
    "pages/assets/returns/%s/sectors-1y.csv" % format_date(last_friday),
    index=False,
)

spx_return = index_returns.loc[
    index_returns["Symbol"] == "SPY", "52 Week ∆"
].values[0]

outperforming_sectors = sector_returns[sector_returns["52 Week ∆"] > spx_return]
outperforming_sector_names = outperforming_sectors.loc[:, "Name"].to_list()

##############
# Securities #
##############
sp500_constituents = pd.read_csv("data/sp500-constituents.csv")

for name in outperforming_sector_names:
    constituents = sp500_constituents.loc[
        sp500_constituents["GICS Sector"] == name
    ]
    constituent_symbols = constituents.loc[:, "Symbol"].to_list()

    print("load stocks for sector: %s" % name)
    constituent_history = load_stocks(
        constituent_symbols, "1wk", last_year, last_friday
    )

    constituent_returns = get_returns(
        constituent_history, constituents, "52 Week ∆"
    )

    sector_return = sector_returns.loc[
        sector_returns["Name"] == name, "52 Week ∆"
    ].values[0]

    outperforming_stocks = constituent_returns[
        constituent_returns["52 Week ∆"] > sector_return
    ]
    outperforming_stocks.to_csv(
        "pages/assets/returns/%s/%s-1y.csv"
        % (format_date(last_friday), name.lower().replace(" ", "-")),
        index=False,
    )
    outperforming_stock_symbols = outperforming_stocks.loc[
        :, "Symbol"
    ].to_list()

    for symbol in outperforming_stock_symbols:
        stock_history = constituent_history.loc[:, symbol]
        make_chart(
            df=stock_history,
            title="%s - Weekly" % symbol,
            filename="%s/%s-weekly" % (format_date(last_friday), symbol),
        )
