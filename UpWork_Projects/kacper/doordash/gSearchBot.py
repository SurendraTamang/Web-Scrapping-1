from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium_stealth import stealth
import os
import pandas as pd
from urllib.parse import unquote
import csv


df = pd.read_excel("/root/doordash/splitData.xlsx")
try:
    df1 = pd.read_csv("/root/doordash/data_41_60k.csv")
    idList = df1['Id'].values.tolist()
except:
    idList = []

def extractUrl(rawUrl):
    try:
        url = rawUrl.split("&url=")[-1].split("&")[0]
        return unquote(url).split("?utm_source=")[0]
    except:
        return None

def writeCSV(data, fieldName):
    fileExists = os.path.isfile("/root/doordash/data_41_60k.csv")
    with open("/root/doordash/data_41_60k.csv", 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
        if not fileExists:
            writer.writeheader()
        writer.writerow(data)


#CHROMEDRIVERPATH = os.environ.get("chromedriver")
CHROMEDRIVERPATH = ("/root/chromedriver")
FIELD_NAMES = ['Id', 'City', 'Area', 'Restaurant Name', 'Average Rating', 'Number Of Reviews', 'Search Queries', 'Website', 'Phone']
cntr = 0

options = Options()
options.headless = True
options.add_argument("start-maximized")
options.add_argument("--no-sandbox")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(CHROMEDRIVERPATH, chrome_options=options)
#driver.maximize_window()
#driver.set_window_size(1920, 1080)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

for _,val in df.iterrows():
    cntr += 1      

    if val['Id'] not in idList:
        idList.append(val['Id'])
        driver.get(f"https://www.google.com/search?q={val['gSearchQuery']}")
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a")))

        html = driver.page_source
        respObj = Selector(text=html)

        website = respObj.xpath("//div[text()='Website']/parent::a/@href").get()
        phone = respObj.xpath("normalize-space(//span[contains(@aria-label, 'phone number')]/text())").get()

        if not website:
            website = respObj.xpath("//div[text()='Website']/parent::div/parent::a/@href").get()
        if not phone:
            phone = respObj.xpath("normalize-space(//span[contains(@aria-label, 'Phone Number')]/text())").get()
        if not phone:
            phone = respObj.xpath("normalize-space((//div[text()='Website']/parent::div/parent::a/preceding-sibling::a)[1]//span[contains(@class,'details')]/div[2]/span[last()]/text())").get()
        if not phone:    
            phone = respObj.xpath("normalize-space((//div[text()='Website']/parent::div/parent::a/preceding-sibling::a)[1]//span[contains(@class,'details')]/div[3]/span[last()]/text())").get()
        if not phone:
            phone = respObj.xpath("normalize-space(//div[text()='A']/parent::div/span/div[2]/span[last()]/text())").get()
        data = {
            FIELD_NAMES[0]: val['Id'],
            FIELD_NAMES[1]: val['State'],
            FIELD_NAMES[2]: val['City'],
            FIELD_NAMES[3]: val['Restaurant name'],
            FIELD_NAMES[4]: val['Average rating'],
            FIELD_NAMES[5]: val['Number of reviews'],
            FIELD_NAMES[6]: val['gSearchQuery'],
            FIELD_NAMES[7]: extractUrl(website),
            FIELD_NAMES[8]: phone
        }
        print(data,"\n")
        writeCSV(data, FIELD_NAMES)

        if cntr % 1000 == 0:
            driver.quit()
            time.sleep(random.randint(80,180))

            options = Options()
            options.headless = True
            options.add_argument("start-maximized")
            options.add_argument("--no-sandbox")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(CHROMEDRIVERPATH, chrome_options=options)
            #driver.maximize_window()
            #driver.set_window_size(1920, 1080)

            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )
