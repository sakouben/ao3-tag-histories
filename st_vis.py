import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

import az1

today_strf_Ymd = pd.Timestamp(datetime.today().strftime('%Y-%m-%d'))
character_dict = {
    "Aether":"Aether",
    "Albedo":"Albedo",
    "Aloy":"Aloy",
    "Amber":"Amber",
    "Arataki Itto":"Itto",
    "Barbara":"Barbara",
    "Beidou":"Beidou",
    "Bennett":"Bennett",
    "Candace":"Candace",
    "Chongyun":"Chongyun",
    "Collei":"Collei",
    "Cyno":"Cyno",
    "Diluc":"Diluc",
    "Diona":"Diona",
    "Dori":"Dori",
    "Eula":"Eula",
    "Faruzan":"Faruzan",
    "Fischl":"Fischl",
    "Ganyu":"Ganyu",
    "Gorou":"Gorou",
    "Hu Tao":"Hu Tao",
    "Jean":"Jean",
    "Kaedehara Kazuha":"Kazuha",
    "Kaeya":"Kaeya",
    "Kamisato Ayaka":"Ayaka",
    "Kamisato Ayato":"Ayato",
    "Keqing":"Keqing",
    "Klee":"Klee",
    "Kujou Sara":"Sara",
    "Kuki Shinobu":"Kuki",
    "Layla":"Layla",
    "Lisa":"Lisa",
    "Mona":"Mona",
    "Nahida":"Nahida",
    "Nilou":"Nilou",
    "Ningguang":"Ningguang",
    "Noelle":"Noelle",
    "Qiqi":"Qiqi",
    "Raiden Shogun":"Raiden",
    "Razor":"Razor",
    "Rosaria":"Rosaria",
    "Sangonomiya Kokomi":"Kokomi",
    "Sayu":"Sayu",
    "Shenhe":"Shenhe",
    "Shikanoin Heizou":"Heizou",
    "Sucrose":"Sucrose",
    "Tartaglia":"Tartaglia",
    "Thoma":"Thoma",
    "Tighnari":"Tighnari",
    "Lumine":"Lumine",
    "Venti":"Venti",
    "Wanderer":"Wanderer",
    "Xiangling":"Xiangling",
    "Xiao":"Xiao",
    "Xingqiu":"Xingqiu",
    "Xinyan":"Xinyan",
    "Yae Miko":"Miko",
    "Yanfei":"Yanfei",
    "Yelan":"Yelan",
    "Yoimiya":"Yoimiya",
    "Yun Jin":"Yun Jin",
    "Zhongli":"Zhongli"
}

char_displayed_list = list(character_dict.keys())
char_internal_list = list(character_dict.values())

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
    options=char_displayed_list
)

filtered_tags = []
for x in character_options:
    filtered_tags += tagswith(character_dict[x], PrimaryDB) 

options = st.multiselect(
    'Pick some tags!',
    set(filtered_tags) #prevents duplicates in dropdown
)

## END tag selector widget
## BEGIN x-axis date delimitation selector widgets

df = df.iloc[[*range(0, len(df)-1)]]

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
    ylabel = f"Average fics per day over a {rolling_days}-day window"
else:
    df = df[options]
    if absolute_type == "Weekly Average":
        chart_data = group_df(df, function="mean", time="week")
        ylabel = "Per-day Weekly Average"
    elif absolute_type == "Monthly Average":
        chart_data = group_df(df, function="mean", time="month")
        ylabel = "Per-day Monthly Average"
    elif absolute_type == "Weekly Sum":
        chart_data = group_df(df, function="sum", time="week")
        ylabel = absolute_type
    elif absolute_type == "Monthly Sum":
        chart_data = group_df(df, function="sum", time="month")
        ylabel = absolute_type
    

## END dataframe processing for final display
## BEGIN final chart display

BOOL_deltas_display = st.checkbox(label='Display deltas', value=True)

if BOOL_deltas_display == True:
    chart_data = chart_data.diff()
else:
    pass

st.subheader(body=ylabel)

if len(options) > 0:
    st.line_chart(
        data=chart_data
    )
else:
    st.text('Pick some tags!')
    


## END final chart display




