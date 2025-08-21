import pandas as pd

avg_user_count_df = pd.read_csv('data_code/sofascore_data/avg_user_count_df.csv')
avg_user_count_dict = dict(zip(avg_user_count_df['keyword'], avg_user_count_df['avg_user_count_score']))
# print(avg_user_count_dict)

avg_home_score_df = pd.read_csv('data_code/sofascore_data/avg_home_score_df.csv')
avg_home_score_dict = dict(zip(avg_home_score_df['keyword'], avg_home_score_df['avg_home_score']))
