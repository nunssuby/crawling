from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

page = 1
max_pages = 50  # ✅ 안전을 위해 최대 페이지 수 설정 (필요시 조절)

while page <= max_pages:
    url = f"https://www.mwcbarcelona.com/exhibitors?page={page}"
    print(f"📄 Page {page} 크롤링 중...")

    driver.get(url)
    
    # 쿠키 팝업은 1페이지만 처리
    if page == 1:
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
        except:
            pass

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.exhibitor-listing > a"))
        )
        cards = driver.find_elements(By.CSS_SELECTOR, "ul.exhibitor-listing > a")
    except:
        print(f"❌ Page {page}: 카드 없음 → 종료")
        break

    if not cards:
        print(f"❌ Page {page}: 카드 없음 → 종료")
        break

    for card in cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, ".ais-Highlight-nonHighlighted").text.strip()
        except:
            name = "N/A"

        try:
            booth = card.find_element(By.CSS_SELECTOR, ".whitespace-nowrap").text.strip()
        except:
            booth = "N/A"

        try:
            badges = [b.text.strip() for b in card.find_elements(By.CSS_SELECTOR, ".badges span")]
        except:
            badges = []

        try:
            link = card.get_attribute("href")
        except:
            link = "N/A"

        print(f"🔹 {name}")
        print(f"   🏷 Booth: {booth}")
        print(f"   🏅 Badges: {', '.join(badges)}")
        print(f"   🔗 Link: {link}")
        print("---")

    page += 1
    time.sleep(1)  # ⏱️ 페이지 간 대기 (예의상)

driver.quit()
