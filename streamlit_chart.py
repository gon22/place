import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime
from datetime import date as dt

# csv 불러오기
@st.cache_data
def long_function():
    df = pd.read_csv('naver_place/keyword_rank_top5test1.csv', low_memory=False)
    return df

long_function()

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

# # 날짜별 순위 변동 확인
# df['date'] = pd.to_datetime(df['date'])
# latest_date = df['date'].max()
# previous_date = df['date'].min()

# # 가장 최근 날짜와 이전 날짜 데이터 비교
# latest_data = df[df['date'] == latest_date]
# previous_data = df[df['date'] == previous_date]

# # 새로운 title 및 순위 변동 확인
# latest_titles = set(latest_data['title'])
# previous_titles = set(previous_data['title'])
# new_titles = latest_titles - previous_titles
# rank_changes = latest_data[latest_data['title'].isin(previous_titles)]

# # Streamlit 대시보드
# st.title('실시간 순위 차트')
# st.write(f'가장 최근 날짜: {latest_date.strftime("%Y-%m-%d")}')
# st.write(f'이전 날짜: {previous_date.strftime("%Y-%m-%d")}')

# # 순위 변동 차트
# st.write('## 순위 변동 차트')
# st.dataframe(rank_changes)

# # 새로운 title 표시
# st.write('## 새로운 Title')
# if new_titles:
#     st.write('새로 추가된 title:')
#     for title in new_titles:
#         st.write(title)
# else:
#     st.write('새로운 title 없음')

# # 순위 차트 시각화
# st.write('## 순위 차트')
# st.line_chart(df.pivot(index='date', columns='title', values='rank'))



#############

today_date = dt.today()
st.write("오늘 날짜 (날짜 부분만):", today_date)
df.head()
