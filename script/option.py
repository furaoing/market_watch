# -*- coding: utf-8 -*-


def get_leverage(strike_price, option_price):
    return (strike_price + option_price)/option_price


def get_target_return(strike_price, option_price, target_price):
    profit = target_price - (strike_price + option_price)
    return profit/option_price


if __name__ == "__main__":
    target_price = 60
    s_set = [
        [42.5, 4.3, target_price],
        [45, 3.3, target_price],
        [47.5, 2.65, target_price],
        [50, 1.93, target_price]]

    for s in s_set:
        strike_price = s[0]
        option_price = s[1]
        target_price = s[2]
        return_ratio = get_target_return(strike_price, option_price, target_price)
        #print("Input: %s" % str(s))
        print("Return: %s" % return_ratio)

