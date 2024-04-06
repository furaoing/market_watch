import logging
import sys


error_handler = logging.StreamHandler(sys.stderr)
error_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s/%(name)s, %(message)s"))
error_handler.setLevel(logging.ERROR)

info_handler = logging.StreamHandler(sys.stdout)
info_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s/%(name)s, %(message)s"))
info_handler.setLevel(logging.INFO)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(error_handler)
root_logger.addHandler(info_handler)
