# -*- coding: utf-8 -*-

import csv
from exceptions import IBShortDataFileFormatException
import datetime
from pytz import timezone


def parse_date(date_str, sep):
    split_result = date_str.split(sep)
    year = int(split_result[0])
    month = int(split_result[1])
    day = int(split_result[2])
    return year, month, day


def parse_time(time_str, sep):
    split_result = time_str.split(sep)
    hour = int(split_result[0])
    minute = int(split_result[1])
    sec = int(split_result[2])
    return hour, minute, sec


def read_IB_data(path):
    with open(path, newline='\n', encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        eof_record_stated = None
        records = []
        file_record_datetime = None
        i = 0
        for row in spamreader:
            if i == 0:
                # BOF|2019.09.30|02:30:02
                file_record_date = row[1]
                file_record_time = row[2]
                year, month, day = parse_date(file_record_date, ".")
                hour, min, sec = parse_time(file_record_time, ":")
                eastern = timezone('US/Eastern')
                file_record_datetime = datetime.datetime(year, month, day, hour, min, sec, tzinfo=eastern)
            elif i == 1:
                i += 1
                continue
            elif row[0] != "#EOF":
                if len(row) != 9:
                    raise IBShortDataFileFormatException
                else:
                    records.append(row[:-1])
            elif row[0] == "#EOF":
                eof_record_stated = int(row[1])
                break
            i += 1

        if len(records) != eof_record_stated:
            raise IBShortDataFileFormatException
        file_record = {"file_record_datetime": file_record_datetime, "records": records}
        return file_record


if __name__ == "__main__":
    path = "data/usa.txt"
    r = read_IB_data(path)
    print(str(r.get("file_record_datetime")))