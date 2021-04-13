from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from scrapy import Selector
import os
import time
import csv


#-- Writing Data to a HTML file --#
def writeHTML(data, file_name):
    f = open(file_name, "w")
    f.write(data)
    f.close()

#-- Initializing the chrome driver --#
def initChromeDriver():
    chrome_options = webdriver.ChromeOptions()
    # prefs = {"download.default_directory" : "/some/path"}
    # chromeOptions.add_experimental_option("prefs",prefs)
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(os.environ.get('chromedriver'), chrome_options=chrome_options) 
    # driver = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
    
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
    url = "https://www.pointdevente.fr/fr/murs-de-boutique-occupes/murs-de-boutique/lf_10"
    driver = initChromeDriver()
    driver.maximize_window()
    driver.get(url)

    html = driver.page_source

    writeHTML(html, f'''{url.replace("https://www.","")}.html''')

    