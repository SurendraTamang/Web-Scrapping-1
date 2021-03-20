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
import pandas as pd


FIELD_NAMES = ['Name', 'Phone', 'Website', 'Address']
KEYWORDS = ["Chambres d'hôtes","gîte","Cottage","Hébergement"]

cityDF = pd.read_excel('cities.xlsx', sheet_name='test')

def writeCSV(data, fieldName, file_name):
    fileExists = os.path.isfile(file_name)
    with open(file_name, 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
        if not fileExists:
            writer.writeheader()
        writer.writerow(data)

chrome_options = webdriver.ChromeOptions()
# prefs = {"download.default_directory" : "/some/path"}
# chromeOptions.add_experimental_option("prefs",prefs)
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--incognito')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(os.environ.get('chromedriver'),chrome_options=chrome_options)
# driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.maximize_window()

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

for _,val in cityDF.iterrows():
    for keyword in KEYWORDS:
        driver.get("https://www.google.com/maps")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search Google Maps']")))

        driver.find_element_by_xpath("//input[@aria-label='Search Google Maps']").clear()
        search_box = driver.find_element_by_xpath("//input[@aria-label='Search Google Maps']")
        search_box.send_keys(f"{keyword} in {val['city']},France")
        search_box.send_keys(Keys.ENTER)

        while True:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@role='region']")))

            for i in range(10):
                scroll = driver.find_element_by_xpath("(//div[@role='region'])[last()]")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
                time.sleep(0.5)

            try:
                result = driver.find_element_by_xpath("((//div[@role='region'])[last()]/div/div/a)[1]")
                driver.execute_script("arguments[0].click()", result)
            except:
                pass
            try:
                result = driver.find_element_by_xpath("(//div[contains(@aria-label, 'Results')]/div[@data-result-index])[1]")
                driver.execute_script("arguments[0].click()", result)
            except:
                pass

            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Back to results']")))
            except:
                break  

            html = driver.page_source
            respObj = Selector(text=html)

            results = respObj.xpath("(//div[contains(@class, 'section-carousel')]//div[contains(@class, 'section-carousel')])[last()]/div")

            for i in range(1,len(results)+1):
                result = driver.find_element_by_xpath(f"(//div[contains(@class, 'section-carousel')]//div[contains(@class, 'section-carousel')])[last()]/div[{i}]")
                driver.execute_script("arguments[0].click()", result)
                time.sleep(3)

                html = driver.page_source
                respObj = Selector(text=html)

                name = respObj.xpath("//h1/span/text()").get()
                phone = respObj.xpath("//button[contains(@aria-label, 'Phone')]/@aria-label").get()
                if phone:
                    phone = phone.replace("Phone:","").strip()
                website = respObj.xpath("//button[contains(@aria-label, 'Website')]/@aria-label").get()
                if website:
                    try:
                        openWebsite = driver.find_element_by_xpath("//button[@aria-label='Open website']")
                        driver.execute_script("arguments[0].click()", openWebsite)
                        time.sleep(2)
                        driver.switch_to.window(driver.window_handles[1])            
                        website = driver.current_url.split("?utm_source=")[0]
                        while True:
                            if "https://www.google.com/maps" in website:
                                time.sleep(0.5)
                                website = driver.current_url.split("?utm_source=")[0]
                            else:
                                break
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    except:
                        driver.switch_to.window(driver.window_handles[0])
                
                address = respObj.xpath("//button[contains(@aria-label, 'Address')]/@aria-label").get()
                if address:
                    address = address.replace("Address:","").strip()

                dataDict = {
                    FIELD_NAMES[0]: name,
                    FIELD_NAMES[1]: phone,
                    FIELD_NAMES[2]: website,
                    FIELD_NAMES[3]: address,
                    # FIELD_NAMES[4]: 'chambres d hôtes',
                    # FIELD_NAMES[5]: 'Basse-Normandie',
                }

                print(dataDict)
                writeCSV(dataDict, FIELD_NAMES, './test1.csv')

            time.sleep(2)
            scroll = driver.find_element_by_xpath("//span[text()='Back to results']")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)

            backBtnElem = driver.find_element_by_xpath("//span[text()='Back to results']")
            driver.execute_script("arguments[0].click()", backBtnElem)

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@role='region']")))
            time.sleep(2)

            for i in range(3):
                scroll = driver.find_element_by_xpath("(//div[@role='region'])[last()]")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
                time.sleep(1)

            nextBtnElem = driver.find_element_by_xpath('//button[@aria-label=" Next page "]/img')
            driver.execute_script("arguments[0].click()", nextBtnElem)
            time.sleep(2)


# time.sleep(5)
driver.quit()
