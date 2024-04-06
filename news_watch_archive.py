import feedparser
import time
from config import Config
from text_processing import generate_news_label, generate_pharma_news_label
from notification import send_news_notification, EmailMsg, send_news_notification_general
import traceback
import requests
from market_watch_logger import root_logger
import pandas as pd
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


def extract_tickers(tags):
    tickers = []
    for tag in tags:
        term = tag["term"]
        result = term.split(":")
        if len(result) == 2:
            exchange = result[0]
            ticker = result[1]
            if exchange.upper() in ["NYSE", "NASDAQ", "AMEX", "NYSE American"]:
                tickers.append(ticker)
    return tickers


def fetch_globalnewswire_feed():
    rss_url = r"https://www.globenewswire.com/RssFeed/orgclass/1/feedTitle/GlobeNewswire%20-%20News%20about%20Public%20Companies"
    d = feedparser.parse(rss_url)
    print(d)
    entries = d['entries']

    records = []
    for entry in entries:
        link = entry["link"]
        title = entry["title"]
        summary = entry["summary"]
        tags = entry["tags"]
        tickers = extract_tickers(tags)
        if len(tickers) > 0:
            record = {"tickers": tickers, "title": title, "summary": summary, "link": link}
            records.append(record)
    return records


def fetch_globalnewswire_merger_feed():
    rss_url = r"https://www.globenewswire.com/RssFeed/subjectcode/27-Mergers%20And%20Acquisitions/feedTitle/GlobeNewswire%20-%20Mergers%20And%20Acquisitions"
    d = feedparser.parse(rss_url)
    entries = d['entries']

    records = []
    for entry in entries:
        link = entry["link"]
        title = entry["title"]
        summary = entry["summary"]
        tags = entry["tags"]
        tickers = extract_tickers(tags)
        if len(tickers) > 0:
            record = {"tickers": tickers, "title": title, "summary": summary, "link": link}
            records.append(record)
    return records


def has_common_memember(list_1, list_2):
    for x in list_1:
        if x in list_2:
            return True


if __name__ == "__main__":
    china_tickers = get_china_tickers()
    history_news = HistoryNewsFootprint()
    has_new_data = False

    messager = EmailMsg()
    pharma_messager = EmailMsg()
    while True:
        if is_valid_reporting_hour():
            records = fetch_globalnewswire_feed()
            now = pd.Timestamp.now(tz="UTC").tz_convert("Asia/Shanghai")
            print("fetch %s" % now)
            for record in records:
                if not history_news.exist(record):
                    one_record_tickers = record["tickers"]
                    one_record_title = record["title"]
                    one_record_link = record["link"]
                    labels = generate_news_label(record)
                    if has_common_memember(one_record_tickers, china_tickers):
                        msg = "Label: %s\nTickers: %s\nTitle: %s\nLink: %s" % (
                            "CNTicker" + " " + " ".join(labels),
                            "#".join(one_record_tickers),
                            one_record_title,
                            one_record_link)
                        root_logger.info(msg)
                        messager.add(msg)
                        history_news.add(record)
                        has_new_data = True
                        messager.set_importance_level(ImportantLevel.IMPORTANT)
                    else:
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
                        pharma_messager.add(msg)
                        history_news.add(record)

            if has_new_data:
                root_logger.info("---------------------------------------------------------------------------------------------")
                email_msg = messager.msg()
                if messager.level:
                    subject_body = ImportantLevel.IMPORTANT
                else:
                    subject_body = "Market News"
                try:
                    send_news_notification(NewsSource.GlobalNewswire, email_msg, subject_body)
                except requests.RequestException:
                    msg = traceback.format_exc()
                    root_logger.error("Msg Sent Failed: %s" % email_msg)
                    root_logger.error(msg)
                    time.sleep(Config.EmailReTryWaitTime)
                    root_logger.error("Retry")
                    try:
                        send_news_notification(NewsSource.GlobalNewswire, email_msg, subject_body)
                    except requests.RequestException:
                        msg = traceback.format_exc()
                        root_logger.error("Retry Failed")
                        root_logger.error(msg)
                messager.clear()
            has_new_data = False

            records = fetch_globalnewswire_merger_feed()
            for record in records:
                if not history_news.exist(record):
                    one_record_tickers = record["tickers"]
                    one_record_title = record["title"]
                    one_record_link = record["link"]
                    labels = ["M&A"]
                    if has_common_memember(one_record_tickers, china_tickers):
                        msg = "Label: %s\nTickers: %s\nTitle: %s\nLink: %s" % (
                            "CNTicker" + " " + " ".join(labels),
                            "#".join(one_record_tickers),
                            one_record_title,
                            one_record_link)
                        root_logger.info(msg)
                        messager.add(msg)
                        history_news.add(record)
                        has_new_data = True
                        messager.set_importance_level(ImportantLevel.IMPORTANT)
                    else:
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
                    send_news_notification(NewsSource.GlobalNewswire, email_msg, subject_body)
                except requests.RequestException:
                    msg = traceback.format_exc()
                    root_logger.error("Msg Sent Failed: %s" % email_msg)
                    root_logger.error(msg)
                    time.sleep(Config.EmailReTryWaitTime)
                    root_logger.error("Retry")
                    try:
                        send_news_notification(NewsSource.GlobalNewswire, email_msg, subject_body)
                    except requests.RequestException:
                        msg = traceback.format_exc()
                        root_logger.error("Retry Failed")
                        root_logger.error(msg)
                messager.clear()
            has_new_data = False

            time.sleep(Config.RSSTimeInterval)
        time.sleep(0.5)
