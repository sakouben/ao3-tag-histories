import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

import az1

today_strf_Ymd = pd.Timestamp(datetime.today().strftime('%Y-%m-%d'))

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

## END data initialization
## BEGIN tag selector widget

options = st.multiselect(
    'Pick some tags',
    tags,
    default="Kazuha/Xiao"
)

## END tag selector widget
## BEGIN x-axis date delimitation selector widgets

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

k = df.index.get_loc(today_strf_Ymd)
df = df.iloc[[*range(0, k)]]

try:
    k = df.index.get_loc(endd)
    df = df.iloc[[*range(0, k)]]
except:
    pass

## END x-axis date delimitation selector widgets
## BEGIN data summarization type widget

summarization_type = st.radio(
    "Choose data summarization type",
    ('Rolling', 'Absolute'),
    horizontal=True
)

## END data summarization type widget
## BEGIN data summarization type-specific widget: if rolling, number_input. elif absolute, radiobutton.

if summarization_type == "Rolling":
    rolling_days = st.number_input('Days to calculate rolling function over', min_value=1)
else:
    absolute_type = st.radio(
        "Choose timeframe and function for absolute display",
        ("Weekly Average", "Monthly Average", "Weekly Sum", "Monthly Sum"),
        horizontal=True
    )
    
## END data summarization type-specific widget
## BEGIN dataframe processing for final display

if summarization_type == "Rolling":
    dfrm = df[options].rolling(int(rolling_days)).mean()
    dfrm = dfrm.fillna(value=0)
    chart_data = dfrm
else:
    df = df[options]
    if absolute_type == "Weekly Average":
        chart_data = group_df(df, function="mean", time="week")
    elif absolute_type == "Monthly Average":
        chart_data = group_df(df, function="mean", time="month")
    elif absolute_type == "Weekly Sum":
        chart_data = group_df(df, function="sum", time="week")
    elif absolute_type == "Monthly Sum":
        chart_data = group_df(df, function="sum", time="month")

## END dataframe processing for final display
## BEGIN final chart display

if len(options) > 0:
    st.line_chart(chart_data)
else:
    st.text('Pick some tags!')

## END final chart display




