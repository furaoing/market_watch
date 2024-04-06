import json
import logging
from constants import Signal
from config import APIConfig, Config
import time
from utils import get_tickers, ticker_lookup
from exceptions import UnknownSymbol, TooManyRequest
from network import Fetcher
import sys
import pandas as pd
from trading_calendars import get_calendar
import traceback
from constants import DataRequestType
from data_model import DataRequest
from common import EndPoint
from collections import defaultdict
from database import MySQLUpdater
from database import fetch_history_price
from notification import send_notification
from common import filter_records_by_life_cycle, generate_short_records_msg
from signals import RS_T0_Check, RS_T1_Pre_Check, RS_T1_Check, RS_T2_Check, RS_T3_Check

error_handler = logging.StreamHandler(sys.stderr)
error_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s/%(name)s, %(message)s"))
error_handler.setLevel(logging.ERROR)

info_handler = logging.StreamHandler(sys.stdout)
info_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s/%(name)s, %(message)s"))
info_handler.setLevel(logging.INFO)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(error_handler)
root_logger.addHandler(info_handler)


def check_data_completeness(data):
    us_calendar = get_calendar('XNYS')
    now = pd.Timestamp.now(tz="UTC")
    last_close = us_calendar.previous_close(now)
    last_close_day = last_close.tz_convert("America/New_York").day

    latest_day_data = data[-1]
    date = latest_day_data["date"]
    latest_data_ts = pd.Timestamp(date, tz="America/New_York")
    latest_data_day = latest_data_ts.day

    if last_close_day == latest_data_day:
        return True
    else:
        return False


def check_one_stock_helper(response_obj):
    try:
        signals = []
        data = response_obj
        if len(data) < 1:
            msg = "Response Contains No Data"
            root_logger.warning(msg)
            return signals
        # if not check_data_completeness(data):
        #     msg = "Data Incomplete: %s" % (json.dumps(data, ensure_ascii=False))
        #     root_logger.warning(msg)
        #     return signals
        close_price_list = [x["close"] for x in data]
        # latest close price less than 5 dollars
        if close_price_list[-1] < Config.MinimumPrice:
            return signals
        n_data_point = len(close_price_list)
        if n_data_point < 2:
            return signals
        elif 3 <= n_data_point < 5:
            three_days_price = close_price_list[-3:]
            RS_T1_Pre_Check_result = RS_T1_Pre_Check(three_days_price)
            RS_T1_Check_result = RS_T1_Check(three_days_price)
            if RS_T1_Check_result:
                signals.append(Signal.RS_T1)
            if RS_T1_Pre_Check_result:
                signals.append(Signal.RS_T1_Pre_Check)
            return signals
        elif n_data_point >= 5:
            three_days_price = close_price_list[-3:]
            five_days_price = close_price_list[-5:]

            RS_T1_Check_result = RS_T1_Check(three_days_price)
            RS_T2_Check_result = RS_T2_Check(five_days_price)

            if RS_T1_Check_result:
                signals.append(Signal.RS_T1)
            if RS_T2_Check_result:
                signals.append(Signal.RS_T2)
            return signals
        return signals
    except Exception:
        msg = "Response is: %s" % json.dumps(response_obj)
        root_logger.error(msg)
        raise Exception("Function: check_one_stock_helper, Exception !")


class BatchStockChecker(object):
    def __init__(self, end_point_url, field):
        self.end_point_url = end_point_url
        self.field = field

    def check_batch_stocks(self, tickers):
        mysql = MySQLUpdater()
        n_last_days = 30
        ticker_dict = ticker_lookup()
        records = []

        data_requests = []
        fetcher = Fetcher()
        for ticker in tickers:
            url = self.end_point_url(ticker)
            data_request = DataRequest(ticker, url, DataRequestType.Quote)
            data_requests.append(data_request)
        fetcher.add_data_requests(data_requests)
        request_response_list = fetcher.fetch()
        for request_response in request_response_list:
            response_obj = request_response.result_obj
            if self.field not in response_obj.keys():
                root_logger.error("Json Field Missing: %s" % request_response.symbol)
                continue
            if response_obj[self.field] is None:
                continue
            last_close_price = response_obj[self.field]
            ticker = request_response.symbol
            history_prices = fetch_history_price(ticker, n_last_days, mysql)
            logging.info("Fetched History Price of %s" % ticker)
            new_response_obj = [{"close": x.ClosePrice} for x in history_prices]
            new_response_obj.append({"close": last_close_price})
            try:
                logging.info("Checking Signal of %s" % ticker)
                signals = check_one_stock_helper(new_response_obj)
                if len(signals) > 0:
                    record = {"ticker": ticker, "name": ticker_dict[ticker], "signals": signals,
                              "time": "Beijing Time: %s" % str(time.asctime())}
                    records.append(record)
            except UnknownSymbol:
                msg = "Unknown Symbol: %s" % str(ticker)
                root_logger.warning(msg)
        mysql.clean_up()
        return records


