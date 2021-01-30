from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
import os
import time
import pandas as pd
import random


#   FETCHING THE GECKO DRIVER PATH  #
FIREFOX_DRIVER_PATH = os.environ.get('firefoxdriver')

#   READING THE EXCEL FILE CONTAINING THE SEARCH QUERIES    #
df = pd.read_excel("./searchQueries.xlsx")

#   WRITING THE DATA INTO TEXT FILE  #
def writeFile(searchQuery,fileCount,data):
    f = open(f'''./data/{searchQuery.replace(" ","_").strip()}_{fileCount}.txt''', "w", encoding="utf-8")
    f.write(data)
    f.close()

#   ITERATING OVER THE SEARCH QUERIES    #
for _,val in df.iterrows():
    #   INITIALIZING THE WEBDRIVER INSTANCE #
    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH, options=options)
    driver.maximize_window()
    #driver.set_window_size(1920, 1080)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[0])
    driver.get("https://www.google.com/search?client=firefox-b-d&q=googlesearch")
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='g']")))
    time.sleep(3)
    
    #   SEARCHING FOR THE QUERY STRING  #
    inputElem = driver.find_element_by_xpath("//input[@title='Search']")
    inputElem.clear()
    inputElem.send_keys(val['queries'])

    serachBtnElem = driver.find_element_by_xpath("//button[@type='submit']")
    driver.execute_script("arguments[0].click()", serachBtnElem)

    fileCount = 0
    for _ in range(val['pages']):
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='g']")))
        except:
            pass

        #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL AVAILABLE LISTINGS #
        height = driver.execute_script("return document.body.scrollHeight")
        for i in range(1, (height//300)+1):
            driver.execute_script(f"window.scrollTo(0, {i*300});")
            time.sleep(0.1)
        driver.execute_script(f"window.scrollTo(0, -5000);")
        time.sleep(2)

        htmlOtr = driver.page_source
        respOtr = Selector(text=htmlOtr)

        #   EXCLUDE - PEOPLE ALSO ASKED FOR URLS
        exUrlLi = []
        exUrls = respOtr.xpath("//h2[text()='People also ask']/parent::div//div[@class='g']")
        for exUrl in exUrls:
            exUrlLi.append(exUrl.xpath(".//a/@href").get())

        results = respOtr.xpath("//div[@class='g']")
        #   SWITCHING TO THE SECOND TAB -> OPEN THE SEARCH RESULT URLS -> EXTRACT HTML DOM -> SAVE    
        driver.switch_to.window(driver.window_handles[1])
        for result in results:
            searchResUrl = result.xpath(".//a/@href").get()
            if (searchResUrl not in exUrlLi) and ("youtube" not in searchResUrl):       
                driver.get(searchResUrl)
                time.sleep(3)
                #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL AVAILABLE LISTINGS #
                height = driver.execute_script("return document.body.scrollHeight")
                for i in range(1, (height//500)+1):
                    driver.execute_script(f"window.scrollTo(0, {i*500});")
                    time.sleep(0.1)
                driver.execute_script(f"window.scrollTo(0, -5000);")

                fileCount += 1
                writeFile(val['queries'], fileCount, driver.page_source)
                time.sleep(random.randint(3,80))
                
        #   HANDLING THE PAGINATION #
        driver.switch_to.window(driver.window_handles[0])
        nextBtnElem = driver.find_element_by_xpath("//span[text()='Next']")
        driver.execute_script("arguments[0].click()", nextBtnElem)
        time.sleep(3)

    #   CLOSING FIREFOX #
    driver.quit()
