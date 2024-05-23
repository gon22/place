{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "a622a4c1-6295-4ca9-8741-e020a9b2fe43",
   "metadata": {},
   "outputs": [],
   "source": [
    "from requests_html import HTMLSession\n",
    "\n",
    "import urllib.request\n",
    "import json\n",
    "import pandas as pd\n",
    "import datetime as dt\n",
    "import chardet\n",
    "import encodings\n",
    "import re\n",
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "98095b7b-2a20-4319-9eee-f5225a0fe937",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 디렉토리 생성하기\n",
    "save_directory = \"./naver_place\" \n",
    "if not os.path.exists(save_directory):\n",
    "    os.makedirs(save_directory)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "94a8c48c-1d49-40ec-9949-a827793e1f35",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "client_id = \"K25hzGPrWL8hskBSJWND\"\n",
    "client_secret = \"SSKeYoapXo\"\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "475f4df6-785d-4902-abdf-861ef002349a",
   "metadata": {},
   "outputs": [],
   "source": [
    "# ,'경기','인천','강원','충청','대전','세종','전라','광주','경상','대구','부산','제주'\n",
    "regions='서울'\n",
    "client_id = \"K25hzGPrWL8hskBSJWND\"\n",
    "client_secret = \"SSKeYoapXo\"\n",
    "query = ['을지로3가 맛집','을지로3가 와인','을지로3가 위스키', '을지로3가 술집']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "e6bfbcc0-95a5-40dd-ae4c-524bbe84b78c",
   "metadata": {},
   "outputs": [],
   "source": [
    "def place_top5(client_id, client_secret, query, *regions):\n",
    "    regions = list(regions)\n",
    "    query = query\n",
    "    result_list=[]\n",
    "    for region in regions:\n",
    "        for q in query:\n",
    "            region_query = region + ' ' + q\n",
    "            encText = urllib.parse.quote(region_query)\n",
    "            url = \"https://openapi.naver.com/v1/search/local.json?query=\" + encText + \\\n",
    "                    \"&display=50\"\n",
    "        \n",
    "            request = urllib.request.Request(url)\n",
    "            request.add_header(\"X-Naver-Client-Id\",client_id)\n",
    "            request.add_header(\"X-Naver-Client-Secret\",client_secret)\n",
    "            response = urllib.request.urlopen(request)\n",
    "            rescode = response.getcode()\n",
    "            \n",
    "            #print(query)\n",
    "            if(rescode==200):\n",
    "                response_body = response.read()\n",
    "                results = json.loads(response_body)['items']\n",
    "                \n",
    "                for i, result in enumerate(results):\n",
    "                    # print(i+1)\n",
    "                    result['rank'] = i+1\n",
    "                    result['search'] = q\n",
    "                    result['region']=region\n",
    "                    result['title']=result['title'].replace('<b>','').replace('</b>','')\n",
    "                    result['date'] = dt.datetime.now()\n",
    "                    result_list.append(result)\n",
    "            else:\n",
    "                print(\"Error Code:\" + rescode)\n",
    "                  \n",
    "    df=pd.DataFrame(result_list)\n",
    "    return df\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "1a33bc45-1c35-4f9a-9cfd-98cbb294bf47",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = place_top5(client_id, client_secret, query, regions)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "1e1ee7cf-db89-4c31-80c0-2e5b987d2d1b",
   "metadata": {},
   "outputs": [],
   "source": [
    "df['year'] = df['date'].dt.year\n",
    "df['month'] = df['date'].dt.month\n",
    "df['day'] = df['date'].dt.day"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "18072784-5806-4793-9423-62d39d72adb6",
   "metadata": {},
   "outputs": [],
   "source": [
    "# csv에 보여줄 내용\n",
    "place = df[['search','rank','title','year','month','day']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "2f38804a-7784-4eac-8339-4b7831edecfe",
   "metadata": {},
   "outputs": [],
   "source": [
    "# adress = \"C:\\\\Users\\\\kwakyonghyen\\\\Desktop\\\\keyword_rank_top5\"\n",
    "file_path = 'naver_place/keyword_rank_top5test1.csv'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "a039cc2a-9ec6-4377-97e7-620276827c01",
   "metadata": {},
   "outputs": [],
   "source": [
    "# place.to_csv(file_path, mode='a', header=True, index=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "44a30da7-0cd7-437e-8c1a-baa5e2f00a8c",
   "metadata": {},
   "outputs": [],
   "source": [
    "if os.path.exists(file_path):\n",
    "    place.to_csv(file_path, mode='a', header=False, index=False, encoding='utf8')\n",
    "else:\n",
    "    place.to_csv(file_path, mode='w', header=True, index=False, encoding='utf8')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "d2dbdeb5-12ad-4779-9ffa-cb6045b1ef48",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
