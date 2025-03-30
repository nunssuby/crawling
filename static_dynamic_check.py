import requests
from bs4 import BeautifulSoup

# 테스트용 URL (필요시 다른 전시회 사이트로 변경)
url = "https://expo.semi.org/korea2025/Public/exhibitors.aspx?ID=29169"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # SSL 인증 무시
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    html = response.text

    print("[1] 응답 상태 코드:", response.status_code)

    # BeautifulSoup 파싱
    soup = BeautifulSoup(html, "html.parser")

    # 주요 콘텐츠 확인: 예) 기업 리스트 테이블 행 수
    rows = soup.select("div.listTableBody table tr")
    print(f"[2] 추출한 <tr> 행 개수: {len(rows)}")

    # 첫 번째 행이 있다면 출력
    if rows:
        print("[3] 첫 번째 기업 정보:")
        print(rows[0].prettify())
    else:
        print("[3] 기업 정보를 찾지 못했습니다. (정적 크롤링 불가능일 수 있음)")

except requests.exceptions.RequestException as e:
    print("요청 중 오류 발생:", e)