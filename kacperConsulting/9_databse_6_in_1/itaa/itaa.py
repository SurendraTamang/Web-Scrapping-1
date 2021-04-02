from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
import os
import csv
import time
import random
from scrapy import Selector
from itertools import combinations_with_replacement
from string import ascii_lowercase


pepIdLi = []
cmpIdLi = []
keywordLi = []
alphaLi = list(combinations_with_replacement([i for i in ascii_lowercase],3))

try:
    with open('people.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for indx,data in enumerate(csv_reader):
            if indx != 0:
                pepIdLi.append(data[-1])
                keywordLi.append(data[-2])
except:
    pass

try:
    with open('company.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for indx,data in enumerate(csv_reader):
            if indx != 0:
                cmpIdLi.append(data[-1])
except:
    pass

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
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # driver = webdriver.Chrome(os.environ.get('chromedriver'), chrome_options=chrome_options)
    driver = webdriver.Chrome('../chromedriver',chrome_options=chrome_options)
    
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
for alpha in alphaLi:
    if "".join(i for i in alpha) not in keywordLi:
        while True:
            try:
                driver.get("https://search.itaa.be/nl-nl")

                #-- Accepting Cookies --#
                try:
                    WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Accepteren']/parent::button")))
                    cookiesBtnElem = driver.find_element_by_xpath("//span[text()='Accepteren']/parent::button")
                    driver.execute_script("arguments[0].click()", cookiesBtnElem)
                except:
                    pass

                #-- Searching for Keywords --#
                search_box = driver.find_element_by_xpath("//input[@id='GeneralSearch']")
                search_box.send_keys("".join(i for i in alpha))
                search_box.send_keys(Keys.ENTER)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Zoekresultaten']")))

                html = driver.page_source
                respObj = Selector(text=html)

                peopleUrls = respObj.xpath("//div[@class='row']/div[contains(text(), 'personen')]/ul/li/a/@href").getall()
                companyUrls = respObj.xpath("//div[@class='row']/div[contains(text(), 'vennoots')]/ul/li/a/@href").getall()

                for pepUrl in peopleUrls:
                    if pepUrl.split("?Number=")[-1].split("&Source=")[0] not in pepIdLi:
                        driver.get(f'''https://search.itaa.be{pepUrl}''')
                        pepIdLi.append(pepUrl.split("?Number=")[-1].split("&Source=")[0])
                        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Zoekresultaten']")))
                        time.sleep(random.randint(1,3))

                        html = driver.page_source
                        respObj = Selector(text=html)

                        FIELD_NAMES = ['Name', 'Vorm','Type', 'Hoedanigheid', 'Taal', 'Adres waar u kantoor houdt', 'Email', 'Keyword', 'id']

                        div1 = [i.strip() for i in respObj.xpath("//b[contains(text(),'Vorm')]/parent::div/text()").getall() if i.strip()] 
                        dataDict = {
                            FIELD_NAMES[0]: respObj.xpath("normalize-space(//h4/text())").get(),
                            FIELD_NAMES[1]: div1[0],
                            FIELD_NAMES[2]: div1[1],
                            FIELD_NAMES[3]: respObj.xpath("normalize-space(//b[text()='Hoedanigheid']/parent::div/text()[last()])").get(),
                            FIELD_NAMES[4]: respObj.xpath("normalize-space(//b[text()='Taal']/parent::div/text()[last()])").get(),
                            FIELD_NAMES[5]: ", ".join(i.strip() for i in respObj.xpath("(//b[contains(text(),'Adres')]/following-sibling::ul/li)[1]/text()").getall() if i),
                            FIELD_NAMES[6]: respObj.xpath("normalize-space(//b[contains(text(),'E-mail')]/following-sibling::ul/li/text())").get(),
                            FIELD_NAMES[7]: "".join(i for i in alpha),
                            FIELD_NAMES[8]: driver.current_url.split("?Number=")[-1].split("&Source=")[0],
                        }
                        print(dataDict)

                        writeCSV(dataDict, FIELD_NAMES, "people.csv")

                for companyUrl in companyUrls:
                    if companyUrl.split("?Number=")[-1].split("&Source=")[0] not in cmpIdLi:
                        driver.get(f'''https://search.itaa.be{companyUrl}''')
                        cmpIdLi.append(companyUrl.split("?Number=")[-1].split("&Source=")[0])
                        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Zoekresultaten']")))
                        time.sleep(random.randint(1,3))

                        html = driver.page_source
                        respObj = Selector(text=html)

                        FIELD_NAMES = ['Name', 'Vorm','Type', 'Hoedanigheid', 'Taal', 'Adres waar u kantoor houdt', 'Email', 'Ondernemingsnummer', 'Keyword', 'id']

                        div1 = [i.strip() for i in respObj.xpath("//b[contains(text(),'Vorm')]/parent::div/text()").getall() if i.strip()] 
                        dataDict = {
                            FIELD_NAMES[0]: respObj.xpath("normalize-space(//h4/text())").get(),
                            FIELD_NAMES[1]: div1[0],
                            FIELD_NAMES[2]: div1[1],
                            FIELD_NAMES[3]: respObj.xpath("normalize-space(//b[text()='Hoedanigheid']/parent::div/text()[last()])").get(),
                            FIELD_NAMES[4]: respObj.xpath("normalize-space(//b[text()='Taal']/parent::div/text()[last()])").get(),
                            FIELD_NAMES[5]: ", ".join(i.strip() for i in respObj.xpath("(//b[contains(text(),'Adres')]/following-sibling::ul/li)[1]/text()").getall() if i),
                            FIELD_NAMES[6]: respObj.xpath("normalize-space(//b[contains(text(),'E-mail')]/following-sibling::ul/li/text())").get(),
                            FIELD_NAMES[7]: respObj.xpath("normalize-space(//b[contains(text(),'Ondernemingsnummer')]/following-sibling::ul/li/text())").get(),
                            FIELD_NAMES[8]: "".join(i for i in alpha),
                            FIELD_NAMES[9]: driver.current_url.split("?Number=")[-1].split("&Source=")[0],
                        }
                        print(dataDict)

                        writeCSV(dataDict, FIELD_NAMES, "company.csv")
                break
            except:
                driver.quit()
                time.sleep(300)
                driver = initChromeDriver()
                driver.maximize_window()
driver.quit()
