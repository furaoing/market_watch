# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, VARCHAR, DATETIME, Binary
from sqlalchemy.orm import sessionmaker

con_str = "%s+%s://%s:%s@%s/%s?charset=%s" % (DB_TYPE,
                                                  DB_CONNECTOR,
                                                  DB_USER,
                                                  DB_PASSWORD,
                                                  DB_HOST,
                                                  DB_DATABASE,
                                                  DB_CHARSET)


# 创建数据表结构的基类:
Base = declarative_base()

# 创建映射库内HeatTopic数据表结构的类:


class HeatTopic(Base):
    # 表名称字符串
    __tablename__ = "HeatTopic"

    # 字段定义
    HeatTopicID = Column(VARCHAR(32), primary_key=True, nullable=False)
    HeatTopicName = Column(VARCHAR(100), default=None, nullable=True)
    IssueID = Column(VARCHAR(32), default=None, nullable=True)
    QueryRule = Column(VARCHAR(1000), default=None, nullable=True)
    CreateTime = Column(DATETIME, default=None, nullable=True)
    IsDisabled = Column(Binary(1), default=0, nullable=True)


# 创建MYSQL Table的基类:
Base = declarative_base()

# 创建连接引擎
engine = create_engine(con_str, echo=True)

# 创建连接Session类
DBSession = sessionmaker(bind=engine)

# 由Session类实例化一个session
session = DBSession()
topic = HeatTopic(HeatTopicID="111",
                  HeatTopicName="111",
                          IssueID="Reader",
                          QueryRule="111",
                          )
session.add(topic)
session.commit()
session.close()