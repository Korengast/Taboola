__author__ = "Koren Gast"

import pandas as pd
import copy
import numpy as np
from matplotlib import pyplot as plt

# Files dir
sample_segments1_path = "C:\\Users\\koren\\PycharmRep\\Taboola\\raw_data\\sample_segments1.csv"
sample_segments2_path = "C:\\Users\\koren\\PycharmRep\\Taboola\\raw_data\\sample_segments2.csv"

s_seg_df = pd \
    .read_csv(sample_segments1_path) \
    .append(pd.read_csv(sample_segments2_path), ignore_index=True) \
    .dropna()

s_seg_df['clicks_ratio'] = s_seg_df['d_segment_clicks'] / s_seg_df['d_segment_views']

# Plotting click ratios vs #views.
plt.scatter(s_seg_df['d_segment_views'], s_seg_df['clicks_ratio'])
plt.show()

# Plotting click ratios vs #views only for #views > median
zoom_df = s_seg_df[s_seg_df['d_segment_views'] >= \
                   np.median(s_seg_df['d_segment_views'])]
plt.scatter(zoom_df['d_segment_views'], zoom_df['clicks_ratio'])
plt.show()

# Correcting the clicks_ratio calculation
# s_seg_df['clicks_ratio'] = s_seg_df['d_segment_clicks'] / (s_seg_df['d_segment_views'])**0.5

# Plot again
# plt.scatter(s_seg_df['d_segment_views'], s_seg_df['clicks_ratio'])
# plt.show()
# zoom_df = s_seg_df[s_seg_df['d_segment_views'] >= \
#                    np.median(s_seg_df['d_segment_views'])]
# plt.scatter(zoom_df['d_segment_views'], zoom_df['clicks_ratio'])
# plt.show()

s_seg_df = s_seg_df[s_seg_df['d_segment_views'] >= \
                    np.percentile(s_seg_df['d_segment_views'], 25)]

# Calculate the equivalent to the "total" csv
s_tot_df = s_seg_df[['campaign_id', 'd', 'd_segment_views', 'clicks_ratio']] \
    .groupby(['campaign_id', 'd']) \
    .sum() \
    .reset_index()


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
