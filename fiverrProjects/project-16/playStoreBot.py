from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import os
import csv
import time
import random

FILE_NAME = "testttt.csv"

with open(FILE_NAME) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for indx,data in enumerate(csv_reader):
        if indx != 0 and data[4] == "Like":
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
            driver.maximize_window()

            stealth(driver,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )

            driver.get(data[0])
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Sign in']")))
            time.sleep(random.randint(2,6))

            signInBtnElem = driver.find_element_by_xpath("//a[text()='Sign in']")
            driver.execute_script("arguments[0].click()", signInBtnElem)

            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Email or phone']")))

            email = driver.find_element_by_xpath("//input[@aria-label='Email or phone']")
            email.send_keys(data[1])

            nextBtnElem = driver.find_element_by_xpath("//span[text()='Next']")
            driver.execute_script("arguments[0].click()", nextBtnElem)
            time.sleep(random.randint(2,6))

            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Enter your password']")))

            passwd = driver.find_element_by_xpath("//input[@aria-label='Enter your password']")
            passwd.send_keys(data[2])

            nextBtnElem = driver.find_element_by_xpath("//span[text()='Next']")
            driver.execute_script("arguments[0].click()", nextBtnElem)
            time.sleep(random.randint(2,6))

            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[text()='Confirm your recovery email']")))
                recoveryBtnElem = driver.find_element_by_xpath("//div[text()='Confirm your recovery email']")
                driver.execute_script("arguments[0].click()", recoveryBtnElem)
                time.sleep(random.randint(2,6))

                recoveryEmail = driver.find_element_by_xpath("//input[@type='email']")
                passwd.send_keys(data[3])

                nextBtnElem = driver.find_element_by_xpath("//span[text()='Next']")
                driver.execute_script("arguments[0].click()", nextBtnElem)
                time.sleep(random.randint(2,6))   
            except:
                pass
            
            #-- Mark the comment as Helpful
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-tooltip='Helpful']")))
            likeBtnElem = driver.find_element_by_xpath("//div[@data-tooltip='Helpful']")
            driver.execute_script("arguments[0].click()", likeBtnElem)
            
            time.sleep(random.randint(10,30))

            driver.quit()
            time.sleep(random.randint(10,30))
