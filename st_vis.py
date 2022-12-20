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
    
chart_data = df[options]

st.line_chart(chart_data)
