# -*- coding: utf-8 -*-

from waffle import system


if __name__ == "__main__":
    f_path = "/home/rao/hdfs-site.xml"
    content = system.f_read(f_path)
    print(content)
