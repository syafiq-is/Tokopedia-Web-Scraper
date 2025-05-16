import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

URL = "https://www.tokopedia.com/search?st=&q=elektronik&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
PAGE_COUNT = 20

driver = webdriver.Chrome()
driver.get(URL)

# Data containers
produk_names = []
harga_values = []
rating_values = []


def progressive_scroll(pause=1, steps=30, delay_between_scrolls=0.3):
    for step in range(steps):
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_position = (scroll_height // steps) * (step + 1)
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(delay_between_scrolls)
    time.sleep(pause)  # Wait at the end


# Scrape pages
for page in range(PAGE_COUNT):
    print(f"🔃 Scraping page {page + 1}...")

    # Let the page render
    # Wait for product container to appear
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "css-5wh65g"))
        )
        print("✅ Elements loaded.")
    except Exception as e:
        print(f"❌ Timeout waiting for elements: {e}")

    time.sleep(2)  # Just to be sure wait for 2 seconds

    # SCROLL TO LOAD MORE
    print(f"🔃 Scrolling down...")
    progressive_scroll(pause=2, steps=50, delay_between_scrolls=0.2)
    print(f"✅ Scrolling finished")

    # Start Scraping page
    print(f"🔃 Parsing HTML...")
    soup = BeautifulSoup(driver.page_source, "html.parser")

    containers = soup.find_all("div", class_="css-5wh65g")
    for item in containers:
        nama_produk = item.find("span", class_="_0T8-iGxMpV6NEsYEhwkqEg==")
        harga = item.find("div", class_="_67d6E1xDKIzw+i2D2L0tjw==")
        rating = item.find("span", class_="_9jWGz3C-GX7Myq-32zWG9w==")

        produk_names.append(nama_produk.text if nama_produk else None)
        harga_values.append(harga.text if harga else None)
        rating_values.append(rating.text if rating else None)

    print(f"✅ Finished parsing HTML")

    print(f"✅ Finished Scraping page {page + 1}...")

    # Try to click next button
    try:
        # Wait until both buttons are present
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "css-dzvl4q-unf-pagination-item")
            )
        )

        time.sleep(2)  # Just to be sure wait for 2 seconds

        # In tokopedia there is two element with this class name [previous_button, next_button] we use te buttons[1]
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", buttons[1]
        )

        buttons[1].click()

        print("➡️ Clicked the 'Next Page' button")
    except Exception as e:
        print(f"❌ Error clicking the next button: {e}")
        break

time.sleep(2)

# Create DataFrame
df = pd.DataFrame(
    {"Produk": produk_names, "Harga": harga_values, "Rating": rating_values}
)

print("\n📊 Hasil Scraping:")
print(df.head(100))

df.to_csv("tokopedia_produk_scraper.csv", index=False)
print("✅ Data saved to 'tokopedia_produk.csv'")

driver.close()
