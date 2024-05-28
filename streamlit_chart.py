import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
from datetime import date as dt
import time

import plotly.express as px
import pytz

# csv 불러오기

df = pd.read_csv('naver_place/keyword_rank_top5test1.csv', low_memory=False)
@st.cache_data
def long_function():
    return df

# search를 search로 비꿈
df.rename(columns={'search': 'keyword'}, inplace=True)
######################################################

# 'date' 열을 datetime 형식으로 변환
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# datetime 변환이 실패한 경우를 처리 (예: NaT로 설정된 값 제거)
df = df.dropna(subset=['date'])

# 날짜 및 시간 정보 추출
df['date_only'] = df['date'].dt.date
df['hour'] = df['date'].dt.hour

# 시간대 설정
KST = pytz.timezone('Asia/Seoul')
df['kodate'] = df['date'].dt.tz_localize('UTC').dt.tz_convert(KST)

# 오늘 날짜 필터링
today = datetime.today().date()
df['date_only'] = df['date'].dt.date
today_data = df[df['date_only'] == today]

# 오전/오후 구분
df['period'] = df['hour'].apply(lambda x: '오전' if x == 4 else '오후')
df['ko_hour'] = df['hour'].apply(lambda x: 13 if x == 4 else 19)

# 날짜 중복 제거 
date_filter = list(set(df['date_only']))


# 메인화면 타이틀

st.header(f'플레이스 TOP5')

col1, col2= st.columns(2)

with col1:
   # 날짜 선택 필터
    option = st.date_input(
        "날짜", 
        help='2024-05-26 이후부터 가능',
        min_value=datetime(2024, 5, 26),
        value=datetime(2024, 5, 26)  # 초기값 설정
    )
with col2:
    # 오전/오후 선택 필터
    apm = ['오전', '오후']
    option_apm = st.selectbox(
        label="시점", 
        help="오전 (pm01), 오후 (pm07)",
        options=apm
    )


# 키워드에 따른 데이터 필터링 함수
def filter_data(keyword, date, period):
    return df.loc[(df['keyword'] == keyword) & (df['date_only'] == date) & (df['period'] == period), ['rank', 'title']]

# 키워드별 데이터프레임 생성 및 열 이름 변경
df1 = filter_data('을지로3가 맛집', option, option_apm).rename(columns={'title': '을지로3가 맛집'})
df2 = filter_data('을지로3가 와인', option, option_apm).rename(columns={'title': '을지로3가 와인'})
df3 = filter_data('을지로3가 위스키', option, option_apm).rename(columns={'title': '을지로3가 위스키'})
df4 = filter_data('을지로3가 술집', option, option_apm).rename(columns={'title': '을지로3가 술집'})

# 'rank'를 기준으로 병합
merged_df = df1.merge(df2, on='rank', how='outer')\
               .merge(df3, on='rank', how='outer')\
               .merge(df4, on='rank', how='outer')

# 'rank' 기준으로 정렬하고 인덱스로 설정
merged_df = merged_df.sort_values(by='rank').set_index('rank')

# 정렬된 데이터프레임 출력
st.dataframe(merged_df)

###################

# asd = df.title.copy()
# cc = asd.drop_duplicates()
# cc


# 특정 키워드로 필터링된 데이터
df11 = df[df['keyword'] == '을지로3가 맛집']
df22 = df[df['keyword'] == '을지로3가 와인']
df33 = df[df['keyword'] == '을지로3가 위스키']
df44 = df[df['keyword'] == '을지로3가 술집']

filter = {'을지로3가 맛집': df11, '을지로3가 와인': df22, '을지로3가 위스키': df33, '을지로3가 술집': df44}
st.header('업체 순위 변동 차트')
filtered_df = st.selectbox(
        label="", help="키워드 선택하여 top5 업체 순위 변동 확인",
        options=filter)

# Plotly 선 그래프 생성
fig = px.line(filter[filtered_df], x="kodate", y="rank", color="title", line_group="title", markers=True)

# y축을 반대로 설정
fig.update_yaxes(autorange='reversed')
fig.update_layout(xaxis_title="Date", yaxis_title="Rank", showlegend=True)

# 스트림릿에 Plotly 그래프 표시
st.plotly_chart(fig, use_container_width=True)


##################

