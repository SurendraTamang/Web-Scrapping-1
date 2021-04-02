from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import os
import csv
import time
import pandas as pd
from scrapy import Selector
import random


def writeCSV(data, fieldName, file_name):
    fileExists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
        if not fileExists:
            writer.writeheader()
        writer.writerow(data)

def initChromeDriver():
    chrome_options = webdriver.ChromeOptions()
    # prefs = {"download.default_directory" : "/some/path"}
    # chromeOptions.add_experimental_option("prefs",prefs)
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(os.environ.get('chromedriver'), chrome_options=chrome_options)
    # driver = webdriver.Chrome('../chromedriver',chrome_options=chrome_options)
    
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver

driver = initChromeDriver()
driver.maximize_window()

df = pd.read_csv('linksBK.csv')
driver.get("https://www.biv.be/de-vastgoedmakelaar/alle-vastgoedmakelaars-vind-je-hier?keys=&location=1050&city=")
time.sleep(5)
loginBtnElem = driver.find_element_by_xpath("//button[contains(text(), 'ik ga akkoord')]")
driver.execute_script("arguments[0].click()", loginBtnElem)

for _,val in df.iterrows():
    driver.get(val['Url'])
    WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//h1")))
    time.sleep(3)

    # loginBtnElem = driver.find_element_by_xpath("//button[contains(text(), 'ik ga akkoord')]")
    # driver.execute_script("arguments[0].click()", loginBtnElem)
    # time.sleep(1)

    html = driver.page_source
    respObj = Selector(text=html)

    FIELD_NAMES = ['Name', 'Erkend als', 'Company Name', 'Street', 'House Number', 'Postal Code', 'Locality', 'Email', 'Source Url']

    dataDict = {
        FIELD_NAMES[0]: respObj.xpath("normalize-space(//h1/text())").get(),
        FIELD_NAMES[1]: ",".join(i.strip() for i in respObj.xpath("//h3[contains(text(), 'Erkend')]/following-sibling::div/text()").getall() if i.strip()),
        FIELD_NAMES[2]: respObj.xpath("normalize-space(//div[contains(@class, 'company-name')]//div/text())").get(),
        FIELD_NAMES[3]: respObj.xpath("normalize-space(//span[contains(@class, 'street')]/text())").get(),
        FIELD_NAMES[4]: respObj.xpath("normalize-space(//span[contains(@class, 'house-number')]/text())").get(),
        FIELD_NAMES[5]: respObj.xpath("normalize-space(//span[contains(@class, 'postal-code')]/text())").get(),
        FIELD_NAMES[6]: respObj.xpath("normalize-space(//span[contains(@class, 'locality')]/text())").get(),
        FIELD_NAMES[7]: respObj.xpath("normalize-space(//a[contains(@href, 'mail')]/text())").get(),
        FIELD_NAMES[8]: driver.current_url,
    }
    print(dataDict)

    writeCSV(dataDict, FIELD_NAMES, "data.csv")

    # time.sleep(random.randint(5,10))
    
    # driver.quit()
    # time.sleep(15)
    # driver = initChromeDriver()
    # driver.maximize_window()
driver.quit()
