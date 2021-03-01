from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
from selenium_stealth import stealth
import os
import csv
import time


CHROMEDRIVER_PATH = os.environ.get("chromedriver")

def writeCSV(data, fieldName, FILE_NAME):
    fileExists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, 'a', encoding='utf-8') as csvfile:
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
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(CHROMEDRIVER_PATH,chrome_options=chrome_options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get("https://www.alphaquery.com/login?returnPage=")
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='email']")))

#    USER LOGIN    #
email = driver.find_element_by_xpath("//input[@name='email']")
email.clear()
email.send_keys("mayur.sangani@gmail.com")
passwd = driver.find_element_by_xpath("//input[@name='password']")
passwd.clear()
passwd.send_keys("Parth1510!")
time.sleep(5)
loginBtnElem = driver.find_element_by_xpath("//button[text()='Log In']")
driver.execute_script("arguments[0].click()", loginBtnElem)

#    NAVIGATING TO QUERY TOOL PAGE    #
queryToolElem = driver.find_element_by_xpath("//a[text()='Query Tool']")
driver.execute_script("arguments[0].click()", queryToolElem)
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Run']")))

#    COPY PASTING THE USER DEFINED QUERY IN THE QUERY BOX    #
testQuery = '''SELECT ticker, name, close_price, volume, percent_change_price_1_day FROM data WHERE close_price >= 5.00 AND average_volume >= 100000 ORDER BY market_cap DESC LIMIT 500'''
queryBox = driver.find_element_by_xpath("//span[@class='cm-keyword']")
queryBox.clear()
queryBox.send_keys(testQuery)
runBtnElem = driver.find_element_by_xpath("//button[text()='Run']")
driver.execute_script("arguments[0].click()", runBtnElem)
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "(//tbody)[last()]/tr")))

time.sleep(5)

html = driver.page_source
respObj = Selector(text=html)

driver.quit()
