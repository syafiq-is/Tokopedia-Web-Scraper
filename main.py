import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Logger import Logger

# User Variable
URL = "https://www.tokopedia.com"
OUTPUT_FILES = "tokopedia_produk_scraper.csv"

# System Variable
ELEM_PAGE_NAV = "css-dzvl4q-unf-pagination-item"
ELEM_PRODUCT_CONTAINER = "css-5wh65g"

# Data containers
products = {
    "titles": [],
    "prices": [],
    "real_prices": [],
    "discounts": [],
    "ratings": [],
    "solds": [],
    "sellers": [],
    "badges": [],
}

# Initiate Logger for easier debugging
log = Logger("my_log.txt")
log.clear()  # Clear log every run

# Open a webdriver
driver = webdriver.Chrome()
driver.get(URL)


def scrape_page():
    log.info("Scraping page...")
    log.info("Parsing HTML...")

    soup = BeautifulSoup(driver.page_source, "html.parser")

    containers = soup.find_all("div", class_=ELEM_PRODUCT_CONTAINER)
    for item in containers:
        title = item.find("span", class_="_0T8-iGxMpV6NEsYEhwkqEg==")
        price = item.find("div", class_="_67d6E1xDKIzw+i2D2L0tjw==")
        real_price = item.find("span", class_="q6wH9+Ht7LxnxrEgD22BCQ==")
        discount = item.find("span", class_="vRrrC5GSv6FRRkbCqM7QcQ==")
        rating = item.find("span", class_="_9jWGz3C-GX7Myq-32zWG9w==")
        sold = item.find("span", class_="se8WAnkjbVXZNA8mT+Veuw==")
        seller = item.find("span", class_="T0rpy-LEwYNQifsgB-3SQw==")
        badge_img = item.find("img", alt="shop badge")
        if badge_img:
            badge_src = badge_img.get("src", "")
            if "official_store_badge" in badge_src:
                badge = "Official Store"
            elif "goldmerchant" in badge_src or "PM%20Pro%20Small" in badge_src:
                badge = "Power Merchant"
        else:
            badge = "No Badge"

        products["titles"].append(title.text if title else None)
        products["prices"].append(price.text if price else None)
        products["real_prices"].append(real_price.text if real_price else price.text)
        products["discounts"].append(discount.text if discount else "0%")
        products["ratings"].append(rating.text if rating else None)
        products["solds"].append(sold.text if sold else None)
        products["sellers"].append(seller.text if seller else None)
        products["badges"].append(badge)

    log.success("Finished parsing HTML")
    log.success(f"Finished Scraping page")


# Main Scraper
if __name__ == "__main__":
    log.info("Please search for anything")
    log.info("Than, scroll the page until all the products you want is Loaded")

    input("Enter any value to start scraping: ")

    scrape_page()

    # Store Data to CSV
    df = pd.DataFrame(products)
    df.to_csv(OUTPUT_FILES, index=False)
    log.success(f"Data saved to {OUTPUT_FILES}")

    driver.close()
