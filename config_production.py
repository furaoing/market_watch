from constants import MillisecondsPerSecond
from constants import TimeConversion


class Config(object):
    RequestIntervalMilliseconds = 20

    # Represented as seconds
    RequestInterval = RequestIntervalMilliseconds/MillisecondsPerSecond
    MaxWorker = 20
    TimeOut = 2
    SignalLifeTime = 12*TimeConversion.HOUR
    TickerFileOutDateTime = 12*TimeConversion.HOUR
    MinimumPrice = 5
    MarketCheckInterval = 10*60
    PremarketCheckInterval = 60*60

    EmailTimeOut = 3
    EmailReTryWaitTime = 60*2
    MailGunBaseURL = ""
    MailGunAPIKey = ""
    MailGunSenderAddr = ""
    MailSenderName = ""

    OnlySelectedNews = True
    RSSTimeInterval = 5
    NewsStopWords = "data/news_stop_words.txt"

    FIXER_KEY = ""


class DBConfig(object):
    DB_HOST = ""
    DB_USER = "us_security"
    DB_PASSWORD = "us_security"
    DB_DATABASE = "us_security"
    DB_TYPE = "mysql"
    DB_CONNECTOR = "pymysql"
    DB_CHARSET = "utf8"


class APIConfig(object):
    secret_token = ""
    baseURL = r"https://cloud.iexapis.com"
    version = r"v1"


class IBConfig(object):
    short_data_file_names = ["usa.txt", "hongkong.txt"]