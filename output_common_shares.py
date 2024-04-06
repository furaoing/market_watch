from utils import ticker_lookup
from constants import TickerType
import os
from utils import stock_type_filter, get_raw_tickers


if __name__ == "__main__":
    raw_tickers = get_raw_tickers()
    lookup_table = ticker_lookup()

    pharma = []
    non_pharma_china = []
    for ticker in raw_tickers:
        name = lookup_table[ticker]
        if stock_type_filter(name, TickerType.Pharma):
            pharma.append(ticker)
        if stock_type_filter(name, TickerType.NonPharmaChinaGeneral):
            non_pharma_china.append(ticker)

    dest_dir_path = "data"

    gp = os.path.join(dest_dir_path, "common_share_tickers.csv")
    with open(gp, "w", newline="\n") as f:
        s = "tickers\n%s" % "\n".join(non_pharma_china)
        f.write(s)

    gp = os.path.join(dest_dir_path, "pharma_tickers.csv")
    with open(gp, "w", newline="\n") as f:
        s = "tickers\n%s" % "\n".join(pharma)
        f.write(s)

