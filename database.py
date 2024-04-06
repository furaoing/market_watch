# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DBConfig
from data_model import Base
from data_model import StockHistoryPrice


class MySQLUpdater(object):
        def __init__(self):
            self.counter = 0
            self.con_str = "%s+%s://%s:%s@%s/%s?charset=%s" % \
                                     (
                                         DBConfig.DB_TYPE,
                                         DBConfig.DB_CONNECTOR,
                                         DBConfig.DB_USER,
                                         DBConfig.DB_PASSWORD,
                                         DBConfig.DB_HOST,
                                         DBConfig.DB_DATABASE,
                                         DBConfig.DB_CHARSET
                                     )
            print(self.con_str)

            # 创建连接引擎
            engine = create_engine(self.con_str)

            # 创建连接Session类
            DBSession = sessionmaker(bind=engine)

            # 由Session类实例化一个session
            self.session = DBSession()

            Base.metadata.create_all(engine)

        def clean_up(self):
            self.session.close()


def fetch_history_price(ticker, n_last_days, mysql):
    ticker = ticker.upper()
    query_records = mysql.session.query(StockHistoryPrice).filter_by(TickerName=ticker)
    records = []
    for q_record in query_records:
        records.append(q_record)
    records.sort(key=lambda x: x.DateInteger)
    return records[-n_last_days:]


if __name__ == "__main__":
    ticker = "AAPL"
    n_last_days = 30
    mysql = MySQLUpdater()
    results = fetch_history_price(ticker, n_last_days, mysql)
    for result in results:
        print(result.AdjClosePrice)


