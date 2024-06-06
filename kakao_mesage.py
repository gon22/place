import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time
from PyKakao import Message


service_key = os.getenv("SERVICE_KEY")
login_id = os.getenv("LOGIN_ID")
login_password = os.getenv("LOGIN_PASSWORD")

# API 설정
API = Message(service_key=service_key)
auth_url = API.get_url_for_generating_code()
print(auth_url)

# Selenium을 이용하여 웹 브라우저 자동화
# driver = webdriver.Chrome()



# ChromeDriverManager를 사용하여 크롬 드라이버 설치 경로를 가져옵니다
service = Service(ChromeDriverManager().install())

# ChromeOptions 객체 생성
options = Options()

# 드라이버 인스턴스를 생성할 때 Service와 Options를 전달합니다
driver = webdriver.Chrome(service=service, options=options)
driver.get(auth_url)

# 아이디 입력창
id = driver.find_element(By.CSS_SELECTOR, "#loginId--1")

# 클릭하도록 설정
id.click()

# 키보드 입력 설정
id.send_keys(login_id)

# 비밀번호 입력창 찾기
pw = driver.find_element(By.CSS_SELECTOR, "#password--2")
# 클릭하도록 설정
pw.click()
# 키보드 입력 설정
pw.send_keys(login_password)

# 로그인 버튼 클릭
login_btn = driver.find_element(By.CSS_SELECTOR, ".btn_g.highlight.submit")
login_btn.click()

# 사용자 입력 대기 (로그인)
time.sleep(5)  # 로그인 시간을 충분히 줍니다. 필요에 따라 조정하세요.

# 로그인 후 리다이렉트된 URL을 가져옴
redirected_url = driver.current_url
print(redirected_url)

code = redirected_url.split('code=')

# 브라우저 종료
driver.quit()

# Access Token
access_token = API.get_access_token_by_redirected_url('code=' + "".join(code[1]))
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