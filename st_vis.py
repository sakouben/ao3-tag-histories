import streamlit as st
import pandas as pd
import numpy as np

import az1

PrimaryDB = az1.TagDB("tag-histories.csv")
df = PrimaryDB.read_DB()

tags = PrimaryDB.tags()

options = st.multiselect(
    'Pick some tags',
    tags,
)
    
rolling_avg_days = st.number_input('Days to calculate rolling average', min_value=1)

dfrm = df[options].rolling(int(rolling_avg_days)).mean()
dfrm = dfrm.fillna(value=0)

chart_data = dfrm


st.line_chart(chart_data)
