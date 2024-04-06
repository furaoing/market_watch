import feedparser
import requests
from market_watch_logger import root_logger
import traceback
import time
from config import Config
from notification import send_news_notification


class HistoryNewsFootprint(object):
    def __init__(self):
        self.hash_container = set()

    def exist(self, record):
        link = record["link"]
        title = record["title"]
        return link in self.hash_container or title in self.hash_container

    def add(self, record):
        link = record["link"]
        title = record["title"]
        self.hash_container.add(link)
        self.hash_container.add(title)


def my_rss_parse(url):
    try:
        feed_content = requests.get(url)
        feed = feedparser.parse(feed_content.text)
        return feed
    except requests.RequestException:
        msg = traceback.format_exc()
        root_logger.error("Requests Error")
        root_logger.error(msg)
        send_news_notification("market_watch", msg, "Exception Occurred")
        time.sleep(Config.ConnectionErrorInterval)
        return None
    except:
        msg = traceback.format_exc()
        root_logger.error("Feed Parser Error")
        root_logger.error(msg)
        return None

