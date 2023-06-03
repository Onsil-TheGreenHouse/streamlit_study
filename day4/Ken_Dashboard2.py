# import libs
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime

# load data

@st.cache_data
def load_data():
    df_agg = pd.read_csv('data/Aggregated_Metrics_By_Video.csv')
    df_agg = df_agg.iloc[1:, :]
    df_agg.columns = [
        'Video', 'Video title', 'Video publish time', 'Comments added', 'Shares', 'Dislikes', 'Likes',
        'Subscribers lost', 'Subscribers gained', 'RPM(USD)', 'CPM(USD)', 'Average % viewed', 'Average view duration',
        'Views', 'Watch time (hours)', 'Subscribers', 'Your estimated revenue (USD)', 'Impressions', 'Impression ctr(%)'
    ]
    df_agg['Video publish time'] = df_agg['Video publish time'].apply(lambda x: x.replace('Jan', 'January')
                                                                      .replace('Feb', 'February')
                                                                      .replace('Mar', 'March')
                                                                      .replace('Apr', 'April')
                                                                      .replace('Jun', 'June')
                                                                      .replace('Jul', 'July')
                                                                      .replace('Aug', 'August')
                                                                      .replace('Sep', 'September')
                                                                      .replace('Oct', 'October')
                                                                      .replace('Nov', 'November')
                                                                      .replace('Dec', 'December'))
    df_agg['Video publish time'] = pd.to_datetime(df_agg['Video publish time'])
    df_agg['Average view duration'] = df_agg['Average view duration'].apply(lambda x: datetime.strptime(x, '%H:%M:%S'))
    df_agg['Avg_duration_sec'] = df_agg['Average view duration'].apply(lambda x: x.second + x.minute*60 + x.hour*3600)
    df_agg['Engagement_ratio'] = (df_agg['Comments added'] + df_agg['Shares'] + df_agg['Dislikes'] + df_agg['Likes']) / df_agg.Views
    df_agg['Views / sub gained'] = df_agg['Views'] / df_agg['Subscribers gained']
    df_agg.sort_values('Video publish time', ascending=False, inplace=True)

    df_agg_sub = pd.read_csv('data/Aggregated_Metrics_By_Country_And_Subscriber_Status.csv')

    df_comments = pd.read_csv('data/Aggregated_Metrics_By_Video.csv')
    df_time = pd.read_csv('data/Video_Performance_Over_Time.csv')
    df_time['Date'] = pd.to_datetime(df_time['Date'].apply(lambda x: x.replace('Sept', 'Sep')))

    return df_agg, df_agg_sub, df_comments, df_time


df_agg, df_agg_sub, df_comments, df_time = load_data()

#engineer data
df_agg_diff = df_agg.copy()
metric_date_12mo = df_agg_diff['Video publish time'].max() - pd.DateOffset(months=12)
one_year_agg = df_agg_diff[df_agg_diff['Video publish time'] >= metric_date_12mo]

numeric_cols = np.array((df_agg_diff.dtypes == 'float64') | (df_agg_diff.dtypes == 'int64'))
median_agg = one_year_agg.iloc[:, numeric_cols].median()
df_agg_diff =


add_sidebar = st.sidebar.selectbox('Aggregate or Individual Video', ('Aggregate Metrics', 'Individual Video Analysis'))

print('End of code')
