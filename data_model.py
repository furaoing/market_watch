# -*- coding: utf-8 -*-

import json
from sqlalchemy import Column, VARCHAR, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
import time


def get_formated_time():
    struct_time = time.localtime()
    year = struct_time.tm_year
    month = struct_time.tm_mon
    day = struct_time.tm_mday
    hour = struct_time.tm_hour
    min = struct_time.tm_min
    sec = struct_time.tm_sec
    formated_time = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(min) + ":" + str(sec)
    return formated_time



class DataRequest(object):
    def __init__(self, symbol, url, data_request_type):
        self.symbol = symbol
        self.url = url
        self.data_request_type = data_request_type

    def __str__(self):
        return "symbol: %s, url: %s, data_request_type: %s" % (self.symbol, self.url, self.data_request_type)


class RequestResponse(object):
    def __init__(self, symbol, result_obj, data_request_type, validation_result):
        self.symbol = symbol
        self.result_obj = result_obj
        self.data_request_type = data_request_type
        self.validation_result = validation_result

    def __str__(self):
        return "symbol: %s, result_obj: %s, data_request_type: %s, validation_result: %s" % \
               (self.symbol, json.dumps(self.result_obj, ensure_ascii=False), self.data_request_type, self.validation_result)


# 创建数据表结构的基类:
Base = declarative_base()


class StockHistoryPrice(Base):
    # 表名称字符串
    __tablename__ = "StockHistoryPrice"

    # 字段定义
    Id = Column(VARCHAR(64), primary_key=True, nullable=False)
    TickerName = Column(VARCHAR(32), nullable=True, index=True)
    StockName = Column(VARCHAR(256), nullable=True)
    Open = Column(Float(6), nullable=True)
    AdjOpen = Column(Float(6), nullable=True)
    High = Column(Float(6), nullable=True)
    AdjHigh = Column(Float(6), nullable=True)
    Low = Column(Float(6), nullable=True)
    AdjLow = Column(Float(6), nullable=True)
    ClosePrice = Column(Float(6), nullable=True)
    AdjClosePrice = Column(Float(6), nullable=True)
    Volume = Column(BigInteger, nullable=True)
    AdjVolume = Column(BigInteger, nullable=True)
    DateFormated = Column(VARCHAR(32), nullable=False)    # Point in Trade Time, Eastern/US Timezone
    DateInteger = Column(BigInteger, nullable=False, index=True)     # Point in Trade Time, Eastern/US Timezone
    TimeCreated = Column(VARCHAR(32), default=get_formated_time, nullable=False)  # Server Time, Shanghai/China Timezone


class StockSharesOutstanding(Base):
    # 表名称字符串
    __tablename__ = "StockSharesOutstanding"

    # 字段定义
    Id = Column(VARCHAR(64), primary_key=True, nullable=False)
    TickerName = Column(VARCHAR(32), nullable=True, index=True)
    StockName = Column(VARCHAR(256), nullable=True)
    SharesOutstanding = Column(BigInteger, nullable=False)
    TimeCreated = Column(VARCHAR(32), default=get_formated_time, nullable=False)  # Server Time, Shanghai/China Timezone


class StockSymbol(Base):
    __tablename__ = "StockSymbol"

    # sid
    Id = Column(BigInteger, primary_key=True, nullable=False)
    TickerName = Column(VARCHAR(32), nullable=True, index=True)
    StockName = Column(VARCHAR(256), nullable=True)
    EffectiveDateFormated = Column(VARCHAR(32), nullable=False)
    EffectiveDateInteger = Column(BigInteger, nullable=False, index=True)


class IBShortDataUS(Base):
    # SYM|CUR|NAME|CON|ISIN|REBATERATE|FEERATE|AVAILABLE|
    __tablename__ = "IBShortDataUS"

    Id = Column(VARCHAR(64), primary_key=True, nullable=False)
    SYM = Column(VARCHAR(32), nullable=True, index=True)
    CUR = Column(VARCHAR(32), nullable=True)
    NAME = Column(VARCHAR(256), nullable=True)
    CON = Column(BigInteger, nullable=False, index=True)
    ISIN = Column(VARCHAR(256), nullable=True)
    REBATERATE = Column(Float(6), nullable=True)
    FEERATE = Column(Float(6), nullable=True)
    AVAILABLE = Column(VARCHAR(32), nullable=True)
    DateTimeFormated = Column(VARCHAR(32), nullable=False)    # File Date Time, Eastern/US Timezone
    DateTimeInteger = Column(BigInteger, nullable=False, index=True)     # File Date Time, Eastern/US Timezone
    TimeCreated = Column(VARCHAR(32), default=get_formated_time, nullable=False)  # Server Time, Shanghai/China Timezone


class IBShortDataHK(Base):
    # SYM|CUR|NAME|CON|ISIN|REBATERATE|FEERATE|AVAILABLE|
    __tablename__ = "IBShortDataHK"

    Id = Column(VARCHAR(64), primary_key=True, nullable=False)
    SYM = Column(VARCHAR(32), nullable=True, index=True)
    CUR = Column(VARCHAR(32), nullable=True)
    NAME = Column(VARCHAR(256), nullable=True)
    CON = Column(BigInteger, nullable=False, index=True)
    ISIN = Column(VARCHAR(256), nullable=True)
    REBATERATE = Column(Float(6), nullable=True)
    FEERATE = Column(Float(6), nullable=True)
    AVAILABLE = Column(VARCHAR(32), nullable=True)
    DateTimeFormated = Column(VARCHAR(32), nullable=False)    # File Date Time, Eastern/US Timezone
    DateTimeInteger = Column(BigInteger, nullable=False, index=True)     # File Date Time, Eastern/US Timezone
    TimeCreated = Column(VARCHAR(32), default=get_formated_time, nullable=False)  # Server Time, Shanghai/China Timezone


class Symbol(object):
    def __init__(self, sid, ticker_name, stock_name, effective_date):
        self.sid = sid
        self.ticker_name = ticker_name
        self.stock_name = stock_name
        self.effective_date = effective_date