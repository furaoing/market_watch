from utils import get_tickers, ticker_lookup
from collections import Counter

tickers = get_tickers()
lookup_table = ticker_lookup()

names = set()

for ticker in tickers:
    name = lookup_table[ticker]
    names.add(name)

c = Counter()
sep = " - "
for name in names:
    result = name.split(sep)
    if len(result) > 1:
        c.update([result[1]])

for x in c.most_common():
    print(x)


# Common Stock
# Ordinary Shares

