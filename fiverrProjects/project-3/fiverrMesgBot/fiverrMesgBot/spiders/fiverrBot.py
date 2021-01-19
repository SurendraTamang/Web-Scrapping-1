import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd


class FiverrbotSpider(scrapy.Spider):
    name = 'fiverrBot'
    FILEPATH = "checkVisitedSellersUrls.csv"
    max_Gigs = int(input("Enter the number of Gigs for which you want to send a message : "))
    max_Gigs_Cntr = 1
    EMAIL = "yourEmail@gmail.com"
    PSSWD = "yourPassword"
    df = pd.read_csv(FILEPATH)
    visitedUrlsLi = df['url'].values.tolist()

     #   WRITING ALREADY MESSAGED GIG'S URLS TO A CSV FILE  #
    def writeCSV(self, dict_data, fieldName):
        with open(self.FILEPATH, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldName, lineterminator='\n')
            for data in dict_data:
                writer.writerow(data)

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.fiverr.com/login",
            wait_time=5,
            callback=self.parse,
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])
        driver.maximize_window()

        #   PAUSE THE SCRIPT UNTIL THE CAPTCHA IS BYPASSED MANUALLY   #
        while True:
            try:            
                WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//p[text()='One Small Step']")))
            except:
                break

        #   lOGGING IN TO FIVERR    #
        email = driver.find_element_by_xpath("//input[@id='login']")
        email.send_keys(self.EMAIL)
        passwd = driver.find_element_by_xpath("//input[@id='password']")
        passwd.send_keys(self.PSSWD)
        driver.find_element_by_xpath("//p[text()='Continue']/parent::button").click()
        time.sleep(4)
        #   Provide the niche URL here  #
        driver.get("https://www.fiverr.com/categories/lifestyle/gaming?source=side-menu")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "(//div[contains(@class, 'gig_listings')])[1]/div")))

        while True:
            if self.max_Gigs_Cntr <= self.max_Gigs:
                pass
            else:
                break
            #   GETTING THE PAGE HEIGHT & SCROLLING GRADUALLY THROUGH THE PAGE TO LAOD ALL THE GIGS #
            height = driver.execute_script("return document.body.scrollHeight")
            for i in range(1, (height//300)+1):
                driver.execute_script(f"window.scrollTo(0, {i*300});")
                time.sleep(0.1)
            driver.execute_script(f"window.scrollTo(0, -5000);")

            #   FETCHING THE HTML DOM   #
            html1 = driver.page_source
            resp1 = Selector(text=html1)

            #   GOING TO EACH & EVERY GIG AND SEND A CUSTOM MESSAGE   #
            gigs = resp1.xpath("(//div[contains(@class, 'gig_listings')])[1]/div")
            driver.switch_to.window(driver.window_handles[1])
            for gig in gigs:
                sellerName = gig.xpath("normalize-space(.//div[@class='seller-name']/a/text())").get()
                sellerUrlRaw = gig.xpath(".//div[@class='seller-name']/a/@href").get()
                sellerUrl = f'''https://www.fiverr.com{sellerUrlRaw.split("?")[0]}'''
                gigUrl = f'''https://www.fiverr.com{gig.xpath(".//h3/a/@href").get()}'''
                if (self.max_Gigs_Cntr <= self.max_Gigs) and (sellerUrl not in self.visitedUrlsLi):
                    self.visitedUrlsLi.append(sellerUrl)
                    urlChk = []
                    driver.get(gigUrl)
                    try:
                        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Contact Seller']")))
                        time.sleep(6)
                        cntSllr = driver.find_element_by_xpath("//a[text()='Contact Seller']")
                        driver.execute_script("arguments[0].click()", cntSllr)
                        mssg = driver.find_element_by_xpath("//div[contains(@class, 'popup-main')]/form//textarea")
                        mssg.send_keys(f'''Hello {sellerName}!''')
                        driver.find_element_by_xpath("//a[text()='Send']").click()
                        time.sleep(6)
                        self.max_Gigs_Cntr += 1
                        urlChk.append(
                            {
                                'url': sellerUrl,
                            }
                        )
                        self.writeCSV(urlChk, ["url"])
                    except:
                        urlChk.append(
                            {
                                'url': sellerUrl,
                            }
                        )
                        self.writeCSV(urlChk, ["url"])
                else:
                    break
            driver.switch_to.window(driver.window_handles[0])      

            #   HANDLING THE PAGINATION  #
            if resp1.xpath("//li[@class='page-number']/following-sibling::li[@class='pagination-arrows']"):
                elem = driver.find_element_by_xpath("//li[@class='pagination-arrows']/a")
                driver.execute_script("arguments[0].click()", elem)
                time.sleep(4)
            else:
                break