class BatchVolumeChecker(object):
    def __init__(self, end_point_url):
        self.end_point_url = end_point_url

    def check_batch_stocks(self, tickers):
        mysql = MySQLUpdater()
        n_last_days = 5
        ticker_dict = ticker_lookup()
        records = []

        data_requests = []
        fetcher = Fetcher()
        for ticker in tickers:
            url = self.end_point_url(ticker)
            data_request = DataRequest(ticker, url, DataRequestType.Quote)
            data_requests.append(data_request)
        fetcher.add_data_requests(data_requests)
        request_response_list = fetcher.fetch()
        for request_response in request_response_list:
            response_obj = request_response.result_obj
            if "latestVolume" not in response_obj.keys() or "avgTotalVolume" not in response_obj.keys() or \
                    "latestPrice" not in response_obj.keys():
                root_logger.error("Json Field Missing: %s" % request_response.symbol)
                continue
            if response_obj["latestVolume"] is None or response_obj["avgTotalVolume"] is None or \
                    response_obj["latestPrice"] is None:
                continue
            ticker = request_response.symbol
            history_prices = fetch_history_price(ticker, n_last_days, mysql)
            avg_price = sum([x.ClosePrice for x in history_prices])/len(history_prices)
            try:
                logging.info("Checking Signal of %s" % ticker)
                signals = []
                if response_obj["latestVolume"] > 3*response_obj["avgTotalVolume"] and response_obj["latestPrice"] > 1.2*avg_price:
                    signals.append(Signal.VOLUME_T0)
                if len(signals) > 0:
                    record = {"ticker": ticker, "name": ticker_dict[ticker], "signals": signals,
                              "time": "Beijing Time: %s" % str(time.asctime())}
                    records.append(record)
            except UnknownSymbol:
                msg = "Unknown Symbol: %s" % str(ticker)
                root_logger.warning(msg)
        mysql.clean_up()
        return records


def group_signals(records):
    new_records = defaultdict(list)
    for record in records:
        signals = record["signals"]
        for signal in signals:
            new_records[signal].append(record)
    return new_records


def check_all_stocks(gp):
    all_tickers = get_tickers()
    f = open(gp, "a", encoding="utf8", newline="\n")

    f.write("Beijing Time: %s, Record Start \n" % str(time.asctime()))
    try:
        end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
        batch_stock_checker = BatchStockChecker(end_point_url=end_point.Quote, field="latestPrice")
        records = batch_stock_checker.check_batch_stocks(all_tickers)
        if len(records) > 0:
            msg = generate_short_records_msg(records)
            send_notification(msg)
        records_dict = group_signals(records)
        for key, record_list in records_dict.items():
            f.write(json.dumps(key, ensure_ascii=False) + "\n")
            for record in record_list:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.write("\n")
    except TooManyRequest:
        f.write("TooManyRequest" + "\n")
    except Exception:
        root_logger.error(traceback.format_exc())
    f.write("Beijing Time: %s, Record End \n" % str(time.asctime()))
    f.write("\n")
    f.close()


def check_all_intraday_stocks(gp, life_limited_list):
    all_tickers = get_tickers()
    f = open(gp, "a", encoding="utf8", newline="\n")

    f.write("Beijing Time: %s, Record Start \n" % str(time.asctime()))
    try:
        end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
        batch_stock_checker = BatchStockChecker(end_point_url=end_point.Quote, field="latestPrice")
        records = batch_stock_checker.check_batch_stocks(all_tickers)
        new_records = filter_records_by_life_cycle(records, life_limited_list)
        if len(new_records) > 0:
            msg = generate_short_records_msg(new_records)
            send_notification(msg)
        records_dict = group_signals(records)
        for key, record_list in records_dict.items():
            f.write(json.dumps(key, ensure_ascii=False) + "\n")
            for record in record_list:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.write("\n")
    except TooManyRequest:
        f.write("TooManyRequest" + "\n")
    except Exception:
        root_logger.error(traceback.format_exc())
    f.write("Beijing Time: %s, Record End \n" % str(time.asctime()))
    f.write("\n")
    f.close()


def check_all_pre_market_stocks(gp, life_limited_list):
    all_tickers = get_tickers()
    f = open(gp, "a", encoding="utf8", newline="\n")

    f.write("Beijing Time: %s, Record Start \n" % str(time.asctime()))
    try:
        end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
        batch_stock_checker = BatchStockChecker(end_point_url=end_point.Quote, field="extendedPrice")
        records = batch_stock_checker.check_batch_stocks(all_tickers)
        new_records = filter_records_by_life_cycle(records, life_limited_list)
        if len(new_records) > 0:
            msg = generate_short_records_msg(new_records)
            send_notification(msg)
        records_dict = group_signals(records)
        for key, record_list in records_dict.items():
            f.write(json.dumps(key, ensure_ascii=False) + "\n")
            for record in record_list:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.write("\n")
    except TooManyRequest:
        f.write("TooManyRequest" + "\n")
    except Exception:
        root_logger.error(traceback.format_exc())
    f.write("Beijing Time: %s, Record End \n" % str(time.asctime()))
    f.write("\n")
    f.close()


def check_all_market_volume(gp, life_limited_list):
    all_tickers = get_tickers()
    f = open(gp, "a", encoding="utf8", newline="\n")

    f.write("Beijing Time: %s, Record Start \n" % str(time.asctime()))
    try:
        end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
        batch_stock_checker = BatchVolumeChecker(end_point_url=end_point.Quote)
        records = batch_stock_checker.check_batch_stocks(all_tickers)
        new_records = filter_records_by_life_cycle(records, life_limited_list)
        if len(new_records) > 0:
            msg = generate_short_records_msg(new_records)
            send_notification(msg)
        records_dict = group_signals(records)
        for key, record_list in records_dict.items():
            f.write(json.dumps(key, ensure_ascii=False) + "\n")
            for record in record_list:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.write("\n")
    except TooManyRequest:
        f.write("TooManyRequest" + "\n")
    except Exception:
        root_logger.error(traceback.format_exc())
    f.write("Beijing Time: %s, Record End \n" % str(time.asctime()))
    f.write("\n")
    f.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        gp = sys.argv[1]
    else:
        gp = r"stock_signal_list.txt"
    check_all_stocks(gp)
