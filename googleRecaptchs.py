# -*- coding: utf-8 -*-

# system libraries
import os
import random
import time

# selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

# recaptcha libraries
import speech_recognition as sr
import ffmpy
import requests
import urllib
import pydub


def delay():
    time.sleep(random.randint(2, 3))


# create chrome driver
CHROMEDRIVERPATH = os.environ.get("chromedriver")
options = Options()
#options.headless = True
options.add_argument("start-maximized")
# options.add_argument("--no-sandbox")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(CHROMEDRIVERPATH, chrome_options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
delay()
# go to website
# driver.get("https://www.google.com/recaptcha/api2/demo")
driver.get("https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3DChina%252088%252CLongmont%252CDenver/Boulder&q=EhAkCUBiAQUQWn2ahcTih1CxGMrw9YAGIhkA8aeDSwUadyeUCdyH3jDaXxany4d6_cLcMgFy")


# switch to recaptcha frame
frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()

# click on checkbox to activate recaptcha
driver.find_element_by_class_name("recaptcha-checkbox-border").click()

# switch to recaptcha audio control frame
driver.switch_to.default_content()
frames = driver.find_element_by_xpath(
    "/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()

# click on audio challenge
driver.find_element_by_id("recaptcha-audio-button").click()

# switch to recaptcha audio challenge frame
driver.switch_to.default_content()
frames = driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
delay()

while True:
    try:
        # click on the play button
        driver.find_element_by_xpath(
            "/html/body/div/div/div[3]/div/button").click()
        # get the mp3 audio file
        src = driver.find_element_by_id("audio-source").get_attribute("src")
        print("[INFO] Audio src: %s" % src)
        # download the mp3 audio file from the source
        urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")
        sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
        sound.export(os.getcwd()+"\\sample.wav", format="wav")
        sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")
        r = sr.Recognizer()

        with sample_audio as source:
            audio = r.record(source)

        # translate audio to text with google voice recognition
        key = r.recognize_google(audio)
        print("[INFO] Recaptcha Passcode: %s" % key)

        #key in results and submit
        driver.find_element_by_id("audio-response").send_keys(key.lower())
        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)

        driver.switch_to.default_content()
        delay()
        driver.find_element_by_id("recaptcha-demo-submit").click()
        delay()

        driver.quit()
        break
    except:
        time.sleep(2)
        driver.switch_to.frame(frames[-1])
        driver.find_element_by_xpath(
            "//div[contains(@class, 'reload-button')]").click()
        time.sleep(5)
        pass
