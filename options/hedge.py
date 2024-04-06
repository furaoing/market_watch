# -*- coding: utf-8 -*-

from matplotlib import pyplot as plot
from options import AmericanCallOption, AmericanPutOption
from equity import ShortEquity


strike = 10
call_option_cost = 1
put_option_cost = 2
current_market_price = 9

call_option = AmericanCallOption(strike, call_option_cost)
put_option = AmericanPutOption(strike, put_option_cost)
equity = ShortEquity(current_market_price)


if __name__ == "__main__":
    market_price_list = []
    value_list = []
    for i in range(200):
        market_price = 3 + 0.1*i
        market_price_list.append(market_price)
        call_option_value = call_option.execrise_value(market_price)
        put_option_value = put_option.execrise_value(market_price)
        equity_value = equity.exercise_value(market_price)
        net_value = call_option_value + equity_value
        value_list.append(put_option_value)

    plot.plot(market_price_list, value_list)
    plot.show()