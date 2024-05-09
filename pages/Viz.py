import pandas as pd
import streamlit as st

#import plotly.figure_factory as ff
import plotly.express as px


st.set_page_config(layout="wide")
st.title("Data Viz")
st.caption("LLM Hackathon for Materials & Chemistry - EPFL Hub")

df = pd.DataFrame(
    {'x': [0,1,2,3,4],
        'y': [0,1,4,9,16],
        'i': [0,1,0,3,1],
        }
)
fig = px.scatter(df, x='x', y='y', color='i')


st.plotly_chart(fig, theme="streamlit", use_container_width=True)