from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

all_data = []
page = 1
max_pages = 2  # 필요 시 조정

while page <= max_pages:
    url = f"https://www.mwcbarcelona.com/exhibitors?page={page}"
    print(f"📄 Page {page} 크롤링 중...")

    driver.get(url)

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
            name = ""

        try:
            booth = card.find_element(By.CSS_SELECTOR, ".whitespace-nowrap").text.strip()
        except:
            booth = ""

        try:
            badges = [b.text.strip() for b in card.find_elements(By.CSS_SELECTOR, ".badges span")]
        except:
            badges = []

        try:
            link = card.get_attribute("href")
        except:
            link = ""

        all_data.append({
            "Company Name": name,
            "Booth Info": booth,
            "Badges": ", ".join(badges),
            "Link": link
        })

    page += 1
    time.sleep(1)

driver.quit()

# ✅ pandas로 CSV 저장
df = pd.DataFrame(all_data)
df.to_csv("mwc_exhibitors.csv", index=False, encoding="utf-8-sig")

print("✅ CSV 저장 완료: mwc_exhibitors.csv")
