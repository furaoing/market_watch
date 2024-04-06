import json
from utils import get_share_outstanding



if __name__ == "__main__":
    share_outstanding = get_share_outstanding()
    fp_record = "data/RS_T0_pharma_record.jsonl"
    market_cap = {}
    market_cap_success = {}
    with open(fp_record, "r", encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            try:
                obj = json.loads(line)
            except:
                print(line)
                raise Exception
            for x in obj:
                stop_loss_flag = x["stop_loss"]
                sell_price = x["sell_price"]
                stock_symbol = x["stock_symbol"]
                date = x["signal/sell_time"]
                if stop_loss_flag:
                    shares = share_outstanding.get(stock_symbol, 0)
                    if shares:
                        market_cap_at_the_time_point = sell_price*shares/(1000000000)
                        market_cap[stock_symbol] = market_cap_at_the_time_point
                        print(stock_symbol)
                        print(date)
                if not stop_loss_flag:
                    shares = share_outstanding.get(stock_symbol, 0)
                    if shares:
                        market_cap_at_the_time_point = sell_price*shares/(1000000000)
                        market_cap_success[stock_symbol] = market_cap_at_the_time_point
    # print(market_cap)
    # avg_cap = sum(market_cap.values())/len(market_cap.values())
    # print(avg_cap)
    # print(market_cap_success)
    # avg_cap = sum(market_cap_success.values())/len(market_cap_success.values())
    # print(avg_cap)

