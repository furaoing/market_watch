import json
import matplotlib.pyplot as plt


with open("bynd_short_record.json", "r") as f:
    data = json.loads(f.read())


new_data = {}
for x in data:
    date = int(x["date"])
    short_volume = x["short_volume"]
    total_volume = x["total_volume"]
    if date not in new_data.keys():
        new_data[date] = {"short_volume": short_volume, "total_volume": total_volume}
    else:
        new_data[date]["short_volume"] += short_volume
        new_data[date]["total_volume"] += total_volume


new_data_list = list(new_data.items())
new_data_list.sort(key=lambda x: x[0])

print(new_data_list)

short_rate_daily = [[x[0], x[1]["short_volume"]/x[1]["total_volume"]] for x in new_data_list]

date = []
ratio = []
for x in short_rate_daily:
    date.append(x[0])
    ratio.append(x[1])

plt.plot(date, ratio)