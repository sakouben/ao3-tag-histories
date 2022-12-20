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


import altair as alt


lines = (
    alt.Chart(df)
    .mark_line()
    .encode(x="date", y="price", color="symbol")
)

xrule = (
    alt.Chart()
    .mark_rule(color="cyan", strokeWidth=2)
    .encode(x=alt.datum(alt.DateTime(year=2020, month="November")))
)

yrule = (
    alt.Chart().mark_rule(strokeDash=[12, 6], size=2).encode(y=alt.datum(350))
)


lines + yrule + xrule
