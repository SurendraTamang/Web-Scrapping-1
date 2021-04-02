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
from scrapy import Selector


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

driver.get("file:///E:/myWorkspace/Web-Scrapping/kacperConsulting/9_databse_6_in_1/fbc_cfmDotBe/index.html")
time.sleep(2)

# WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//td[contains(text(), 'Naam')]")))
# time.sleep(5)

# search_box = driver.find_element_by_xpath("//td[contains(text(), 'Naam')]/following-sibling::td[1]/input")
# search_box.send_keys("")
# search_box.send_keys(Keys.ENTER)

# WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "(//table/tbody)[last()]/tr/td[@valign]/parent::tr")))
# time.sleep(3)

html = driver.page_source
respObj = Selector(text=html)

FIELD_NAMES = ['Naam', 'Arrondissement', 'Email', 'Profession', 'Interventiegebied', 'Taal', 'Address1', 'Address2', 'Contact']

rowElements = respObj.xpath("(//table/tbody)[last()]/tr/td[@valign]/parent::tr")
for re in rowElements:
    addressRaw =  re.xpath(".//td[3]/text()").getall()[:-4]
    address = [i for i in addressRaw if i.strip()]
    addr1 = None
    addr2 = None
    contact = None

    try:
        if len(address) == 2:
            addr1 = address[0].strip()
            addr2 = address[1].strip()
        else:
            if sum(c.isdigit() for c in address[2]) > 5:
                addr1 = address[0].strip()
                addr2 = address[1].strip()
                contact = address[2].strip()
                try:
                    if sum(c.isdigit() for c in address[3]) > 5:
                        contact = f"{contact},{address[3].strip()}"
                except: pass
                try:
                    if sum(c.isdigit() for c in address[4]) > 5:
                        contact = f"{contact},{address[4].strip()}"
                except: pass
            else:
                addr1 = address[2].strip()
                addr2 = address[3].strip()
                if sum(c.isdigit() for c in address[-1]) > 5:
                    contact = address[-1].strip()
                if sum(c.isdigit() for c in address[-2]) > 5:
                    contact = f"{contact},{address[-2].strip()}"
    except:
        pass

    dataDict = {
        'Naam': re.xpath("normalize-space(.//td[1]/text())").get().strip(),
        'Arrondissement': re.xpath("normalize-space(.//td[2]/text())").get(),
        'Email': re.xpath("normalize-space(.//td[3]/a[contains(@href, 'mail')]/text())").get(),
        'Profession': re.xpath("normalize-space(.//td[3]/text()[last()-1])").get(),
        'Interventiegebied': ",".join(i.strip() for i in re.xpath(".//li[contains(text(), 'Interventiegebied')]/ul/li/text()").getall() if i.strip()),
        'Taal': ",".join(i.strip() for i in re.xpath(".//li[contains(text(), 'Taal')]/ul/li/text()").getall() if i.strip()),
        'Address1': addr1,
        'Address2': addr2,
        'Contact': contact
    }
    print(dataDict)

    writeCSV(dataDict, FIELD_NAMES, './test2.csv')


driver.quit()

