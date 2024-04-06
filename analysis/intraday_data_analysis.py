import pandas as pd

# %matplotlib inline
fp = r"data/2019-4-11-FTFT.json"

df = pd.read_json(fp)

open_price = df.iloc[0]["marketAverage"]
open_volume = df.iloc[0]["marketVolume"]
open_notional = open_price*open_volume
open_total = open_notional.sum()

above_open_df = df[df["marketAverage"] > open_price]
above_open_volume = above_open_df["marketVolume"]
above_open_price = above_open_df["marketAverage"]
above_open_notional = above_open_volume*above_open_price
above_open_total = above_open_notional.sum()

total_gain = above_open_total - open_total

print("Open Volume: %s" % open_volume)
print("Above Open Volume: %s" % above_open_volume.sum())
print("\n")

print("Open Total: %s" % open_total)
print("Above Open Total: %s" % above_open_total)
print("\n")

print("Difference: %s" % total_gain)
print("\n")