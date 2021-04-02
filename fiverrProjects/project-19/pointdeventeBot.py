from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from scrapy import Selector
import os
import time
import csv


#-- Writing Data to a CSV file --#
def writeCSV(data, fieldName, file_name):
	fileExists = os.path.isfile(file_name)
	with open(file_name, 'a', encoding='utf-8') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
		if not fileExists:
			writer.writeheader()
		writer.writerow(data)

#-- Initializing the chrome driver --#
def initChromeDriver():
    chrome_options = webdriver.ChromeOptions()
    # prefs = {"download.default_directory" : "/some/path"}
    # chromeOptions.add_experimental_option("prefs",prefs)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # driver = webdriver.Chrome(os.environ.get('chromedriver'), chrome_options=chrome_options) 
    driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
    
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver



if __name__ == "__main__":

    FIELD_NAMES = ['City', 'Price', 'Rent', 'Area', 'Ref', 'Formula', 'link']
    curr_page = 1

    driver = initChromeDriver()
    driver.maximize_window()
    driver.get("https://www.pointdevente.fr/fr/murs-de-boutique-occupes/murs-de-boutique/lf_10")
    
    while True:
        time.sleep(3)

        html = driver.page_source
        respObj = Selector(text=html)

        cards = respObj.xpath("//div[contains(@class, 'block-card-detail')]")
        for card in cards:

            rent = card.xpath("normalize-space(.//li[contains(text(), 'Loyer')]/span/strong/text())").get()
            if rent:
                rent = int("".join(i for i in rent if i.isdigit()))
            
            price = card.xpath("normalize-space(.//span[@class='price']/text())").get()
            if price:
                price = int("".join(i for i in price if i.isdigit()))

            formulae = None
            if rent and price:
                formulae = f"{round(((rent * 12) / price) * 100, 2)}%"

            dataDict = {
                FIELD_NAMES[0]: f'''{card.xpath("normalize-space(.//div[@class='address']/text())").get()}{card.xpath("normalize-space(.//div[@class='address']/sup/text())").get()}''',
                FIELD_NAMES[1]: price,
                FIELD_NAMES[2]: rent,
                FIELD_NAMES[3]: card.xpath("normalize-space(.//li[contains(text(), 'Surface')]/span/strong/text())").get(),
                FIELD_NAMES[4]: card.xpath("normalize-space(.//div[@class='ref']/text())").get().replace("Réf.",""),
                FIELD_NAMES[5]: formulae,
                FIELD_NAMES[6]: card.xpath(".//a/@href").get(),
            }
            print(dataDict)
            writeCSV(dataDict, FIELD_NAMES, 'data.csv')

        #-- Handling Pagination --#
        curr_page += 1
        try:
            nextPageBtn = driver.find_element_by_xpath(f"(//span[@class='pagination-numbers'])[last()]/a[text()='{curr_page}']")
            driver.execute_script("arguments[0].click()", nextPageBtn)
        except:
            break

    driver.quit()
