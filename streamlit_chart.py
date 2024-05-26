import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('naver_place/keyword_rank_top5test1.csv', low_memory=False)
st.title('을지로3가 맛집')
# df[df.search == '을지로3가 맛집']


df.loc['title',df.search == '을지로3가 맛집']


