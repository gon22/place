
import os
from requests_html import HTMLSession
import urllib.request
import json
import pandas as pd
import datetime as dt
import chardet
import encodings
import re

# 디렉토리 생성하기
save_directory = "./naver_place" 
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")


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
                    result['date'] = dt.datetime.now()
                    result_list.append(result)
            else:
                print("Error Code:" + rescode)
                
    df = pd.DataFrame(result_list)
    return df

df = place_top5(client_id, client_secret, query, regions)

# 연도, 월, 일 추출
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

# 시간 정보 추출
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute
df['second'] = df['date'].dt.second

# 날짜 요약
df['date_summary'] = df['date'].dt.date

# 시간 요약 (hh:mm:ss)
df['time_summary'] = df['date'].dt.time


# csv에 보여줄 내용
place = df.copy()


# 파일 경로 설정
file_path = 'naver_place/keyword_rank_top5test1.csv'

if os.path.exists(file_path):
    place.to_csv(file_path, mode='a', header=False, index=False, encoding='utf8')
else:
    place.to_csv(file_path, mode='w', header=True, index=False, encoding='utf8')



# 카카오 메시지 알림 - 르템플 순위 변동
