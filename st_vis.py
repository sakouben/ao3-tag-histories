import streamlit as st
import pandas as pd
import numpy as np

import az1

PrimaryDB = az1.TagDB("tag-histories.csv")
df = PrimaryDB.read_DB()

tags = df.tags()

options = st.multiselect(
    'Pick some tags',
    tags,
)

st.write('You selected:', options)
    
chart_data = df["Venti/Xiao"]

st.line_chart(chart_data)
