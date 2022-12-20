import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

import az1

PrimaryDB = az1.TagDB("tag-histories.csv")
df = PrimaryDB.read_DB()

tags = PrimaryDB.tags()

options = st.multiselect(
    'Pick some tags',
    tags,
)
    
rolling_avg_days = st.number_input('Days to calculate rolling average', min_value=1)

#startdate = st.date_input(
#    "x-axis start date",
#    datetime.date(2019, 7, 6))
#startd = pd.Timestamp(startdate).strftime("%Y-%m-%d")
#
#enddate = st.date_input(
#    "x-axis end date",
#    datetime.date(2023, 1, 1))
#endd = pd.Timestamp(enddate).strftime("%Y-%m-%d")
#
#try:
#    k = df.index.get_loc(startdate)
#    df = df.iloc[[k, len(df) - 1]]
#except:
#    pass
#
#try:
#    k = df.index.get_loc(enddate)
#    df = df.iloc[[0, k]]
#except:
#    pass

dfrm = df[options].rolling(int(rolling_avg_days)).mean()
dfrm = dfrm.fillna(value=0)

chart_data = dfrm


st.line_chart(chart_data)
