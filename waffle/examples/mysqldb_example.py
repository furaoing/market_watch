# -*- coding: utf-8 -*-

import MySQLdb


class MySQLdriver(object):
    def __init__(self, _host, _user, _passwd, _db):
        self.db = MySQLdb.Connect(
            host=_host,
            user=_user,
            passwd=_passwd,
            db=_db
        )
        self.db.query('SET NAMES utf8')
        self.cursor = self.db.cursor()

    def insert(self, sql):
        sql = sql.encode('utf8')
        self.cursor.execute(sql)
        self.db.commit()

    def check_records(self, sql):
        sql = sql.encode('utf8')
        self.cursor.execute(sql)
        self.db.commit()
        result = self.cursor.fetchall()
        return result

    def clean_up(self):
        self.db.close()



