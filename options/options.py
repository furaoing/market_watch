# -*- coding: utf-8 -*-

from datetime import datetime
from matplotlib import pyplot as plot


class AmericanOption(object):
    def __init__(self, strike_price, cost, expire_date: datetime=None):
        self.strike_price = strike_price
        self.cost = cost
        self.expire_date = expire_date

    # 行权价值
    def execrise_value(self, underlying_market_value) -> float:
        raise NotImplemented

    def is_expired(self, current_datetime: datetime) -> bool:
        return current_datetime > self.expire_date


class AmericanCallOption(AmericanOption):
    # The dollar return (investment proceeds - investment cost) when execrise the option
    def execrise_value(self, underlying_market_value) -> float:
        execrise_cost = self.strike_price + self.cost
        diff = underlying_market_value - execrise_cost
        if diff > (- self.cost):
            return diff
        else:
            return -self.cost


class AmericanPutOption(AmericanOption):
    # The dollar return (investment proceeds - investment cost) when execrise the option
    def execrise_value(self, underlying_market_value) -> float:
        execrise_proceed = self.strike_price - self.cost
        diff = execrise_proceed - underlying_market_value
        if diff > (- self.cost):
            return diff
        else:
            return -self.cost


if __name__ == "__main__":
    my_option = AmericanPutOption(10, 1)

    market_price_list = []
    value_list = []
    for i in range(200):
        market_price = 3 + 0.1*i
        market_price_list.append(market_price)
        value = my_option.execrise_value(market_price)
        value_list.append(value)

    plot.plot(market_price_list, value_list)
    plot.show()
