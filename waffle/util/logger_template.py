# -*- coding: utf-8 -*-

import logging


class LoggerTemplate(object):
    def __init__(self, log_pth):
        self.log_pth = log_pth
        self.level = logging.ERROR
        self.logger = logging.basicConfig(
            filename=self.log_pth,
            filemode="a",
            format="%(asctime)s %(levelname)s/%(name)s, %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=self.level
            )

    def debug(self, msg):
        return logging.debug(msg)

    def info(self, msg):
        return logging.info(msg)

    def warning(self, msg):
        return logging.warning(msg)

    def error(self, msg):
        return logging.error(msg)

    def critical(self, msg):
        return logging.critical(msg)


if __name__ == "__main__":
    logger = LoggerTemplate("test.log")
    logger.error("Error Occurred")




