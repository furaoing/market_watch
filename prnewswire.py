import feedparser
import time
from market_watch_logger import root_logger
from config import Config
import re
from notification import send_news_notification, EmailMsg
import requests
import traceback
import pandas as pd
from text_processing import generate_news_label
from utils import get_china_tickers
from constants import ImportantLevel, NewsSource
from news_watch_common import HistoryNewsFootprint


def is_valid_reporting_hour():
    now = pd.Timestamp.now(tz="UTC").tz_convert("Asia/Shanghai")
    hour = now.hour

    # if 15 <= hour <= 22:
    #     return True
    # else:
    #     return False
    return True


def extract_ticker(summary):
    pattern = "[\( ](?:NYSE|NASDAQ|NYSE American): ?(.+?)[\);]"
    result = re.findall(pattern, summary)
    return result


def fetch_prnewswire_feed():
    rss_url = r"https://www.prnewswire.com/rss/news-releases-list.rss"
    businesswire_merger_news_url = r"http://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeEFtRWA=="
    d = feedparser.parse(rss_url)
    businesswire_d = feedparser.parse(businesswire_merger_news_url)
    entries = d["entries"] + businesswire_d["entries"]
    records = []
    for entry in entries:
        link = entry["link"]
        title = entry["title"]
        summary = entry["summary"]
        ticker_list = extract_ticker(summary)
        if len(ticker_list) > 0:
            record = {"tickers": ticker_list, "title": title, "summary": summary, "link": link}
            records.append(record)
    return records


def hash_record(record):
    title = record["title"]
    return title


def has_common_memember(list_1, list_2):
    for x in list_1:
        if x in list_2:
            return True


if __name__ == "__main__":
    china_tickers = get_china_tickers()
    history_news = HistoryNewsFootprint()
    has_new_data = False

    messager = EmailMsg()
    while True:
        if is_valid_reporting_hour():
            records = fetch_prnewswire_feed()
            for record in records:
                if not history_news.exist(record):
                    one_record_tickers = record["tickers"]
                    one_record_title = record["title"]
                    one_record_link = record["link"]
                    labels = generate_news_label(record)

                    has_label = len(labels) > 0
                    final_flag = None
                    if Config.OnlySelectedNews:
                        final_flag = has_label
                    else:
                        final_flag = True
                    if final_flag:
                        msg = "Label: %s\nTickers: %s\nTitle: %s\nLink: %s" % (
                            str(labels),
                            " ".join(one_record_tickers),
                            one_record_title,
                            one_record_link)
                        root_logger.info(msg)
                        messager.add(msg)
                        history_news.add(record)
                        has_new_data = True

            if has_new_data:
                root_logger.info("---------------------------------------------------------------------------------------------")
                email_msg = messager.msg()
                if messager.level:
                    subject_body = ImportantLevel.IMPORTANT
                else:
                    subject_body = "Market News"
                try:
                    send_news_notification(NewsSource.PRNewswire, email_msg, subject_body)
                except requests.RequestException:
                    msg = traceback.format_exc()
                    root_logger.error("Msg Sent Failed: %s" % email_msg)
                    root_logger.error(msg)
                    time.sleep(Config.EmailReTryWaitTime)
                    root_logger.error("Retry")
                    try:
                        send_news_notification(NewsSource.PRNewswire, email_msg, subject_body)
                    except requests.RequestException:
                        msg = traceback.format_exc()
                        root_logger.error("Retry Failed")
                        root_logger.error(msg)
                messager.clear()
            has_new_data = False
            time.sleep(Config.RSSTimeInterval)
        time.sleep(0.5)