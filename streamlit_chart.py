import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
from datetime import date as dt

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

st.header(f'{today} (today)')

col1, col2= st.columns(2)

with col1:
    # 날짜 선택 필터
   option = st.date_input("확인하고 싶은 날짜를 선택 하세요.", value=None)
with col2:
    # 오전오후 선택 필터
    apm = ['오전','오후']
    option_apm = st.selectbox(
        "오전 (전날 pm07 - pm01), 오후 (pm01 - pm07)",
        (apm))

# ######################################################
# # 하루 전의 날짜 계산
# one_day_before = date_filter - timedelta(days=1)

# # 전날 데이터
# yesterday_data = df[df['date_only'] == one_day_before]

# # 전날 데이터에서 rank 열의 이름을 변경하여 오늘 데이터와 병합할 준비
# yesterday_data = yesterday_data.rename(columns={'rank': 'rank_yesterday'})

# # 오늘 데이터
# today_data = df[df['date_only'] == option]

# # 오늘 데이터에서 필요한 열만 선택
# today_data = today_data[['keyword', 'rank']]

# # 전날과 오늘 데이터를 키워드를 기준으로 병합
# merged_data = pd.merge(today_data, yesterday_data, on='keyword', how='left')

# # 전날 순위와 오늘 순위를 비교하여 순위 차이 계산
# merged_data['rank_diff'] = merged_data['rank_yesterday'] - merged_data['rank']

# # 순위 차이가 양수인 경우에만 '상승', 음수인 경우에는 '하락', 그 외에는 '-'을 지정
# merged_data['rank_change'] = np.where(merged_data['rank_diff'] > 0, '상승', 
#                                       np.where(merged_data['rank_diff'] < 0, '하락', '-'))

# 필요한 열만 선택하여 출력
# result_df = merged_data[['keyword', 'rank_yesterday', 'rank', 'rank_diff', 'rank_change']]
# st.write(result_df)
st.divider()
st.header('르템플 키워드 순위')
a = df.loc[(df['keyword']=='을지로3가 맛집') & (df['date_only']==option) & (df['title']=='르템플') & (df['period']==option_apm),'rank'].values
b = df.loc[(df['keyword']=='을지로3가 와인') & (df['date_only']==option) & (df['title']=='르템플') & (df['period']==option_apm),'rank'].values
c = df.loc[(df['keyword']=='을지로3가 위스키') & (df['date_only']==option) & (df['title']=='르템플') & (df['period']==option_apm),'rank'].values
d = df.loc[(df['keyword']=='을지로3가 술집') & (df['date_only']==option) & (df['title']=='르템플') & (df['period']==option_apm),'rank'].values
tt = ''

def main_rank(tt):
    if not a:
        tt = '순위 밖 또는 데이터 없음'
        st.write(f'을지로3가 맛집 : {tt}')
    else:
        tt = a[0]
        st.write(f'을지로3가 맛집 : {tt}위')
    if not b:
        tt = '순위 밖 또는 데이터 없음'
        st.write(f'을지로3가 와인 : {tt}')
    else:
        tt = b[0]
        st.write(f'을지로3가 와인 : {tt}위')
    if not c:
        tt = '순위 밖 또는 데이터 없음'
        st.write(f'을지로3가 위스키 : {tt}')
    else:
        tt = c[0]
        st.write(f'을지로3가 위스키 : {tt}위')
    if not d:
        tt = '순위 밖 또는 데이터 없음'
        st.write(f'을지로3가 술집 : {tt}')
    else:
        tt = d[0]
        st.write(f'을지로3가 술집 : {tt}위')

main_rank(tt)

st.divider()
# 메인화면 순위 컬럼 
st.header('플레이스 1~5순위')

# 각 키워드별 데이터프레임 생성 및 열 이름 변경
df1 = df.loc[(df['keyword'] == '을지로3가 맛집') & (df['date_only'] == option), ['rank', 'title']].rename(columns={'title': '을지로3가 맛집'})
df2 = df.loc[(df['keyword'] == '을지로3가 와인') & (df['date_only'] == option), ['rank', 'title']].rename(columns={'title': '을지로3가 와인'})
df3 = df.loc[(df['keyword'] == '을지로3가 위스키') & (df['date_only'] == option), ['rank', 'title']].rename(columns={'title': '을지로3가 위스키'})
df4 = df.loc[(df['keyword'] == '을지로3가 술집') & (df['date_only'] == option), ['rank', 'title']].rename(columns={'title': '을지로3가 술집'})

# 'rank'를 기준으로 병합
merged_df = df1.merge(df2, on='rank', how='outer')\
               .merge(df3, on='rank', how='outer')\
               .merge(df4, on='rank', how='outer')

# 'rank' 기준으로 정렬하고 인덱스로 설정
merged_df = merged_df.sort_values(by='rank').set_index('rank')

# 정렬된 데이터프레임 출력
# st.write("랭크 기준 가로 정렬된 데이터프레임:")
st.dataframe(merged_df)
