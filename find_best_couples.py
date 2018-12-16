__author__ = "Koren Gast"

# import data_preparation
import pandas as pd
import numpy as np

segments_path = "data_v2\\segments.csv"
segments = pd.read_csv(segments_path)
segments = segments.dropna()

segments = segments[segments['d_segment_views'] >=
                    np.median(segments['d_segment_views'])]

best_100 = segments[['campaign_id', 'user_data_directory_id', 'd_segment_views', 'click_rate']]\
    .groupby(['campaign_id', 'user_data_directory_id'])\
    .sum()\
    .reset_index()\
    .sort_values('click_rate', ascending=0)\
    .head(100)