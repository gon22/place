
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

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['date_summary'] = df['date'].dt.date


# csv에 보여줄 내용
place = df.copy()

# 파일 경로 설정
file_path = 'naver_place/keyword_rank_top5test1.csv'

if os.path.exists(file_path):
    place.to_csv(file_path, mode='a', header=False, index=False, encoding='utf8')
else:
    place.to_csv(file_path, mode='w', header=True, index=False, encoding='utf8')



# 카카오 메시지 알림 - 르템플 순위 변동

from PyKakao import Message

API = Message(service_key = "535beb56f41f8c1d92b5f87300a2fd96")

auth_url = API.get_url_for_generating_code()
print(auth_url)

url = "https://localhost:5000/?code=UdjtRSsSWGshH1tMhOR3JGAyqZCbJUFQCr35RDkndNZPHXAkFH6H5gAAAAQKKcjZAAABj8V4ux62xj-RG-1vuA"

access_token = API.get_access_token_by_redirected_url(url)
API.set_access_token(access_token)

# 메시지 유형 - 피드
message_type = "feed"

# 파라미터
content = {
            "title": "오늘의 디저트",
            "description": "아메리카노, 빵, 케익",
            "image_url": "https://mud-kage.kakao.com/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
                "android_execution_params": "contentId=100",
                "ios_execution_params": "contentId=100"
            }
        }

item_content = {
            "profile_text" :"Kakao",
            "profile_image_url" :"https://mud-kage.kakao.com/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png",
            "title_image_url" : "https://mud-kage.kakao.com/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png",
            "title_image_text" :"Cheese cake",
            "title_image_category" : "Cake",
            "items" : [
                {
                    "item" :"Cake1",
                    "item_op" : "1000원"
                },
                {
                    "item" :"Cake2",
                    "item_op" : "2000원"
                },
                {
                    "item" :"Cake3",
                    "item_op" : "3000원"
                },
                {
                    "item" :"Cake4",
                    "item_op" : "4000원"
                },
                {
                    "item" :"Cake5",
                    "item_op" : "5000원"
                }
            ],
            "sum" :"Total",
            "sum_op" : "15000원"
        }

social = {
            "like_count": 100,
            "comment_count": 200,
            "shared_count": 300,
            "view_count": 400,
            "subscriber_count": 500
        }

buttons = [
            {
                "title": "웹으로 이동",
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net"
                }
            },
            {
                "title": "앱으로 이동",
                "link": {
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            }
        ]

API.send_message_to_me(
    message_type=message_type,
    content=content, 
    item_content=item_content, 
    social=social, 
    buttons=buttons
    )




