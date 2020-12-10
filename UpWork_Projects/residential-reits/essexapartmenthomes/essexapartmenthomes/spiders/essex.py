# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class EssexSpider(scrapy.Spider):
        name = 'essex'

        init_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # urls = pd.read_csv("D:/sipun/rrScrapers/essexapartmenthomes/essexAPI/apmtUrls.csv")
        urls = pd.read_csv("/home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes/essexAPI/apmtUrls.csv")

        EMAIL_USER = os.environ.get('EMAIL_USER')
        EMAIL_PASS = os.environ.get('EMAIL_PASS')

        def sendMail(self, subject, body):
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.EMAIL_USER
            msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
            msg.set_content(body)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.EMAIL_USER, self.EMAIL_PASS)    
                smtp.send_message(msg)
        

        def start_requests(self):
            yield SeleniumRequest(
                url="https://www.essexapartmenthomes.com",
                wait_time=5,
                callback=self.parse
            )

        def parse(self, response):
            try:
                driver = response.meta['driver']
                driver.maximize_window()

                for _,val in self.urls.iterrows():
                    if '500-folsom' not in val['Floor Plans Url']:
                        driver.get(val['Floor Plans Url'].replace("/floor-plans-and-pricing", ""))
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'office-hours')]/table")))
                        time.sleep(1)
                        html1 = driver.page_source
                        respObj1 = Selector(text=html1)

                        days = respObj1.xpath("//div[contains(@class, 'office-hours')]/table/tr")
                        ofcHrs = []
                        for day in days:
                            ofcHrs.append(" ".join(day.xpath(".//td/text()").getall()))
                            
                        driver.get(val['Floor Plans Url'])
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='floor-plan-card__wrapper' or @class='select-unit-container']/div")))
                        time.sleep(2)
                        html = driver.page_source
                        respObj = Selector(text=html)

                        floorPlans = respObj.xpath("//div[@class='floor-plan-card__wrapper' or @class='select-unit-container']/div")
                        for floorPlan in floorPlans:
                            if "pricing-card" in floorPlan.xpath(".//@class").get():
                                bedBath = floorPlan.xpath("normalize-space(.//p[contains(@class, 'size')]/text())").get()
                                bed = bedBath.split("/")[0].strip().split(" ")[0]
                                bath = bedBath.split("/")[1].strip().split(" ")[0]
                                area = floorPlan.xpath("normalize-space(.//span[contains(text(), 'sq')]/text())").get().replace("sq. ft.", "").strip()
                                floorPlanType = None
                                try:
                                    availability = respObj.xpath("normalize-space(//p[contains(@class, 'availability')]/text())").get().replace("Available as soon as:","").strip()
                                except:
                                    availability = None
                                try:
                                    price = floorPlan.xpath("normalize-space(.//p[contains(@class, 'price')]/text())").get().replace("Starting at","").strip()
                                except:
                                    price = None
                            else:
                                bedBath = floorPlan.xpath("normalize-space(.//p[contains(@class, 'content__size')]/text()[1])").get()
                                
                                bed = bedBath.split("/")[0].strip().split(" ")[0]
                                bath = bedBath.split("/")[1].strip().split(" ")[0]
                                floorPlanType = floorPlan.xpath("normalize-space(.//p[contains(@class, 'content__layout')]/text())").get()
                                area = floorPlan.xpath("normalize-space(.//p[contains(@class, 'content__size')]/text()[2])").get().replace("sq. ft.", "").strip()            

                                if floorPlan.xpath(".//span[contains(text(), 'Available')]"):
                                    price = floorPlan.xpath("normalize-space(.//p[contains(@class, 'content__price')]/text())").get().replace("Starting from", "").strip()
                                    availability = floorPlan.xpath("normalize-space(.//p[contains(@class, 'content__availability')]/text())").get().replace("Available as soon as:","").strip()
                                else:
                                    availability = floorPlan.xpath("normalize-space(.//p[contains(@class, 'content__price')]/text())").get()
                                    price = None                      
                                    
                            yield{
                                'Community Name': val['Community Name'],
                                'Address': val['Address'],
                                'City': val['City'],
                                'State': val['State'],
                                'Zip Code': val['Zip Code'],
                                'Coordinate': val['Coordinate'],
                                'Phone': val['Phone'],
                                'Office Hours': " | ".join(oh.strip() for oh in ofcHrs),
                                'Floor Plan Type': floorPlanType,
                                'Area in sq ft': area,
                                'Bed': bed,
                                'Bath': bath,
                                'Price': price,
                                'Availability': availability,
                                'Floor Plan Url': floorPlan.xpath(".//div[@class='image-lightbox']/div/img//@src").get(),
                                'Apartment Amenities': val['Apartment Amenities'],
                                'Community Amenities': val['Community Amenities'],
                                'Community Images': val['Community Images'],
                                'Base URL': val['Floor Plans Url'],
                                'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            }
            except:
                self.sendMail('SCRAPER ERROR ALERT: essexApartmentHomes', f'Hi,\nessexapartmenthomes scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes/essexapartmenthomes/spiders/essex.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except :
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: essexApartmentHomes'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\nessexApartmentHomes scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes/essexapartmenthomes/spiders/essex.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
