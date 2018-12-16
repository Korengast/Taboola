__author__ = "Koren Gast"

import pandas as pd
import copy

# Files dir
sample_segments1_path = "C:\\Users\\koren\\PycharmRep\\Taboola\\raw_data\\sample_segments1.csv"
sample_segments2_path = "C:\\Users\\koren\\PycharmRep\\Taboola\\raw_data\\sample_segments2.csv"

s_seg_df = pd \
    .read_csv(sample_segments1_path) \
    .append(pd
            .read_csv(sample_segments2_path), ignore_index=True)

s_tot_df = s_seg_df.groupby(['campaign_id', 'd'])\
    .sum()\
    .reset_index()\
    .drop('user_data_directory_id', axis=1)\
    .rename({"d_segment_views": "views", "d_segment_clicks": "clicks"}, axis = 'columns')

s_seg_df['clicks_ratio'] = s_seg_df['d_segment_clicks'] / s_seg_df['d_segment_views']
s_tot_df['clicks_ratio'] = s_tot_df['clicks'] / s_tot_df['views']

def calc_click_rate(click_ratio, campaign, date):
    # Calculating click rate of a campaign-segment by comparing
    # the clicks ratio in a specific date of the segment
    # to the average click ratio for this date and campaign
    row = s_tot_df[s_tot_df['campaign_id'] == campaign][s_tot_df['d'] == date]
    return float(click_ratio / row['clicks_ratio'])

df = copy.deepcopy(s_seg_df)
s_seg_df['click_rate'] = df. \
    apply(lambda row: calc_click_rate(row['clicks_ratio'],
                                      row['campaign_id'],
                                      row['d']), axis=1)

s_seg_df.to_csv('data_v2\\segments.csv')