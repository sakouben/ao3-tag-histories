import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

import az1

today_strf_Ymd = pd.Timestamp(datetime.today().strftime('%Y-%m-%d'))

character_list = [
    "Aether",
    "Albedo",
    "Aloy",
    "Amber",
    "Arataki Itto",
    "Barbara",
    "Beidou",
    "Bennett",
    "Candace",
    "Chongyun",
    "Collei",
    "Cyno",
    "Diluc",
    "Diona",
    "Dori",
    "Eula",
    "Faruzan",
    "Fischl",
    "Ganyu",
    "Gorou",
    "Hu Tao",
    "Jean",
    "Kaedehara Kazuha",
    "Kaeya",
    "Kamisato Ayaka",
    "Kamisato Ayato",
    "Keqing",
    "Klee",
    "Kujou Sara",
    "Kuki Shinobu",
    "Layla",
    "Lisa",
    "Mona",
    "Nahida",
    "Nilou",
    "Ningguang",
    "Noelle",
    "Qiqi",
    "Raiden Shogun",
    "Razor",
    "Rosaria",
    "Sangonomiya Kokomi",
    "Sayu",
    "Shenhe",
    "Shikanoin Heizou",
    "Sucrose",
    "Tartaglia",
    "Thoma",
    "Tighnari",
    "Lumine",
    "Venti",
    "Wanderer",
    "Xiangling",
    "Xiao",
    "Xingqiu",
    "Xinyan",
    "Yae Miko",
    "Yanfei",
    "Yelan",
    "Yoimiya",
    "Yun Jin",
    "Zhongli"
]

def group_df(df, function="sum", time="month"):
    df['date'] = df.index
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['year'] = pd.to_datetime(df['date']).dt.year
    df.groupby(['year', 'month'], as_index=False).sum(numeric_only=True)
    df.index = pd.DatetimeIndex(df.index)
    df = df.drop('month', axis=1)
    df = df.drop('year', axis=1)
    
    if function == "sum":
        if time == "month":
            df = df.resample('M').sum(numeric_only=True)
        elif time == "week":
            df = df.resample('W').sum(numeric_only=True)
    elif function == "mean":
        if time == "month":
            df = df.resample('M').mean(numeric_only=True)
        elif time == "week":
            df = df.resample('W').mean(numeric_only=True)
    
    
    return df

def tagswith(character_name, DB_name): #returns list of tags containing character_name
    tag_sublist = list(
        filter(
        lambda x: character_name in x, DB_name.tags()
        )
    ) 
    
    return tag_sublist

PrimaryDB = az1.TagDB("tag-histories.csv")
df = PrimaryDB.read_DB()

tags = PrimaryDB.tags()

## END data initialization
## BEGIN tag selector widget

character_options = st.multiselect(
    label='Pick some characters!',
    options=character_list
)

filtered_tags = [tagswith(x, PrimaryDB) for x in character_options]

options = st.multiselect(
    'Pick some tags!',
    filtered_tags
)

## END tag selector widget
## BEGIN x-axis date delimitation selector widgets

k = df.index.get_loc(pd.Timestamp(datetime.today()).strftime("%Y-%m-%d"))
df = df.iloc[[*range(0, k)]]

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




