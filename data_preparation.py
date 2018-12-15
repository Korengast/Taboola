__author__ = "Koren Gast"

import pandas as pd
import copy

# Files dir
sample_segments1_path = "C:\\Users\\koren\\PycharmRep\\Taboola\\raw_data\\sample_segments1.csv"
sample_segments2_path = "C:\\Users\\koren\\PycharmRep\\Taboola\\raw_data\\sample_segments2.csv"
sample_total_path = "C:\\Users\\koren\\PycharmRep\\Taboola\\raw_data\\sample_total1.csv"

# Read both segments csv files, append them and add clicks_ratio column
s_seg_df = pd \
    .read_csv(sample_segments1_path) \
    .append(pd
            .read_csv(sample_segments2_path), ignore_index=True)
s_seg_df['clicks_ratio'] = s_seg_df['d_segment_clicks'] / s_seg_df['d_segment_views']

# Read total csv file and add clicks_ratio column
s_tot_df = pd \
    .read_csv(sample_total_path)
s_tot_df['clicks_ratio'] = s_tot_df['d_campaign_clicks'] / s_tot_df['d_campaign_views']

# The nonexist will hold the (campaign, d) pairs
# from the segments file that are not exist in the total file
nonexist_rows = {'campaign_id': [], 'd': [], 'click_ratio': [], }


def calc_click_rate(click_ratio, campaign, date):
    # Calculating click rate of a campaign-segment by comparing
    # the clicks ratio in a specific date of the segment
    # to the average click ratio for this date and campaign
    try:
        row = s_tot_df[s_tot_df['campaign_id'] == campaign][s_tot_df['d'] == date]
        return float(click_ratio / row['clicks_ratio'])
    except:
        print('Could not find row')
        nonexist_rows['campaign_id'].append(campaign)
        nonexist_rows['d'].append(date)
        nonexist_rows['click_ratio'].append(click_ratio)
        return None


df = copy.deepcopy(s_seg_df)
s_seg_df['click_rate'] = df. \
    apply(lambda row: calc_click_rate(row['clicks_ratio'],
                                      row['campaign_id'],
                                      row['d']), axis=1)

nonexist_rows = pd.DataFrame(nonexist_rows)

# Svaing the dataframes
s_seg_df.to_csv('data\\segments.csv')
s_tot_df.to_csv('data\\total.csv')
nonexist_rows.to_csv('data\\nonexist.csv')
