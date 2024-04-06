# -*- coding: utf-8 -*-

import pandas as pd
from pandas import DataFrame as df

file_path = "D:\workspace\Libraries\BosonNLP_sentiment_score\BosonNLP_sentiment_score.txt"
my_df = pd.read_csv(file_path, sep=" ")
bb = my_df["freq"]
bb.plot()

