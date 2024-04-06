import sys
sys.path.append('../')

from config import APIConfig
from constants import DataRequestType
from data_model import DataRequest
from common import EndPoint
from network import Fetcher
from utils import get_china_tickers


def get_earnings_date():
    data_requests = []
    tickers = get_china_tickers()
    fetcher = Fetcher()
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
    for ticker in tickers:
        url = end_point.Earnings(ticker)
        data_request = DataRequest(ticker, url, DataRequestType.EarningRelease)
        data_requests.append(data_request)
    fetcher.add_data_requests(data_requests)
    request_response_list = fetcher.fetch()

    for response in request_response_list:
        result_obj = response.result_obj
        if len(result_obj) > 0:
            print(result_obj)


if __name__ == "__main__":
    get_earnings_date()

