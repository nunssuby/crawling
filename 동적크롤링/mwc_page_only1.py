from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.mwcbarcelona.com/exhibitors?page=1")

# 쿠키 허용
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    ).click()
except:
    print("쿠키 팝업 없음 또는 이미 허용됨")

# 참가업체 카드가 로딩될 때까지 기다림
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.exhibitor-listing > a"))
)

# 카드 선택
cards = driver.find_elements(By.CSS_SELECTOR, "ul.exhibitor-listing > a")

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

driver.quit()
