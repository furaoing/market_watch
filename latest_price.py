from common import EndPoint
from utils import get_tickers
from network import Fetcher
from config import APIConfig, Config
from data_model import DataRequest
from constants import DataRequestType
import traceback
import logging
import sys


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


def check_batch_stocks(tickers, n_worker=10):
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
    records = []

    data_requests = []
    fetcher = Fetcher(n_worker)
    for ticker in tickers:
        url = end_point.Price(symbol=ticker)
        data_request = DataRequest(ticker, url, DataRequestType.HistoryPrice)
        data_requests.append(data_request)
    fetcher.add_data_requests(data_requests)
    request_response_list = fetcher.fetch()

    for request_response in request_response_list:
        response_obj = request_response.result_obj
        ticker = request_response.symbol
        records.append({"ticker": ticker, "price": response_obj})
    return records


def get_all_latest_price(n_worker=5):
    all_tickers = get_tickers()
    try:
        records = check_batch_stocks(all_tickers, n_worker)
        return records

    except Exception:
        root_logger.error(traceback.format_exc())


if __name__ == "__main__":
    records = get_all_latest_price(Config.MaxWorker)
    print(records)