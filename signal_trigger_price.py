import sys
import logging
from constants import Signal
from config import Config
from exceptions import TooManyRequest
import traceback
from database import MySQLUpdater
from database import fetch_history_price
from signals import RS_T0_Check, RS_T1_Check, RS_T2_Check, RS_T4_Check
import copy

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


def check_signal(ticker):
    try:
        ticker = ticker.upper()
        mysql = MySQLUpdater()
        n_last_days = 4
        history_prices = fetch_history_price(ticker, n_last_days, mysql)
        mysql.clean_up()
        history_prices = [x.ClosePrice for x in history_prices]
        last_price = history_prices[-1]
        signals = {Signal.RS_T0: -1, Signal.RS_T1: -1, Signal.RS_T2: -1, Signal.RS_T4: -1}
        x = last_price
        RS_T0_Check_Flag = False
        RS_T1_Check_Flag = False
        RS_T2_Check_Flag = False
        RS_T4_Check_Flag = False
        while x < last_price*5:
            close_price_list = copy.deepcopy(history_prices)
            close_price_list.append(x)
            two_days_price = close_price_list[-2:]
            three_days_price = close_price_list[-3:]
            four_days_price = close_price_list[-4:]
            five_days_price = close_price_list[-5:]

            RS_T0_Check_result = RS_T0_Check(two_days_price)
            RS_T1_Check_result = RS_T1_Check(three_days_price)
            RS_T2_Check_result = RS_T2_Check(five_days_price)
            RS_T4_Check_result = RS_T4_Check(four_days_price)

            if RS_T0_Check_result and not RS_T0_Check_Flag:
                signals[Signal.RS_T0] = round(x, 2)
                RS_T0_Check_Flag = True
            if RS_T1_Check_result and not RS_T1_Check_Flag:
                signals[Signal.RS_T1] = round(x, 2)
                RS_T1_Check_Flag = True
            if RS_T2_Check_result and not RS_T2_Check_Flag:
                signals[Signal.RS_T2] = round(x, 2)
                RS_T2_Check_Flag = True
            if RS_T4_Check_result and not RS_T4_Check_Flag:
                signals[Signal.RS_T4] = round(x, 2)
                RS_T4_Check_Flag = True
            if RS_T0_Check_Flag or RS_T1_Check_Flag or RS_T2_Check_Flag or RS_T4_Check_Flag:
                break
            if x < Config.MinimumPrice:
                x += 0.05
            else:
                x += 0.1
        root_logger.info(signals)
    except TooManyRequest:
        msg = "TooManyRequest" + "\n"
        root_logger.error(msg)
    except Exception:
        root_logger.error(traceback.format_exc())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
        check_signal(ticker)
    else:
        root_logger.error("No Ticker Given")
        raise Exception