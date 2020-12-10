import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class UdrdotcomSpider(scrapy.Spider):
        name = 'udrdotcom'

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
                url="https://www.udr.com/search-apartments",
                wait_time=5,
                callback=self.parse
            )

        def parse(self, response):
            try:
                driver = response.meta['driver']
                driver.maximize_window()
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[0])
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'market-and-state')]/li/div/div")))
                time.sleep(1)


                html1 = driver.page_source
                respObj1 = Selector(text=html1)

                cities = respObj1.xpath("//ul[contains(@class, 'market-and-state')]/li/div/div/a")
                for city in cities:
                    driver.get(f'''https://www.udr.com{city.xpath(".//@href").get()}map''')
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='market-card card']")))
                    time.sleep(1)

                    html2 = driver.page_source
                    respObj2 = Selector(text=html2)

                    communitites = respObj2.xpath("//div[@class='market-card card']")
                    driver.switch_to.window(driver.window_handles[1])
                    for community in communitites:
                        communityName = community.xpath("normalize-space(.//span[@class='prop-name']/text())").get()
                        address = community.xpath(".//span[@class='address']/text()").getall()


                        #   --- CODE TO SCRAPE IMAGES ---
                        driver.get(f'''https://www.udr.com{community.xpath(".//a[contains(@href, 'photos-and-tours')]/@href").get()}''')
                        # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class='swiper-wrapper']")))
                        time.sleep(5)
                        html5 = driver.page_source
                        respObj5 = Selector(text=html5)
                        cimg1 = respObj5.xpath("//ul[@class='swiper-wrapper']/li[contains(@class, 'community')]/div/div/img/@data-src").getall()
                        cimg2 = respObj5.xpath("//ul[@class='swiper-wrapper']/li[contains(@class, 'community')]/div/div/img/@src").getall()
                        aimg1 = respObj5.xpath("//ul[@class='swiper-wrapper']/li[contains(@class, 'apartment')]/div/div/img/@data-src").getall()
                        aimg2 = respObj5.xpath("//ul[@class='swiper-wrapper']/li[contains(@class, 'apartment')]/div/div/img/@src").getall()                
                        #   --- CODE TO SCRAPE IMAGES ENDS ---  


                        #   --- CODE TO SCRAPE AMENITIES ---
                        driver.get(f'''https://www.udr.com{respObj5.xpath("//span[contains(text(), 'Amenities')]/parent::a/@href").get()}''')
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//section/div[@class='row']")))
                        html6 = driver.page_source
                        respObj6 = Selector(text=html6)
                        amntys = respObj6.xpath("//section/div[@class='row']")
                        for amnty in amntys:
                            chkCmty = amnty.xpath(".//span[contains(text(), 'Community Amenities')]/text()").get()
                            chkApt = amnty.xpath(".//span[contains(text(), 'Apartment Amenities')]/text()").get()
                            if chkCmty :
                                aptAmnty = amnty.xpath(".//ul[contains(@class, 'amenities-list')]/li/text()").getall()
                                aptAmntyF = "|".join(x.strip() for x in aptAmnty)
                            elif chkApt :
                                cmntyAmnty = amnty.xpath(".//ul[contains(@class, 'amenities-list')]/li/text()").getall()
                                cmntyAmntyF = "|".join(y.strip() for y in cmntyAmnty)
                            else:
                                aptAmntyF = None
                                cmntyAmntyF = None
                            chkCmty = None
                            chkApt = None
                        #   --- CODE TO SCRAPE AMENITIES ENDS ---   

                        driver.get(f'''https://www.udr.com{community.xpath(".//a[contains(@aria-label, 'Apartments and Pricing')]/@href").get()}''')
                        # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='market-card card']")))
                        time.sleep(3)
                        
                        html3 = driver.page_source
                        respObj3 = Selector(text=html3)

                        floorplans = respObj3.xpath("//div[@class='floorplans-filter-beds']/a")
                        for floorplan in floorplans:
                            if "from $" in floorplan.xpath("normalize-space(.//span[contains(@id, 'monthlyRentMin')]/text())").get():
                                driver.get(f'''https://www.udr.com{floorplan.xpath(".//@href").get()}''')
                                time.sleep(3)
                                
                                html4 = driver.page_source
                                respObj4 = Selector(text=html4)

                                apartments = respObj4.xpath("//ul[@id='unitResults']/li")
                                for apartment in apartments:
                                    yield{
                                        'Community Name': communityName,
                                        'Apartment No': apartment.xpath(".//@data-long-title").get().replace("Apartment ", ""),
                                        'Address': ", ".join(addr.strip() for addr in address),
                                        'Bath': apartment.xpath(".//@data-baths").get(),
                                        'Bed' : apartment.xpath(".//@data-beds").get(),                            
                                        'Area in sq ft': apartment.xpath(".//@data-sqft-min").get(),
                                        'Price': apartment.xpath(".//@data-rent-min").get(),
                                        'Availability': apartment.xpath(".//@data-movedate").get(),
                                        'Apartment Features' : "|".join(amnty.strip() for amnty in apartment.xpath(".//ul[contains(@id, 'appartamentFeatures')]/li/text()").getall()),    
                                        'Floor Plan Name': apartment.xpath(".//@data-floor-plan-name").get(),
                                        'Floor Plan Img Url': f'''https://www.udr.com{apartment.xpath(".//img[@alt='listing image']/@src").get()}''',
                                        'Apartment Amenities': aptAmntyF,
                                        'Community Amenities': cmntyAmntyF,
                                        'Appartment Images Url': ",".join(f'https://www.udr.com{aimg}' for aimg in aimg1+aimg2),
                                        'Community Images Url': ",".join(f'https://www.udr.com{cimg}' for cimg in cimg1+cimg2),
                                        # 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                    }
            except:
                self.sendMail('SCRAPER ERROR ALERT: udr', f'Hi,\nudr scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed.".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/udr/udr/spiders/udrdotcom.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except :
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: udr'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\nudr scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/udr/udr/spiders/udrdotcom.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)