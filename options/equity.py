# -*- coding: utf-8 -*-

from matplotlib import pyplot as plot


class Equity(object):
    def __init__(self, cost):
        self.cost = cost

    def exercise_value(self, market_price):
        raise NotImplemented


class LongEquity(Equity):
    def exercise_value(self, underlying_market_value) -> float:
        return underlying_market_value - self.cost


class ShortEquity(Equity):
    def exercise_value(self, underlying_market_value) -> float:
        return self.cost - underlying_market_value


if __name__ == "__main__":
    my_equity = ShortEquity(10)

    market_price_list = []
    value_list = []
    for i in range(200):
        market_price = 3 + 0.1*i
        market_price_list.append(market_price)
        value = my_equity.execrise_value(market_price)
        value_list.append(value)

    plot.plot(market_price_list, value_list)
    plot.show()