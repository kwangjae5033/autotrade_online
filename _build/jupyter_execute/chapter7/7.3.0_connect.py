#!/usr/bin/env python
# coding: utf-8

# ## 서비스 연결

# API 요청을 하기 위해 requests 와 json 패키지를 불러줍니다. 
# requests 패키지는 HTTP 요청을 보낼 때, json 은 수신 받은 객체를 JSON 데이터로 만들어서 쓰기 위해 활용되는 모듈입니다.
# 참고로 JSON 데이터는 pandas 데이터프레임으로 변환하기 쉬운 이점도 있습니다.

# In[ ]:


import requests 
import json


# requests 는 크게 GET 방식과 POST 방식이 있습니다. GET 방식은 현재가 혹은 주식 잔고조회 같은 요청에서 쓰이고, POST 방식은 주로 주문/정정/취소 요청에서 쓰입니다.

# In[ ]:


"""주식 종목 현재가 조회"""

# 다음 장에서 더 자세히 설명 드립니다. 
# requests.get() 함수의 구성 요소를 집중적으로 봐주세요 (e.g. URL, headers, params)

URL_BASE = "https://openapi.koreainvestment.com:9443" # 실전 투자
PATH = "uapi/domestic-stock/v1/quotations/inquire-price" # 현재가 조회를 위한 URL 경로
URL = f"{URL_BASE}/{PATH}""
code = "005930" # 삼성전자 종목 코드

headers = {
    "Content-Type":"application/json",
    "authorization": f"Bearer {ACCESS_TOKEN}", # 보안인증키
    "appKey":APP_KEY, # API 신청으로 발금 받은 Key
    "appSecret":APP_SECRET, # API 신청으로 발금 받은 Secret
    "tr_id":"FHKST01010100" # 현재가 조회를 위한 id
}
params = {
    "fid_cond_mrkt_div_code":"J", # J: 주식
    "fid_input_iscd":code, # 조회 하고 싶은 주식 종목의 코드 ex) 삼성전자: 005930
}

res = requests.get(URL, headers=headers, params=params) # <<<<<<<<<

print(int(res.json()['output']['stck_prpr']))


# 상대적으로 보안이 중요한 POST 는 hashkey 를 활용해 암호화를 진행합니다. 

# In[ ]:


"""주식 시장가 매수"""

# 다음 장에서 더 자세히 설명 드립니다. 
# requests.post() 함수의 구성 요소를 집중적으로 봐주세요 (e.g. URL, headers, data)

URL_BASE = "https://openapi.koreainvestment.com:9443" # 실전 투자
PATH = "uapi/domestic-stock/v1/trading/order-cash" # cash 주문
URL = f"{URL_BASE}/{PATH}"
code = "005930" # 삼성전자 종목 코드
data = {
    "CANO": CANO, # 계좌번호 앞자리
    "ACNT_PRDT_CD": ACNT_PRDT_CD,  # 계좌번호 뒷자리
    "PDNO": code,
    "ORD_DVSN": "01", # 시장가
    "ORD_QTY": str(int(qty)), # 매수 주문 수량
    "ORD_UNPR": "0", # 시장가로 매수 시, ORD_UNPR 는 0 (지정가로 매수 시, ORD_UNPR 는 원하는 지정가로 명시) 
}
headers = {"Content-Type":"application/json",
    "authorization":f"Bearer {ACCESS_TOKEN}", # 보안인증키
    "appKey":APP_KEY,  # API 신청으로 발금 받은 Key
    "appSecret":APP_SECRET, # API 신청으로 발금 받은 Secret
    "tr_id":"TTTC0802U", # 매수 주문을 위한 id
    "custtype":"P", # P: 개인 
    "hashkey" : hashkey(data)
}

res = requests.post(URL, headers=headers, data=json.dumps(data)) # <<<<<<<<<


# 해쉬키 함수는 다음과 같이 정의 되어 있습니다.

# In[ ]:


def hashkey(datas):
    """암호화"""
    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
    'content-Type' : 'application/json',
    'appKey' : APP_KEY,
    'appSecret' : APP_SECRET,
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]
    return hashkey


# 위 예제 코드의 GET 과 POST 방식 모두 headers 에서 ACCESS_TOKEN 을 필요로 하는데, get_access_token() 함수에서 APP_KEY 와 APP_SECRET 를 이용해서 발급 받을 수 있습니다. 

# In[ ]:


def get_access_token():
    """토큰 발급"""
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
    "appkey":APP_KEY,
    "appsecret":APP_SECRET}
    PATH = "oauth2/tokenP"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"]
    return ACCESS_TOKEN


# 현재가 조회와 매수 주문 코드 예제를 보면서 GET 과 POST 호출 방식의 비슷한 점들을 발견하셨을 겁니다. 
# requests.get() 과 reqeusts.post() 모두 URL, headers, 그리고 params 혹은 data 파라미터가 필요합니다.
# 결국 요청의 목적에 따라서 URL 의 PATH 변수, headers 딕셔너리의 key 값, 그리고 params 혹은 data 딕셔너리의 key 값들을 교체 해주면 성공적으로 요청 작업을 완료 할 수 있습니다.
# 요청에 따른 인자 값 변경은 KIS developers 홈페이지에서 (https://apiportal.koreainvestment.com/) 더 자세한 정보를 확인할 수 있습니다.
# 한편, headers 와 data 에서 반복적으로 사용되는 개인 정보들은 config.yaml 파일에 일괄적으로 저장 해두면 훨씬 더 간결한 코드를 작성 하실 수 있습니다.

# In[ ]:


"""config.yaml 파일 생성"""

#홈페이지에서 API서비스 신청시 받은 Appkey, Appsecret 값 설정
APP_KEY: "xxxxxxxxxxxxxxxxxxxxxxx"
APP_SECRET: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

#계좌번호 앞 8자리
CANO: "xxxxxxxx"
#계좌번호 뒤 2자리
ACNT_PRDT_CD: "01"

#실전투자
URL_BASE: "https://openapi.koreainvestment.com:9443"
#모의투자
# URL_BASE: "https://openapivts.koreainvestment.com:29443"

#디스코드 웹훅 URL
DISCORD_WEBHOOK_URL: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

