import pyodide_http
import json
import datetime

pyodide_http.patch_all()  # Patch all libraries

import requests

vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

service_key = "aIsRditBsUScVGImZFHmF9Ks8mcHAdsVw1Pt6dqB1Eoum2lh0CBnDUX3lDb0S608y61RBcdJTKwLKH%2Ft%2BXVlrg%3D%3D"

today = datetime.datetime.today()
print(today)
base_date = "20230417"  # today.strftime("%Y%m%d") # "20200214" == 기준 날짜
print(base_date)
base_time = "2300"  # 날씨 값

# 인천 구월동
nx = "55"
ny = "124"

payload = "serviceKey=" + service_key + "&" + \
          "dataType=json" + "&" + \
          "base_date=" + base_date + "&" + \
          "base_time=" + base_time + "&" + \
          "nx=" + nx + "&" + \
          "ny=" + ny

pty_code = {"0": "없음", "1": "비", "2": "비/눈", "3": "눈", "4": "소나기", "5": "빗방울", "6": "빗방울/눈날림", "7": "눈날림"}

data = dict()
data['date'] = base_date
print(data)
weather = dict()

# 값 요청
res = requests.get(vilage_weather_url + payload)
try:
    items = res.json().get('response').get('body').get('items')

    for item in items['item']:
        # 기온
        if item['category'] == 'TMP':
            weather['tmp'] = item['fcstValue']

        # 강수상태
        if item['category'] == 'PTY':
            weather['code'] = item['fcstValue']
            weather['state'] = pty_code[item['fcstValue']]
except:
    print("날씨 정보 가져오기 실패 : ", res.text)

data['weather'] = weather
print(data['weather'])
print(data)


def get_pm10_state(pm10_value):
    if pm10_value < 30:
        pm10_state = "좋음"
    elif pm10_value < 80:
        pm10_state = "보통"
    elif pm10_value < 150:
        pm10_state = "나쁨"
    else:
        pm10_state = "매우 나쁨"

    return pm10_state


def get_pm25_state(pm25_value):
    if pm25_value < 15:
        pm25_state = "좋음"
    elif pm25_value < 35:
        pm25_state = "보통"
    elif pm25_value < 75:
        pm25_state = "나쁨"
    else:
        pm25_state = "매우 나쁨"

    return pm25_state


dust_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"

service_key = "aIsRditBsUScVGImZFHmF9Ks8mcHAdsVw1Pt6dqB1Eoum2lh0CBnDUX3lDb0S608y61RBcdJTKwLKH%2Ft%2BXVlrg%3D%3D"

sidoName = "인천"

payload = "serviceKey=" + service_key + "&" + \
          "returnType=json" + "&" + \
          "numOfRows=100" + "&" + \
          "pageNo=1" + "&" + \
          "sidoName=인천" + "&" + \
          "ver=1.0"

# pm10 pm2.5 수치 가져오기
res = requests.get(dust_url + payload)
result = res.json()
dust = dict()
if (res.status_code == 200) & (result['response']['header']['resultCode'] == '00'):
    dust['PM10'] = {'value': int(result['response']['body']['items'][0]['pm10Value'])}
    dust['PM2.5'] = {'value': int(result['response']['body']['items'][0]['pm25Value'])}
    # PM10 미세먼지 30 80 150
    pm10_value = dust.get('PM10').get('value')
    pm10_state = get_pm10_state(pm10_value)

    # PM2.5 초미세먼지 15 35 75
    pm25_value = dust.get('PM2.5').get('value')
    pm25_state = get_pm25_state(pm25_value)

    dust.get('PM10')['state'] = pm10_state
    dust.get('PM2.5')['state'] = pm25_state
else:
    print("미세먼지 가져오기 실패 : ", result['response']['header']['resultMsg'])

data['dust'] = dust
print(data['dust'])

import random  # 랜덤하게 음식 리스트 뽑기

rain_foods = "부대찌개,아구찜,해물탕,칼국수,수제비,짬뽕,우동,치킨,국밥,김치부침개,두부김치,파전".split(',')
pmhigh_foods = "콩나물국밥,고등어,굴,쌀국수,마라탕".split(',')


def get_foods_list(weather, dust_pm10, dust_pm20):
    if weather != '0':
        recommand_state = 'Case1'
        # random.sample(x, k=len(x)) 무작위로 리스트 섞기
        foods_list = random.sample(rain_foods, k=len(rain_foods))
    elif dust_pm10 == '매우나쁨' or dust_pm20 == '매우나쁨':
        recommand_state = 'Case2'
        foods_list = random.sample(pmhigh_foods, k=len(pmhigh_foods))
    else:
        recommand_state = 'Case3'
        foods_list = ['']

    return recommand_state, foods_list


def naver_local_search(query, display):
    # 네이버 애플리케이션의 client_id와 client_secret 키 설정
    headers = {
        "X-Naver-Client-Id": "SNA8wBH7IeZOY6d2Xz68",
        "X-Naver-Client-Secret": "gpAXis8weS"
    }

    # 지역 검색 요청 파라미터 설정
    params = {
        "sort": "comment",
        "query": query,
        "display": display
    }

    # 지역 검색 URL과 요청 파라미터
    naver_local_url = "https://openapi.naver.com/v1/search/local.json"

    # 지역 검색 요청
    res = requests.get(naver_local_url, headers=headers, params=params)

    # 지역 검색 결과 확인
    places = res.json().get('items')

    return places


# 경우 1 : 비/눈/소나기 => 비오는날 음식 3개 추천
# 경우 2 : 초/미세먼지 나쁨 이상 => 미세먼지에 좋은 음식 3개 추천
# 경우 3 : 정상 => 블로그 리뷰 순 맛집 추천
weather = data.get('weather').get('code')
dust_pm10 = data.get('dust').get('PM10').get("state")
dust_pm20 = data.get('dust').get('PM2.5').get("state")

# 날씨 상태와 음식 종류 선정
weather_state, foods_list = get_foods_list(weather, dust_pm10, dust_pm20)
print(weather_state)
print(foods_list)

# 위치는 사용자가 사용할 지역으로 변경 가능
location = "구월동"

# 추천된 맛집을 담을 리스트
recommands = []
for food in foods_list:
    # 지역 검색 요청 파라미터 설정
    # 만약, 날씨가 맑은 경우, food가 ''이므로, '문래동 맛집'이 된다.
    query = location + " " + food + " 맛집"

    # 맛집 검색 결과
    result_list = naver_local_search(query, 3)

    if len(result_list) > 0:
        if weather_state == 'Case3':  # Case3 처리 로직 : 맛집 검색 결과에서 가장 상위 3개를 가져옴
            recommands = result_list
            break
        else:  # Case1, Case2 처리 로직 : 해당 음식 검색 결과에서 가장 상위를 가져옴
            recommands.append(result_list[0])
    else:
        print("검색 결과 없음")  # 메뉴에 해당하는 맛집이 없을 수 있음

    if len(recommands) == 3:
        break

print(recommands)
