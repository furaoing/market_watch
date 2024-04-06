# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:23:52 2015

@author: Taikor
"""
import os
import time
import codecs
import json
import sys


def listdir_powered(folder):
    files = os.listdir(folder)
    myfiles = list()

    for file in files:
        myfiles.append(os.path.join(folder, file))
    myfiles = sorted(myfiles)
    return myfiles


def f_read(_file, readlines=False, strip_option=True):
    strip_option_enum = (True, False)
    readlines_enum = (True, False)

    if strip_option not in strip_option_enum:
        print("Wrong Argument Given: strip_option")
        raise Exception
    if readlines not in readlines_enum:
        print("Wrong Argument Given: readlines")
        raise Exception
    # check if a illegal argument was given

    if not readlines:
        with codecs.open(_file, "r", encoding="utf8") as f:
            s = f.read()
            if strip_option:
                s = s.strip("\n")
                s = s.strip("\r")
                s = s.strip(" ")
                s = s.strip("\t")
            return s
    else:
        with codecs.open(_file, "r", encoding="utf8") as f:
            s = f.readlines()

            if strip_option:
                for i in range(len(s)):
                    s[i] = s[i].strip("\n")
                    s[i] = s[i].strip("\r")
                    s[i] = s[i].strip(" ")
                    s[i] = s[i].strip("\t")
            return s


def f_read_generator(_file, strip_option=True):
    strip_option_enum = (True, False)
    if strip_option not in strip_option_enum:
        print("Wrong Argument Given: strip_option")
        raise Exception
    f = codecs.open(_file, "r", encoding="utf8")
    while True:
        yield f.readline()


def f_write(_file, content, mode="w"):
    with codecs.open(_file, mode, encoding="utf8") as f:
        f.write(content)
    return 0


def json_read(_file):
    json_str = f_read(_file)
    json_obj = json.loads(json_str)
    return json_obj


def json_write(_file, json_obj):
    json_str = json.dumps(json_obj, ensure_ascii=False)
    f_write(_file, json_str)
    return 0


class Timer(object):
    def __init__(self):
        self.start_time = time.time()
        self.end_time = 0
        self.t_elapsed = 0

    def __str__(self):
        return self.t_elapsed

    def start(self):
        self.start_time = time.time()
        return self.start_time

    def stop(self):
        self.end_time = time.time()
        return self._t_elapsed()

    def _t_elapsed(self):
        self.t_elapsed = self.end_time - self.start_time


def get_entry_pth():
    """
    Entry path refers to the directory path of the entry script
    :return:
    """
    tmp = sys.path[0]
    if sys.path[0] == "":
        return os.getcwd()
    else:
        return tmp


def get_entry_pth_parent():
    entry_pth = get_entry_pth()
    return os.path.dirname(entry_pth)


def get_entry_pth_basename():
    entry_pth = get_entry_pth()
    return os.path.basename(entry_pth)


def get_package_root():
    return get_entry_pth()


def get_package_name():
    return get_entry_pth_basename()


def extend_pythonpath():
    parent_of_package_root = get_entry_pth_parent()
    sys.path.append(parent_of_package_root)
    return True


def create_abs_path(rel_pth):
    """
    Create an abs path based on a path relative to the entry path
    :param rel_pth:
    :return:
    """
    base_path = get_entry_pth()
    abs_path = os.path.join(base_path, rel_pth)
    return abs_path


def abs_path(rel_pth):
    """
    Name Alias
    :param rel_pth:
    :return:
    """
    return create_abs_path(rel_pth)


if __name__ == "__main__":
    pass
