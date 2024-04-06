import csv
import os
from download_tickers import download_ftp_files
from constants import TickerType, TimeConversion
import time
from config import Config
import json


def is_pharma_stock(name):
    kw_list = ["pharma", "medica", "therape", "bio"]
    kw_set = set()
    for kw in kw_list:
        kw_set.add(kw.lower())
    for kw in kw_set:
        if kw in name.lower():
            return True
    return False


def is_china_stock(name):
    china_tickers = get_china_tickers()
    return name in china_tickers


def is_common_stock(name):
    kw_list = ["Common Stock", "Class A Common Stock", "Ordinary Shares",
               "American Depositary Shares", "Common Shares", "Class B Common Stock",
               "common stock", "Class A Ordinary Shares", "American Depositary Share",
               "Ordinary Share", "Series A Common Stock", "Class A Common Shares",
               "Series B Common Stock", "ADS", "ADR", "Common Share", "Class C Common Stock",
               "Class C Capital Stock", "American Depositary Receipts", "Voting Common Stock",
               "Non-Voting Common Stock", "ADRs", "common share"
               ]
    kw_set = set()
    for kw in kw_list:
        kw_set.add(kw.lower())

    is_common_stock_flag = False
    for kw in kw_set:
        if kw in name.lower():
            is_common_stock_flag = True
            break
    return is_common_stock_flag


def stock_type_filter(name, ticker_type):
    if ticker_type == TickerType.NonPharmaGeneral:
        if is_common_stock(name):
            if not is_pharma_stock(name):
                return True
        return False
    if ticker_type == TickerType.Pharma:
        if is_common_stock(name):
            if is_pharma_stock(name):
                return True
        return False
    if ticker_type == TickerType.General:
        if is_common_stock(name):
            return True
        return False
    if ticker_type == TickerType.NonPharmaChinaGeneral:
        if is_common_stock(name) and not is_pharma_stock(name) and not is_china_stock(name):
            return True
        return False
    raise Exception("Not a Valid Ticker Type")


def if_file_outdated(fp):
    modified_time = os.path.getmtime(fp)
    now = time.time()
    if now - modified_time > Config.TickerFileOutDateTime:
        return True
    else:
        return False


def get_active_trading_tickers_nasdaq():
    dest_dir_path = "data"
    f_path = os.path.join(dest_dir_path, "nasdaqlisted.txt")
    if not os.path.exists(f_path) or if_file_outdated(f_path):
        download_ftp_files(dest_dir_path)

    trading_tickers = set()
    fp = os.path.join(os.path.dirname(__file__), f_path)
    with open(fp, encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        next(spamreader)
        for span in spamreader:
            symbol = span[0]
            etf_flag = span[-2]
            test_issue_flag = span[3]

            if etf_flag == "N" and test_issue_flag == "N":
                trading_tickers.add(symbol)
    return trading_tickers


def get_active_trading_tickers_nyse():
    dest_dir_path = "data"
    f_path = os.path.join(dest_dir_path, "otherlisted.txt")
    if not os.path.exists(f_path) or if_file_outdated(f_path):
        download_ftp_files(dest_dir_path)

    trading_tickers = set()
    fp = os.path.join(os.path.dirname(__file__), f_path)
    with open(fp, encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        next(spamreader)
        for span in spamreader:
            if span[0] == span[-1]:
                symbol = span[0]
                etf_flag = span[-4]
                exchange = span[2]
                test_issue_flag = span[-2]

                if etf_flag == "N" and test_issue_flag == "N" and exchange == "N":
                    trading_tickers.add(symbol)

    return trading_tickers


def ticker_lookup():
    lookup_table = {}
    fp = os.path.join(os.path.dirname(__file__), r"data/nasdaqlisted.txt")
    with open(fp, encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        next(spamreader)
        for span in spamreader:
            symbol = span[0]
            name = span[1]
            lookup_table[symbol] = name

    fp = os.path.join(os.path.dirname(__file__), r"data/otherlisted.txt")
    with open(fp, encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        next(spamreader)
        for span in spamreader:
            if span[0] == span[-1]:
                symbol = span[0]
                name = span[1]
                lookup_table[symbol] = name
    return lookup_table


# def is_in_black_list(ticker, stock_name_lookup_table):
#     black_list = ["warrant", "warrants"]
#     for w in black_list:
#         if w in stock_name_lookup_table[ticker].lower():
#             return True
#     return False


def get_tickers():
    nyse = get_active_trading_tickers_nyse()
    nasdaq = get_active_trading_tickers_nasdaq()
    combine = nyse.union(nasdaq)

    new_combine = set()
    stock_name_lookup_table = ticker_lookup()

    for ticker in combine:
        name = stock_name_lookup_table[ticker]
        if stock_type_filter(name, TickerType.NonPharmaGeneral):
            new_combine.add(ticker)
    return new_combine


def get_raw_tickers():
    nyse = get_active_trading_tickers_nyse()
    nasdaq = get_active_trading_tickers_nasdaq()
    combine = nyse.union(nasdaq)
    return combine


def get_china_tickers():
    china_tickers = []
    fp = os.path.join(os.path.dirname(__file__), r"data/china_tickers.csv")
    with open(fp, encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        next(spamreader)
        for span in spamreader:
            ticker = span[0]
            china_tickers.append(ticker)
    return china_tickers


def get_share_outstanding():
    share_outstanding = {}
    fp = os.path.join(os.path.dirname(__file__), r"data/outstanding_shares.txt")
    with open(fp, encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader)
        for span in spamreader:
            ticker = span[0]
            oustanding_number = int(span[1])
            share_outstanding[ticker] = oustanding_number
    return share_outstanding


def load_ticker_universe():
    with open("data/ticker_universe.json", "r", encoding="utf-8") as f:
        content = f.read()
        ticker_universe = json.loads(content)
        ticker_universe = list(set(ticker_universe))
        return ticker_universe


if __name__ == "__main__":
    r = get_active_trading_tickers_nyse()
    print(r)