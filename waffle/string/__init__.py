# -*- coding: utf-8 -*-

import string


def strip_punctuations(obj_str):
    del_str = "\n\r\t  ~`!@#$%^&*()_+-=	{}|[]\\:\";\'<>?,./~·！@#￥%……&*（）——+-=【】、{}|；‘：“，。、《》？"
    clean_str = obj_str.translate(string.maketrans("", ""), del_str)
    return clean_str


def linux_line_sep(s):
    s = s.replace("\r\n", "\n")
    s = s.replace("\r", "\n")
    return s


def win_line_sep(s):
    s = s.replace("\n", "\r\n")
    s = s.replace("\r", "\r\n")
    return s


def mac_line_sep(s):
    s = s.replace("\r\n", "\r")
    s = s.replace("\n", "\r")
    return s


if __name__ == "__main__":
    exp_str = 'a  bc#$dd%\tcc\tc'
    print(strip_punctuations(exp_str))