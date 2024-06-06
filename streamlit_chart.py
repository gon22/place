import streamlit as st
import pandas as pd
import numpy as np
import urllib.request
import json

from datetime import datetime, timedelta
from datetime import date as dt
import time

import plotly.express as px
import pytz



## 실시간 데이터 보기
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# client_id = "K25hzGPrWL8hskBSJWND"
# client_secret = "SSKeYoapXo"


regions = '서울'
query = ['을지로3가 맛집','을지로3가 와인','을지로3가 위스키', '을지로3가 술집']

def place_top5(client_id, client_secret, query, *regions):
    regions = list(regions)
    query = query
    result_list=[]
    for region in regions:
        for q in query:
            region_query = region + ' ' + q
            encText = urllib.parse.quote(region_query)
            url = "https://openapi.naver.com/v1/search/local.json?query=" + encText + "&display=50"
    
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            
            if(rescode==200):
                response_body = response.read()
                results = json.loads(response_body)['items']
                
                for i, result in enumerate(results):
                    result['rank'] = i+1
                    result['search'] = q
                    result['region'] = region
                    result['title'] = result['title'].replace('<b>','').replace('</b>','')
                    result['date'] = datetime.now()
                    result_list.append(result)
            else:
                print("Error Code:" + rescode)
                
    df = pd.DataFrame(result_list)
    return df

df_real = place_top5(client_id, client_secret, query, regions)

# search를 search로 비꿈
df_real.rename(columns={'search': 'keyword'}, inplace=True)
# 특정 키워드로 필터링된 데이터
df111 = df_real.loc[df_real['keyword'] == '을지로3가 맛집', ['rank', 'title']].rename(columns={'title': '을지로3가 맛집'})
df222 = df_real.loc[df_real['keyword'] == '을지로3가 와인',['rank', 'title']].rename(columns={'title': '을지로3가 와인'})
df333 = df_real.loc[df_real['keyword'] == '을지로3가 위스키',['rank', 'title']].rename(columns={'title': '을지로3가 위스키'})
df444 = df_real.loc[df_real['keyword'] == '을지로3가 술집',['rank', 'title']].rename(columns={'title': '을지로3가 술집'})

# 'rank'를 기준으로 병합
merged_df_real = df111.merge(df222, on='rank', how='outer')\
               .merge(df333, on='rank', how='outer')\
               .merge(df444, on='rank', how='outer')

st.header(f'플레이스 TOP5')
now = datetime.today()
st.write(now.strftime('%Y-%m-%d %H:%M'))
merged_df_real = merged_df_real.sort_values(by='rank').set_index('rank')
st.dataframe(merged_df_real)



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

# 현재 날짜 가져오기
today = datetime.today()
# 메인화면 타이틀

#######################

from itertools import cycle

# 타이틀별 색상 맵 초기화
color_palette = cycle(px.colors.qualitative.Plotly)  # Plotly의 색상 팔레트 사용
color_map = {}

# 특정 키워드로 필터링된 데이터
df11 = df[df['keyword'] == '을지로3가 맛집']
df22 = df[df['keyword'] == '을지로3가 와인']
df33 = df[df['keyword'] == '을지로3가 위스키']
df44 = df[df['keyword'] == '을지로3가 술집']

filter = {'을지로3가 맛집': df11, '을지로3가 와인': df22, '을지로3가 위스키': df33, '을지로3가 술집': df44}
st.header('순위 변동 차트')
filtered_df = st.selectbox(
    label="키워드 선택", 
    help="키워드 선택하여 top5 업체 순위 변동 확인", 
    options=list(filter.keys())
)

# 선택된 데이터프레임
selected_df = filter[filtered_df]

# 타이틀별 색상 할당
for title in selected_df['title'].unique():
    if title not in color_map:
        color_map[title] = next(color_palette)

# Plotly 선 그래프 생성
fig = px.line(
    selected_df, 
    x="kodate", 
    y="rank", 
    color="title", 
    line_group="title", 
    markers=True,
    color_discrete_map=color_map  # 색상 맵 적용
)

# y축을 반대로 설정
fig.update_yaxes(autorange='reversed')

# 레전드를 위쪽에 배치
fig.update_layout(
    xaxis_title="Date", 
    yaxis_title="Rank", 
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

specific_title = "르템플"
fig.update_traces(
    line=dict(width=5),  # 원하는 선 두께 지정
    selector=dict(name=specific_title)  # 특정 타이틀 선택
)

# 나머지 선 스타일을 대시로 변경
fig.for_each_trace(
    lambda trace: trace.update(line=dict(dash='dash')) if trace.name != specific_title else ()
)

# 스트림릿에 Plotly 그래프 표시
st.plotly_chart(fig, use_container_width=True)


# st.header(f'플레이스 TOP5')

# col1, col2= st.columns(2)

# with col1:
#    # 날짜 선택 필터
#     option = st.date_input(
#         "날짜", 
#         help='2024-05-26 이후부터 가능',
#         min_value=datetime(2024, 5, 26),
#         value=datetime(today.year, today.month, today.day)  # 초기값 설정
#     )
# with col2:
#     # 오전/오후 선택 필터
#     apm = ['오전', '오후']
#     option_apm = st.selectbox(
#         label="시점", 
#         help="오전 (pm01), 오후 (pm07)",
#         options=apm
#     )


# # 키워드에 따른 데이터 필터링 함수
# def filter_data(keyword, date, period):
#     return df.loc[(df['keyword'] == keyword) & (df['date_only'] == date) & (df['period'] == period), ['rank', 'title']].rename(columns={'title': keyword})

# # 키워드별 데이터프레임 생성 및 열 이름 변경
# df1 = filter_data('을지로3가 맛집', option, option_apm)
# df2 = filter_data('을지로3가 와인', option, option_apm)
# df3 = filter_data('을지로3가 위스키', option, option_apm)
# df4 = filter_data('을지로3가 술집', option, option_apm)

# # 'rank'를 기준으로 병합
# merged_df = df1.merge(df2, on='rank', how='outer')\
#                .merge(df3, on='rank', how='outer')\
#                .merge(df4, on='rank', how='outer')

# # 중복된 행 제거
# merged_df = merged_df.drop_duplicates(subset='rank')

# # 'rank' 기준으로 정렬하고 인덱스로 설정
# merged_df = merged_df.sort_values(by='rank').set_index('rank')

# # 정렬된 데이터프레임 출력
# st.dataframe(merged_df)
