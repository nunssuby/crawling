import requests
import pandas as pd

# 인증키

# API 요청 URL
url = "https://kosis.kr/openapi/Param/statisticsParameterData.do"

params = {
    "method": "getList",
    "apiKey": api_key,
    "itmId": "T001+T002+T003+T004+",
    "objL1": "ALL",
    "objL2": "ALL",
    "objL3": "",
    "objL4": "",
    "objL5": "",
    "objL6": "",
    "objL7": "",
    "objL8": "",
    "format": "json",
    "jsonVD": "Y",
    "prdSe": "Y",  # 연도 기준
    "newEstPrdCnt": 3,  # 최근 3개년
    "orgId": "430",  # 통계표 소속기관
    "tblId": "DT_430001_09_001"  # 테이블 ID
}

# 데이터 요청
response = requests.get(url, params=params)

# 결과 확인
if response.status_code == 200:
    data = response.json()
    print("✅ 데이터 수신 완료")
    
    # 데이터프레임 변환
    df = pd.DataFrame(data)
    print(df.head())

    # CSV 저장
    df.to_csv("kosis_data.csv", index=False, encoding="utf-8-sig")
    print("📁 'kosis_data.csv' 로 저장 완료")
else:
    print(f"❌ 오류 발생. 상태코드: {response.status_code}")