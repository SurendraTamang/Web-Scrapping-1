import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import os
import sys
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class AmericanhomesSpider(scrapy.Spider):
        name = 'americanhomes'

        init_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

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
                url="https://www.americanhomes4rent.com/States/AZ?lv=true",
                wait_time=5,
                callback=self.parse
            )

        def parse(self, response):
            try:
                driver = response.meta['driver']
                driver.maximize_window()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='listings']/li//button[contains(@class, 'full-details')]")))
                time.sleep(3)

                html = driver.page_source
                respObj = Selector(text=html)

                states = respObj.xpath("//span[contains(text(), 'Please Select')]/parent::a/parent::li/following-sibling::li/a/span/text()").getall()
                if states[-1] == "\xa0":
                    states = states[:-1]
                for state in states:
                    driver.get(f'https://www.americanhomes4rent.com/States/{state}?lv=true')
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//ul[@id='listings']/li//button[contains(@class, 'full-details')]")))
                    time.sleep(5)

                    html1 = driver.page_source
                    respObj1 = Selector(text=html1)

                    homes = respObj1.xpath("//ul[@id='listings']/li//button[contains(@class, 'full-details')]")
                    for home in homes:
                        homeUrl = home.xpath(".//@onclick").get()
                        yield scrapy.Request(
                            url=homeUrl.replace("location.href='", "").rstrip("'"),
                            callback=self.homeDetails
                        )
            except:
                self.sendMail('SCRAPER ERROR ALERT: americanHomes4rent', f'Hi,\namericanhomes scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed with some unexcepted error. May be the website layout might have been changed / Page didnt load properly".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/americanhomes4rent/americanhomes4rent/spiders/americanhomes.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def homeDetails(self, response):
            try:
                amntyFinal = []
                images = response.xpath("//div[@class='showcase-thumbnail']/img/@src").getall()
                intAmmenities = response.xpath("//h4[contains(text(), 'Exterior')]/preceding-sibling::div[@class='amft-piece']")
                for intAmmenity in intAmmenities:
                    amntyType = intAmmenity.xpath("normalize-space(.//h5/text())").get()
                    amnty = intAmmenity.xpath(".//ul/li/span/text()").getall()
                    amntyFinal.append(f'''{amntyType}:{",".join(i.strip() for i in amnty)}''')
                yield{
                    'Address': response.xpath("normalize-space(//h2/text())").get(),
                    'Price': f'''${response.xpath("normalize-space(//h3[contains(@class, 'price')]/text())").get()}''',
                    'Bed': response.xpath("normalize-space(//h5[contains(text(), 'Beds')]/following-sibling::p/text())").get(),
                    'Bath': response.xpath("normalize-space(//h5[contains(text(), 'Baths')]/following-sibling::p/text())").get(),
                    'Area in sq ft': response.xpath("normalize-space(//h5[contains(text(), 'Sq Ft')]/following-sibling::p/text())").get(),
                    'Built Year': response.xpath("normalize-space(//h5[contains(text(), 'Built')]/following-sibling::p/text())").get(),
                    'Availability': response.xpath("normalize-space(//span[@id='estimated-date-value']/text())").get(),
                    'Phone': response.xpath("normalize-space(//span[@id='contact-number']/text())").get(),
                    'Interior Amenities': " | ".join(amntyFinal),
                    'Exterior Amenities': response.xpath("//h4[contains(text(), 'Exterior')]/following-sibling::div[@class='amft-piece']/ul/li/span/text()").getall(),
                    'House Images': ",".join(image.replace("small", "medium") for image in images),
                    'Property Url': response.url,
                    #'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }
            except:
                self.sendMail('SCRAPER ERROR ALERT: americanHomes4rent', f'Hi,\namericanhomes scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "homeDetails function failed with some unexcepted error. May be the website layout might have been changed / Page didnt load properly".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/americanhomes4rent/americanhomes4rent/spiders/americanhomes.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except Exception:
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: americanHomes4rent'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\namericanhomes4rent scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/americanhomes4rent/americanhomes4rent/spiders/americanhomes.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
