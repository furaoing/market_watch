import pprint
import sys
import requests
import json

sys.path.append('../')
from common import EndPoint
from config import APIConfig


if __name__ == "__main__":
    ticker = sys.argv[1]
    end_point = EndPoint(APIConfig.baseURL, APIConfig.version, APIConfig.secret_token)

    url = end_point.Quote(ticker)
    r = requests.get(url)
    result = json.loads(r.text)
    pprint.pprint(result)
