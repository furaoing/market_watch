# -*- coding: utf-8 -*-

import time


class Time(object):
    def get_time_zone(self):
        time_zone_affix = None
        local_time_struct = time.localtime()
        gmt_time_struct = time.gmtime()
        time_diff = local_time_struct.tm_hour - gmt_time_struct.tm_hour
        if time_diff < 10:
            time_zone_affix = "+0%d:00" % time_diff
        else:
            time_zone_affix = "+%d:00" % time_diff
        return time_zone_affix


class TimeFormater(Time):
    """
    Create a UTC style string to represent time
    """
    def __init__(self, style="es"):
        self.style = style

    def _add_zero_char(self, my_int):
        my_str = str(my_int)
        if len(my_str) == 1:
            my_str = "0" + my_str
        return my_str

    def format_time(self):
        style = self.style
        formated_time = None
        style_enum = ("es", "mysql", "log")

        if style not in style_enum:
            raise Exception

        struct_time = time.localtime()
        year = struct_time.tm_year
        month = struct_time.tm_mon
        day = struct_time.tm_mday
        hour = struct_time.tm_hour
        _min = struct_time.tm_min
        sec = struct_time.tm_sec

        year = self._add_zero_char(year)
        month = self._add_zero_char(month)
        day = self._add_zero_char(day)
        hour = self._add_zero_char(hour)
        _min = self._add_zero_char(_min)
        sec = self._add_zero_char(sec)

        if style == "es":
            formated_time = year + "-" + month + "-" + day + "T" + \
                            hour + ":" + _min + ":" + sec + self.get_time_zone()
        elif style == "mysql":
            formated_time = year + "-" + month + "-" + day + " " + \
                            hour + ":" + _min + ":" + sec
        else:
            formated_time = year + "-" + month + "-" + day + " " + \
                            hour + ":" + _min + ":" + sec

        return formated_time

    def format_time_as_fn(self):
        """ fn = file name """
        fm_time = self.format_time()
        fm_time_as_fn = fm_time.replace(r":", "-")
        return fm_time_as_fn


if __name__ == "__main__":
    tf = TimeFormater("es")
    print(tf.format_time_as_fn())
    b = time.tzname
    a = 1
