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
    
dfrm = df[options].rolling(7).mean()
dfrm = dfrm.fillna(value=0)

chart_data = dfrm


st.line_chart(chart_data)
