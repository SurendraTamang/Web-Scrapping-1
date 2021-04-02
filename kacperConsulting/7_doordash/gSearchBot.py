from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
from selenium_stealth import stealth
import os
import pandas as pd
from urllib.parse import unquote, quote
import csv

# recaptcha libraries
# import speech_recognition as sr
# import ffmpy
# import requests
# import urllib
# import pydub


df = pd.read_excel("./inputData/testData.xlsx", sheet_name="Sheet1")
#df = pd.read_excel("/root/doordash/testData.xlsx", sheet_name="Sheet1")
try:
    df1 = pd.read_csv("./scrappedData/data_Sheet2.csv")
    #df1 = pd.read_csv("/root/doordash/data_Sheet2.csv")
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
    fileExists = os.path.isfile("./scrappedData/data_Sheet2.csv")
    #fileExists = os.path.isfile("/root/doordash/data_Sheet2.csv")
    with open("./scrappedData/data_Sheet2.csv", 'a', encoding='utf-8') as csvfile:
    #with open("/root/doordash/data_Sheet2.csv", 'a', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
        if not fileExists:
            writer.writeheader()
        writer.writerow(data)

browser = "chrome"
browser1 = "firefox"

CHROMEDRIVERPATH = os.environ.get("chromedriver")
options = Options()
#options.headless = True
options.add_argument("start-maximized")
#options.add_argument("--no-sandbox")
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

#CHROMEDRIVERPATH = ("/root/chromedriver")
FIELD_NAMES = ['Id', 'City', 'Area', 'Restaurant Name', 'Average Rating', 'Number Of Reviews', 'Search Queries', 'Website', 'Phone']
cntr = 0


for _,val in df.iterrows():

    if val['Id'] not in idList:
        idList.append(val['Id'])
        driver.get(f"https://www.google.co.in/search?q={quote(val['gSearchQuery'])}")
        time.sleep(random.randint(2,4))
        #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a")))
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@title='Search']")))
        except:
            while True:
                print("Encountered Captcha")
                if browser == "firefox":
                    from selenium.webdriver.chrome.options import Options
                    browser = "chrome"
                    driver.quit()
                    time.sleep(random.randint(30,60))

                    options = Options()
                    #options.headless = True
                    options.add_argument("start-maximized")
                    #options.add_argument("--no-sandbox")
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
                else:
                    driver.quit()
                    time.sleep(random.randint(30,60))
                    browser = "firefox"
                    from selenium.webdriver.firefox.options import Options
                    FIREFOX_DRIVER_PATH = os.environ.get('firefoxdriver')
                    #FIREFOX_DRIVER_PATH = "/root/geckodriver"
                    options = Options()
                    driver = webdriver.Firefox(executable_path=FIREFOX_DRIVER_PATH, options=options)
                    driver.maximize_window()

                driver.get(f"https://www.google.co.in")
                #   SEARCHING FOR THE QUERY STRING  #
                inputElem = driver.find_element_by_xpath("//input[@title='Search']")
                inputElem.clear()
                inputElem.send_keys(val['gSearchQuery'])
                driver.find_element_by_xpath("//input[@title='Search']").send_keys(Keys.ENTER)

                time.sleep(random.randint(3,6))
                # driver.get(f"https://www.google.co.in/search?q={quote(val['gSearchQuery'])}")
                # time.sleep(random.randint(2,4))

                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@title='Search']")))
                    break
                except:
                    pass
        # if cntr % 10 == 0:
        #     driver.quit()

            # try:
            #     # switch to recaptcha frame
            #     frames = driver.find_elements_by_tag_name("iframe")
            #     driver.switch_to.frame(frames[0])
            #     time.sleep(random.randint(2,3))

            #     # click on checkbox to activate recaptcha
            #     driver.find_element_by_class_name("recaptcha-checkbox-border").click()
            #     time.sleep(random.randint(2,3))

            #     # switch to recaptcha audio control frame
            #     driver.switch_to.default_content()
            #     frames = driver.find_element_by_xpath(
            #         "/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
            #     driver.switch_to.frame(frames[0])
            #     time.sleep(random.randint(2,3))

            #     # click on audio challenge
            #     driver.find_element_by_id("recaptcha-audio-button").click()

            #     # switch to recaptcha audio challenge frame
            #     driver.switch_to.default_content()
            #     frames = driver.find_elements_by_tag_name("iframe")
            #     driver.switch_to.frame(frames[-1])
            #     time.sleep(random.randint(2,3))

            #     while True:
            #         try:
            #             # click on the play button
            #             driver.find_element_by_xpath(
            #                 "/html/body/div/div/div[3]/div/button").click()
            #             # get the mp3 audio file
            #             src = driver.find_element_by_id("audio-source").get_attribute("src")
            #             print("[INFO] Audio src: %s" % src)
            #             # download the mp3 audio file from the source
            #             urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
            #             sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
            #             sound.export(os.getcwd()+"\\sample.wav", format="wav")
            #             sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
            #             r = sr.Recognizer()

            #             with sample_audio as source:
            #                 audio = r.record(source)

            #             # translate audio to text with google voice recognition
            #             key = r.recognize_google(audio)
            #             print("[INFO] Recaptcha Passcode: %s" % key)

            #             #key in results and submit
            #             driver.find_element_by_id("audio-response").send_keys(key.lower())
            #             time.sleep(2)
            #             driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)

            #             driver.switch_to.default_content()
            #             time.sleep(random.randint(2,3))
            #             driver.find_element_by_id("recaptcha-demo-submit").click()
            #             time.sleep(random.randint(2,3))

            #             driver.quit()
            #             break
            #         except:
            #             time.sleep(2)
            #             driver.switch_to.frame(frames[-1])
            #             driver.find_element_by_xpath(
            #                 "//div[contains(@class, 'reload-button')]").click()
            #             time.sleep(5)
            #             pass
            # except:
            #     pass

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

        #if cntr % 10 == 0:
            
driver.quit()