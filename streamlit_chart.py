import streamlit as st
import pandas as pd
import numpy as np

st.title('을지로3가 맛집')
# df[df.search == '을지로3가 맛집']

@st.cache_data
def long_function():
    df = pd.read_csv('naver_place/keyword_rank_top5test1.csv', low_memory=False)
    return df

long_function()

col1, col2, col3 = st.columns(3)

with col1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg")


