import pandas as pd
import glob
import os

folder = "data_code/trend_data"
files = glob.glob(os.path.join(folder, "trend_scores_*.csv"))

if not files:
    raise FileNotFoundError("No trend_scores_*.csv files found in data_code/trend_data/")


df_list = [pd.read_csv(f) for f in files]
full_result = pd.concat(df_list, ignore_index=True)
