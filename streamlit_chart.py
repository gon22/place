import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from datetime import date as dt

# csv 불러오기

@st.cache_data
def long_function():
    return df


# # 메인화면 타이틀
# st.title(f'키워드 순위{}')

# # 메인화면 순위 컬럼 
# col1, col2, col3 = st.columns(3)

# with col1:
#    st.header("A cat")
#    st.image("https://static.streamlit.io/examples/cat.jpg")

# with col2:
#    st.header("A dog")
#    st.image("https://static.streamlit.io/examples/dog.jpg")

# with col3:
#    st.header("An owl")
#    st.image("https://static.streamlit.io/examples/owl.jpg")



#####################

# 날짜 및 시간 정보 추출
df['date_only'] = df['date'].dt.date
df['hour'] = df['date'].dt.hour

# 오전/오후 구분
df['period'] = df['hour'].apply(lambda x: '오전' if x < 12 else '오후')

# 타이틀별, 날짜별, 오전/오후별 순위 확인
rank_changes = df.pivot_table(index=['date_only', 'period'], columns='title', values='rank')

# Streamlit 대시보드
st.title('실시간 순위 차트')
st.write(f'가장 최근 날짜: {df["date_only"].max()}')

# 순위 변동 차트
st.write('## 순위 변동 차트')
st.dataframe(rank_changes)

# 순위 차트 시각화 (오전/오후 구분)
st.write('## 오전/오후 순위 차트')

for title in df['title'].unique():
    title_data = df[df['title'] == title]
    title_data = title_data.pivot(index='date', columns='period', values='rank')
    st.write(f'### {title}의 순위 변동')
    st.line_chart(title_data)

# 새로운 title 표시
latest_date = df['date_only'].max()
previous_date = df['date_only'].min()

latest_data = df[df['date_only'] == latest_date]
previous_data = df[df['date_only'] == previous_date]

latest_titles = set(latest_data['title'])
previous_titles = set(previous_data['title'])
new_titles = latest_titles - previous_titles

st.write('## 새로운 Title')
if new_titles:
    st.write('새로 추가된 title:')
    for title in new_titles:
        st.write(title)
else:
    st.write('새로운 title 없음')



#############

today_date = dt.today()
st.write("오늘 날짜 (날짜 부분만):", today_date)

