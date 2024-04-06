# -*- coding: utf-8 -*-
import requests
import json
import time
from config import Config
from notification import send_news_notification, EmailMsg
import traceback
from market_watch_logger import root_logger
import random
import re
from common import HistoryNewsFootprint
from datetime import datetime
from constants import TimeConversion


def extract_time(author_text):
    pattern = "\t\t\t\t(.+?)\n"
    result = re.findall(pattern, author_text, re.M)
    if len(result) > 0:
        tmp = result[0]
        tmp = tmp.replace("\t", "")
        tmp = tmp.replace("\r", "")
        tmp = tmp.replace("\n", "")
        return tmp
    else:
        return None


def extract_year_month_date(text):
    pattern = "(201[0-9])年(.*?)月(.*?)日"
    result = re.findall(pattern, text)
    if len(result) > 0:
        try:
            year = result[0][0]
            month = result[0][1]
            date = result[0][2]
            return [int(year), int(month), int(date)]
        except IndexError:
            msg = "Regex Error: %s" % text
            root_logger.error(msg)
            return None
    else:
        return None


def fetch_news(kw):
    url = "http://127.0.0.1:52500/se_scraper"
    data = {"kw": kw}
    news_list = []
    r = requests.post(url, json=data)
    r.encoding = "utf8"
    res = r.text
    try:
        obj = json.loads(res)
        for k, v in obj["results"].items():
            for sub_k, sub_v in v.items():
                results = sub_v["results"]
                for result in results:
                    title = result["title"]
                    link = result["link"]
                    author = result["author"]
                    time = extract_time(author)
                    one_news = {"title": title, "link": link, "time": time}
                    news_list.append(one_news)
    except:
        root_logger.error("se_scraper response: %s" % res)
        root_logger.error(traceback.format_exc())
    return news_list


def get_random_interval():
    random_int = random.randint(1, 5)
    random_float = random.random()
    return random_int + random_float


def fetch_baidu_news(kws):
    records = []
    for kw in kws:
        record = fetch_news(kw)
        for one_record in record:
            records.append(one_record)
        time.sleep(get_random_interval())
    return records


class NewsValidator(object):
    def __init__(self):
        self.stop_words = set()
        with open(Config.NewsStopWords, "r", encoding="utf8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                self.stop_words.add(line)

    def if_valid_news(self, record):
        title, time_text = record["title"], record["time"]
        stop_words_flag = True
        for stop_word in self.stop_words:
            if stop_word in title:
                stop_words_flag = False

        outdate_flag = True
        year_month_date_result = extract_year_month_date(time_text)
        if year_month_date_result:
            year, month, date = year_month_date_result
            news_datetime = datetime(year, month, date)
            news_timestamp = news_datetime.timestamp()
            current_timestamp = time.time()
            if current_timestamp - news_timestamp > 2*TimeConversion.DAY:
                outdate_flag = False

        return stop_words_flag and outdate_flag


def remove_whitespace(tmp):
    tmp = tmp.replace("\t", "")
    tmp = tmp.replace("\r", "")
    tmp = tmp.replace("\n", "")
    tmp = tmp.replace(" ", "")
    return tmp


if __name__ == "__main__":
    fp = "data/cn_names"
    with open(fp, "r", encoding="utf8") as f:
        lines = f.readlines()
        kws = [line.strip() for line in lines]

    news_validator = NewsValidator()
    history_news = HistoryNewsFootprint()
    has_new_data = False
    source = "BaiduNews"

    messager = EmailMsg()
    while True:
        records = fetch_baidu_news(kws)
        for record in records:
            if not history_news.exist(record) and news_validator.if_valid_news(record):
                msg = "Title: %s\nTime: %s\nLink: %s" % (remove_whitespace(record["title"]),
                                                         record["time"], record["link"])
                root_logger.info(msg)
                messager.add(msg)
                history_news.add(record)
                has_new_data = True

        if has_new_data:
            root_logger.info("---------------------------------------------------------------------------------------------")
            email_msg = messager.msg()
            try:
                send_news_notification(source, email_msg)
            except requests.RequestException:
                msg = traceback.format_exc()
                root_logger.error("Msg Sent Failed: %s" % email_msg)
                root_logger.error(msg)
                time.sleep(Config.EmailReTryWaitTime)
                root_logger.error("Retry")
                try:
                    send_news_notification(source, email_msg)
                except requests.RequestException:
                    msg = traceback.format_exc()
                    root_logger.error("Retry Failed")
                    root_logger.error(msg)
            messager.clear()
        has_new_data = False
        time.sleep(get_random_interval()*1500)
