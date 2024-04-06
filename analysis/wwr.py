import json

fp = r"data/wwr_history.json"
with open(fp, "r", encoding="utf8") as f:
    c = f.read()
data = json.loads(c)

for i in range(len(data)):
    x = data[i]
    date = x["date"]
    unadj_open = x["uOpen"]
    unadj_price = x["uClose"]
    print("%s     %s     %s" % (date, unadj_open, unadj_price))


# import pandas as pd
#
# df = pd.read_json(fp)
# sel = df[df["date"] > "2012-08-02"]["date"]
#
# print(sel)


