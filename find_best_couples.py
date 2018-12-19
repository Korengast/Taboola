__author__ = "Koren Gast"

# import data_preparation_v2
import pandas as pd
import numpy as np

segments_path = "data_v2\\segments.csv"
segments = pd.read_csv(segments_path)

sorted_df = segments[['campaign_id', 'user_data_directory_id', 'd_segment_views', 'click_rate']] \
    .groupby(['campaign_id', 'user_data_directory_id']) \
    .sum() \
    .reset_index() \
    .sort_values('click_rate', ascending=0)

print('Average views: {}'.format(np.mean(sorted_df['d_segment_views'])))
print('Average best 100 views: {}'.format(np.mean(sorted_df.head(100)['d_segment_views'])))

sorted_df.head(100).to_csv('best_100')
