import time


def get_formated_time():
    struct_time = time.localtime()
    year = struct_time.tm_year
    month = struct_time.tm_mon
    day = struct_time.tm_mday
    hour = struct_time.tm_hour
    min = struct_time.tm_min
    formated_time = str(year) + "-" + str(month) + "-" + str(day) + "-" + str(hour) + "-" + str(min)
    return formated_time


def get_struct_stime():
    struct_time = time.localtime()
    return struct_time