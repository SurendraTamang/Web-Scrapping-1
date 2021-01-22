from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random


EMAIL = "yourEmail@gmail.com"
PASSWORD = "yourPassword"
CHROMEDRIVERPATH = "../chromedriver"
yourName = "yourName"

#   SAVING THE VISITED SELLERS LISTS TO A TEXT FILE    #
def writeSellersToFile(sellerName):
    fw = open("visitedSellersList.txt", "a")
    fw.write(f'''{sellerName}\n''')
    fw.close()

#   READING THE CATEGORIES, VISITED SELLERS AND MESSAGES FILE    #
frCAT = open("./redbubbleCategories.txt", "r")
catLi = frCAT.read().split("\n")
frCAT.close()

frVSL = open("./visitedSellersList.txt", "r")
sellerIDs = frVSL.read().split("\n")
frVSL.close()

fRmsg = open("./messages.txt", "r")
msgLi = fRmsg.read().split("\n")
fRmsg.close()

options = Options()
driver = webdriver.Chrome(CHROMEDRIVERPATH, chrome_options=options)
driver.maximize_window()
driver.get('https://www.redbubble.com/auth/login')
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//label[contains(text(), 'Email')]/preceding-sibling::input")))
time.sleep(1)

#    USER LOGIN    #
email = driver.find_element_by_xpath("//label[contains(text(), 'Email')]/preceding-sibling::input")
email.clear()
email.send_keys(EMAIL)
passwd = driver.find_element_by_xpath("//label[contains(text(), 'Password')]/preceding-sibling::input")
passwd.clear()
passwd.send_keys(PASSWORD)
time.sleep(5)
driver.find_element_by_xpath("//span[text()='Log In']/parent::span/parent::button").click()

#   PAUSE THE SCRIPT UNTIL THE CAPTCHA IS BYPASSED MANUALLY   #
while True:
    try:            
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='recaptcha challenge']")))
    except:
        break

#    SEARCHING FOR EACH CATEGORY
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='search']")))
time.sleep(2)
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
for cat in catLi:
    pageCntr = 1
    visitedSellerCount = 1
    if cat:        
        while visitedSellerCount <= 20:
            driver.get(f'''https://www.redbubble.com/shop/?iaCode=all-departments&page={pageCntr}&query={cat.lower()}&sortOrder=recent''')
            pageCntr += 1
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='search']")))
            time.sleep(15)

            #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL AVAILABLE LISTINGS #
            height = driver.execute_script("return document.body.scrollHeight")
            for i in range(1, (height//300)+1):
                driver.execute_script(f"window.scrollTo(0, {i*300});")
                time.sleep(0.1)
            driver.execute_script(f"window.scrollTo(0, -5000);")
            time.sleep(3)

            #    EXTRACTING HTML DOM    #
            html = driver.page_source
            respObj = Selector(text=html)

            cards = respObj.xpath("//div[@id='SearchResultsGrid']/a")
            for card in cards:
                rawUrl = card.xpath(".//@href").get()
                sellerName = rawUrl.split("/")[-2].split("-")[-1]
                sellerUrl = f'''https://www.redbubble.com/people/{sellerName}/shop'''
                if (visitedSellerCount <= 20) and (sellerName not in sellerIDs):
                    try:
                        driver.get(sellerUrl)
                        print(f'{sellerName} => {cat}')
                        visitedSellerCount += 1
                        sellerIDs.append(sellerName)
                        writeSellersToFile(sellerName)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='SearchResultsGrid']")))
                        time.sleep(1)

                        driver.execute_script(f"window.scrollTo(0, 2000);")
                        time.sleep(2)
                        driver.execute_script(f"window.scrollTo(0, -5000);")

                        #    LIKE 20 PRODUCTS OF THE SELLER #
                        try:
                            for cntr in range(20):
                                likeButtonElem = driver.find_element_by_xpath(f'''(//div[@id='SearchResultsGrid']/a//button[@data-testid='favorite-button'])[{cntr+1}]''')
                                driver.execute_script("arguments[0].click()", likeButtonElem)
                                time.sleep(0.5)
                        except:
                            pass

                        #   FOLLOW THE SELLER   #
                        followButtonElem = driver.find_element_by_xpath("//span[text()='Follow']/parent::span/parent::button")
                        driver.execute_script("arguments[0].click()", followButtonElem)
                        time.sleep(5)

                        #   SEND A MESSAGE TO THE SELLER   #
                        html = driver.page_source
                        respObj = Selector(text=html)
                        sellerMailUrl = respObj.xpath("//span[text()='Message']/parent::span/parent::a/@href").get()
                        driver.get(sellerMailUrl)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//textarea[@id='bm_newinput']")))
                        sellerNameElem = driver.find_element_by_xpath("//li[text()='To: ']/a")
                        sellerName = sellerNameElem.get_attribute('innerHTML').strip()
                        messageElem = driver.find_element_by_xpath("//textarea[@id='bm_newinput']")
                        messageElem.clear()
                        messageElem.send_keys(f'''Hi {sellerName},\n\n{random.choice(msgLi)}\n\nThanks\n{yourName}''')
                        sendMsgElem = driver.find_element_by_xpath("//input[@id='bm_submit_new']")
                        time.sleep(5)
                        driver.execute_script("arguments[0].click()", sendMsgElem)
                        time.sleep(15)
                    except:
                        pass
                else:
                    break

# Quit selenium driver
driver.quit()
