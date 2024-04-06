from requests_futures.sessions import FuturesSession
import requests
from exceptions import TooManyRequest, HttpStatusCodeOtherThan200, UnknownSymbol, InValidJson
from data_model import RequestResponse
from constants import ValidationResultType
import json
import logging
from config import Config
import time
import traceback
import concurrent

root_logger = logging.getLogger()


class Fetcher(object):
    def __init__(self):
        self.session = FuturesSession(max_workers=Config.MaxWorker)
        self.data_requests = None

    def add_data_requests(self, data_requests):
        self.data_requests = data_requests

    def validate_response(self, response_one, data_request):
        response_one.encoding = "utf8"
        content = response_one.text
        msg_compiled = "Status Code: %s\t\tContent: %s" % (str(response_one.status_code), content)
        if response_one.status_code == 200:
            try:
                symbol = data_request.symbol
                request_type = data_request.data_request_type
                result_obj = json.loads(content)
                request_response = RequestResponse(symbol, result_obj, request_type, ValidationResultType.Normal)
                root_logger.info(msg_compiled)
                return request_response
            except:
                root_logger.error(msg_compiled)
                root_logger.error(data_request.__str__())
                root_logger.error("InValidJson")
                raise InValidJson
        elif response_one.status_code == 429:
            root_logger.error(msg_compiled)
            root_logger.error("Too Many Request")
            raise TooManyRequest
        elif response_one.status_code == 404:
            root_logger.error(msg_compiled)
            root_logger.error(data_request.__str__())
            root_logger.error("Unknown symbol")
            raise UnknownSymbol
        else:
            root_logger.error(msg_compiled)
            root_logger.error("HttpStatusCodeOtherThan200")
            raise HttpStatusCodeOtherThan200

    def fetch(self):
        if Config.MaxWorker == 1:
            response_list = self.sequential_fetch()
        else:
            response_list = self.batch_fetch()
        return response_list

    def batch_fetch(self):
        request_response_list = []

        future_and_data_request = []
        request_made = 0
        for data_request in self.data_requests:
            try:
                future_one = self.session.get(data_request.url)
                future_and_data_request.append((future_one, data_request))
            except:
                root_logger.error(traceback.format_exc())
            request_made += 1
            time.sleep(Config.RequestInterval)

            if request_made == Config.MaxWorker:
                for future_one_tmp, data_request_tmp in future_and_data_request:
                    try:
                        response_one = future_one_tmp.result(timeout=Config.TimeOut)
                        try:
                            request_response = self.validate_response(response_one, data_request_tmp)
                            request_response_list.append(request_response)
                        except UnknownSymbol:
                            continue
                        except InValidJson:
                            continue
                    except requests.exceptions.ConnectionError:
                        msg_compiled = "Connection Error - URL: %s\t\tTicker: %s" % (
                            data_request_tmp.url, data_request_tmp.symbol)
                        root_logger.error(msg_compiled)
                    except concurrent.futures.TimeoutError:
                        msg_compiled = "Request Timeout - URL: %s\t\tTicker: %s" % (
                            data_request_tmp.url, data_request_tmp.symbol)
                        root_logger.error(msg_compiled)
                    except:
                        root_logger.error(traceback.format_exc())
                future_and_data_request = []
                request_made = 0

        if len(future_and_data_request) > 0:
            for future_one_tmp, data_request_tmp in future_and_data_request:
                try:
                    response_one = future_one_tmp.result(timeout=Config.TimeOut)
                    try:
                        request_response = self.validate_response(response_one, data_request_tmp)
                        request_response_list.append(request_response)
                    except UnknownSymbol:
                        continue
                    except InValidJson:
                        continue
                except requests.exceptions.ConnectionError:
                    msg_compiled = "Connection Error - URL: %s\t\tTicker: %s" % (
                        data_request_tmp.url, data_request_tmp.symbol)
                    root_logger.error(msg_compiled)
                except concurrent.futures.TimeoutError:
                    msg_compiled = "Request Timeout - URL: %s\t\tTicker: %s" % (
                        data_request_tmp.url, data_request_tmp.symbol)
                    root_logger.error(msg_compiled)
                except:
                    root_logger.error(traceback.format_exc())
        return request_response_list

    def sequential_fetch(self):
        request_response_list = []
        for data_request in self.data_requests:
            response_one = requests.get(data_request.url)
            request_response = self.validate_response(response_one, data_request)
            request_response_list.append(request_response)
        return request_response_list
