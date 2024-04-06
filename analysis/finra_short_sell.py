import requests
import csv
import datetime
import json
import logging


def get_data_file(url, session):
    r = session.get(url)
    if r.status_code == 200:
        r.encoding = "utf8"
        return r.text
    else:
        return None


def generate_url(exchange_code, date_str):
    base_url = "http://regsho.finra.org/%s%s.txt" % (exchange_code, date_str)
    return base_url


def make_time_str(struct_time):
    year = struct_time.year
    month = struct_time.month
    day = struct_time.day
    if month < 10:
        month_str = "0" + str(month)
    else:
        month_str = str(month)
    if day < 10:
        day_str = "0" + str(day)
    else:
        day_str = str(day)
    return str(year) + month_str + day_str


def construct_time_str(year, month, day):
    if month < 10:
        month_str = "0" + str(month)
    else:
        month_str = str(month)
    if day < 10:
        day_str = "0" + str(day)
    else:
        day_str = str(day)
    return str(year) + month_str + day_str


def read_csv(txt):
    data = []
    # one = {"symbol": None, "short_volume": None, "total_volume": None}
    lines = txt.split()[:-1]
    spamreader = csv.reader(lines, delimiter='|', quotechar='"')
    next(spamreader)
    for row in spamreader:
        date = row[0]
        symbol = row[1]
        short_volume = int(row[2])
        totoal_volume = int(row[4])
        data.append({"date": date, "symbol": symbol, "short_volume": short_volume, "total_volume": totoal_volume})
    return data


class ShortCounter(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.short_volume = 0
        self.total_volume = 0
        self.data = []

    def is_symbol(self, symbol):
        return symbol == self.symbol

    def add_short_volume(self, short_volume):
        self.short_volume += short_volume

    def add_total_volume(self, total_volume):
        self.total_volume += total_volume

    def add_record(self, one_record):
        self.data.append(one_record)


def get_one_day_data(ticker, time_str):
    exchange_code = "CNMSshvol"
    session = requests.Session()
    url = generate_url(exchange_code, time_str)
    txt = get_data_file(url, session)
    logging.info("URL: %s Finished" % url)
    if txt:
        data = read_csv(txt)
        for record in data:
            if record["symbol"].lower() == ticker.lower():
                short_volume = record["short_volume"]
                total_volume = record["total_volume"]
                volumes = [short_volume, total_volume]
                return volumes


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    BYND = ShortCounter("AAPL")
    # These All the Exchange Specific Data
    # exchange_code_list = ["FNRAshvol", "FNQCshvol", "FNSQshvol", "FNYXshvol", "FORFshvol"]
    exchange_code_list = ["CNMSshvol"]
    start = datetime.datetime(2019, 9, 24)
    one_day = datetime.timedelta(hours=24)
    session = requests.Session()
    for _ in range(1):
        start = start + one_day
        time_str = make_time_str(start)
        for code in exchange_code_list:
            url = generate_url(code, time_str)
            txt = get_data_file(url, session)
            logging.info("URL: %s Finished" % url)
            if txt:
                data = read_csv(txt)
                for record in data:
                    if BYND.is_symbol(record["symbol"]):
                        BYND.add_record(record)
                        BYND.add_short_volume(record["short_volume"])
                        BYND.add_total_volume(record["total_volume"])

    dump_str = json.dumps(BYND.data)
    with open("bynd_short_record.json", "w") as f:
        f.write(dump_str)

    print(BYND.total_volume)
    print(BYND.short_volume)






