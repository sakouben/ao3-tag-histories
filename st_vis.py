import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

import az1

def group_df(df, function="sum", time="month"):
    df['date'] = df.index
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['year'] = pd.to_datetime(df['date']).dt.year
    df.groupby(['year', 'month'], as_index=False).sum()
    df.index = pd.DatetimeIndex(df.index)
    df = df.drop('month', axis=1)
    df = df.drop('year', axis=1)
    
    if function == "sum":
        if time == "month":
            df = df.resample('M').sum()
        elif time == "week":
            df = df.resample('W').sum()
    elif function == "mean":
        if time == "month":
            df = df.resample('M').mean()
        elif time == "week":
            df = df.resample('W').mean()
    
    
    return df

PrimaryDB = az1.TagDB("tag-histories.csv")
df = PrimaryDB.read_DB()

tags = PrimaryDB.tags()

summarization_type = st.radio(
    "Choose data summarization type",
    ('Rolling', 'Absolute'))


options = st.multiselect(
    'Pick some tags',
    tags,
    default="Kazuha/Xiao"
)

if summarization_type == "Rolling":
    rolling_days = st.number_input('Days to calculate rolling function over', min_value=1)
else:
    absolute_type = st.radio(
        "Choose timeframe to calculate absolute function over",
        ("Weekly", "Monthly")
    )

startdate = st.date_input(
    "x-axis start date")
startd = pd.Timestamp(startdate).strftime("%Y-%m-%d")

enddate = st.date_input(
    "x-axis end date")
endd = pd.Timestamp(enddate).strftime("%Y-%m-%d")

try:
    k = df.index.get_loc(startd)
    df = df.iloc[[*range(k, len(df) - 1)]]
except:
    pass

try:
    k = df.index.get_loc(endd)
    df = df.iloc[[*range(0, k)]]
except:
    pass

dfrm = df[options].rolling(int(rolling_days)).mean()
dfrm = dfrm.fillna(value=0)

chart_data = dfrm
chart_data_2 = group_df(df)



if summarization_type == "Rolling":
    st.line_chart(chart_data)
else:
    st.line_chart(chart_data_2)






