# -*- coding: utf-8 -*-

import xlrd
from config import APIConfig
from network import Fetcher
from constants import DataRequestType
from data_model import DataRequest
from common import EndPoint
import market_watch_logger
import sys

sys.path.append("../")

if __name__ == "__main__":
    fp = r""
    book = xlrd.open_workbook(fp)
    sh = book.sheet_by_index(0)

    symbols = []
    for rx in range(1, sh.nrows):
        row = sh.row_values(rx)
        symbol = row[0]
        symbols.append(symbol)

    data_requests = []
    fetcher = Fetcher()
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)
    field = "dividendYield"
    for ticker in symbols:
        url = end_point.Stat(ticker, field)
        data_request = DataRequest(ticker, url, DataRequestType.Stat)
        data_requests.append(data_request)
    fetcher.add_data_requests(data_requests)
    request_response_list = fetcher.fetch()

    pe_data = [{"symbol": symbol, "pe": None} for symbol in symbols]
    pe_dict = {}
    for request_response in request_response_list:
        obj = request_response.result_obj
        symbol = request_response.symbol
        pe_dict[symbol] = obj

    for i in range(len(pe_data)):
        symbol = pe_data[i].get("symbol")
        pe_value = pe_dict.get(symbol)
        if pe_value:
            pe_data[i]["pe"] = pe_value
        else:
            pe_data[i]["pe"] = "na"

    for one_data in pe_data:
        print(one_data.get("pe"))