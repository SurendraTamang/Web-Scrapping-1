import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
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
    class IretSpider(scrapy.Spider):
        name = 'iret'

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
                url="https://www.iretapartments.com",
                wait_time=5,
                callback=self.parse
            )

        def parse(self, response):
            driver = response.meta['driver']
            driver.maximize_window()

            html = driver.page_source
            respObj = Selector(text=html)

            states = respObj.xpath("//p[contains(text(), 'Explore Apartment Homes')]/following-sibling::div//ul/li/a[contains(@class, 'propertyName')]")
            for state in states:
                driver.get(f'https://www.iretapartments.com{state.xpath(".//@href").get()}')
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@id, 'property')]")))
                time.sleep(3)
                
                html1 = driver.page_source
                respObj1 = Selector(text=html1)

                properties = respObj1.xpath("//div[contains(@id, 'property')]")
                for count_outer, item in enumerate(properties, 1):
                    if 'Parkhouse Apartment Homes' == item.xpath("normalize-space(.//div[@data-part='pc-name']/div/text())").get() and 'Denver' == state.xpath("normalize-space(.//text())").get() :
                        try:
                            driver.execute_script("window.open('');")
                            driver.switch_to.window(driver.window_handles[1])
                            
                            driver.get("https://www.liveparkhouseapts.com/floor-plans")
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='floorplan-container']/div")))
                            time.sleep(10)
                            html4 = driver.page_source
                            respObj4 = Selector(text=html4)
                            phone = respObj4.xpath("//a[contains(@href, 'tel')]/@href").get()
                            address = respObj4.xpath("normalize-space((//a[@id='directionsLink'])[last()]/text())").get()
                            plans = respObj4.xpath("//div[@id='floorplan-container']/div")
                            cntr = 0
                            for plan in plans:
                                unitType = plan.xpath("normalize-space(.//h2/text())").get()
                                bed = plan.xpath("normalize-space(.//span[contains(text(), 'Beds')]/span[1]/text())").get()
                                bath = plan.xpath("normalize-space(.//span[contains(text(), 'Beds')]/span[2]/text())").get()
                                if plan.xpath(".//div[@aria-label='Available Units']"):
                                    cntr += 1
                                    try:
                                        driver.find_element_by_xpath("//div[@id='floorplan-container']/div//div[@aria-label='Available Units']").click()
                                        time.sleep(2)
                                    except:
                                        self.sendMail('SCRAPER ERROR ALERT: iret apartments', f'Hi,\niret scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "Selenium webdriver failed to perform the click operation on Available Units button - https://www.liveparkhouseapts.com/floor-plans".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/iretApartments/iretApartments/spiders/iret.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                                        os._exit(1)
                                    time.sleep(2)
                                    html5 = driver.page_source
                                    respObj5 = Selector(text=html5)
                                    units = respObj5.xpath(f"//div[contains(text(), '{unitType}')]/parent::div/following-sibling::div")
                                    for unit in units:
                                        apartmentNo = unit.xpath("normalize-space(.//div[@class='unit-number']/text())").get()
                                        area = unit.xpath("normalize-space(.//div[@class='unit-sqft']/text())").get()
                                        try:
                                            areaf1 = area.replace(" sqft", "")
                                        except:
                                            areaf1 = None
                                        price = unit.xpath("normalize-space(.//div[@class='unit-rent']/text())").get()
                                        lease = unit.xpath("normalize-space(.//div[contains(text(), 'Lease Term')])").get()
                                        leaseF = lease.replace("Lease Term: ", "")
                                        if unit.xpath("normalize-space(.//span[@class='available-now']/text())").get() == "NOW":
                                            availability = "Available now!"
                                        else:
                                            availability = unit.xpath("normalize-space(.//span[@class='available-now']/text())").get()
                                else:
                                    area = plan.xpath("normalize-space(.//span[contains(text(), 'Beds')]/span[3]/text())").get()
                                    try:
                                        areaf1 = area.replace(" sqft", "")
                                    except:
                                        areaf1 = None
                                    prce = plan.xpath("normalize-space(.//div[@class='fp-price-range']/strong/text())").get()
                                    price = prce.replace("From ", "")
                                    apartmentNo = None
                                    availability = None
                                    leaseF = None
                                yield{
                                    'Apartment Name': "Parkhouse Apartment Homes",
                                    'Phone': phone.replace("tel:", ""),
                                    'Address': address,
                                    'Office Hours': "Mon-Fri 9am-6pm | Sat 10am-5pm | Sun 1pm-5pm",
                                    'Type': unitType,
                                    'Area in sq ft': areaf1,
                                    'Bed': bed,
                                    'Bath': bath,
                                    'Availability': availability,
                                    'Lease Term(months)': leaseF,
                                    'Price': price,
                                    'Apartment Numbers': apartmentNo,
                                    'Apartment Specs': None,
                                    'Lifestyle': None,
                                    'Community Amenities': respObj4.xpath("//ul[contains(@class, 'amenities-list')]/li/text()").getall(),
                                    'Floor Plan Amenities': None,
                                    # 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                }

                            driver.switch_to.window(driver.window_handles[0])
                        except:
                            self.sendMail('SCRAPER ERROR ALERT: iret apartments', f'Hi,\niret scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "Script failed for - https://www.liveparkhouseapts.com/floor-plans".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/iretApartments/iretApartments/spiders/iret.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                            os._exit(1)
                    else:
                        try:
                            try:
                                driver.find_element_by_xpath(f"(//div[contains(@id, 'property')])[{count_outer}]").click()
                            except:
                                self.sendMail('SCRAPER ERROR ALERT: iret apartments', f'Hi,\niret scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "Selenium websdriver failed to perform the click operation on the community listings page".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/iretApartments/iretApartments/spiders/iret.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                                os._exit(1)
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-component='selection-group']/div")))
                            time.sleep(6)
                            html2 = driver.page_source
                            respObj2 = Selector(text=html2)
                            address = respObj2.xpath("normalize-space(//div[contains(@class, 'propertyDetails_content')]/div/p[@class='text']/text())").get()
                            officeHours = respObj2.xpath("normalize-space(//p[contains(text(), 'Office Hours')]/text())").get()
                            phone = respObj2.xpath("//a[contains(@href, 'tel')]/@href").get()
                            lifestyle = respObj2.xpath("//div[contains(@class, 'lifestyles')]/div//p/text()").getall()
                            communityAmenities = respObj2.xpath("//ul[@data-id='communityAmenitiesList']/li/text()").getall()
                            floorPlanAmenities = respObj2.xpath("//ul[@data-id='floorplanAmenitiesList']/li/text()").getall()
                            apartmentName = respObj2.xpath("(//input[contains(@placeholder, 'Search by City')]/@value)[last()]").get()

                            types = respObj2.xpath("//div[@data-component='selection-group']/div")

                            for count,item in enumerate(types, 1):
                                element1 = driver.find_element_by_xpath(f"//div[@data-component='selection-group']/div[{count}]")
                                driver.execute_script("return arguments[0].scrollIntoView(true);", element1)
                                driver.execute_script("scrollBy(0,-150);")
                                try:
                                    driver.find_element_by_xpath(f"//div[@data-component='selection-group']/div[{count}]").click()
                                except:
                                    self.sendMail('SCRAPER ERROR ALERT: iret apartments', f'Hi,\niret scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "Selenium websdriver failed to perform the click operation on appartment types in the community details page.".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/iretApartments/iretApartments/spiders/iret.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                                    os._exit(1)
                                time.sleep(6)
                                html3 = driver.page_source
                                respObj3 = Selector(text=html3)
                                models = respObj3.xpath("//div[@data-id='unitsContainer']/div")
                                for model in models:
                                    modelType = model.xpath("normalize-space(.//div[@data-id='marketingLayoutTitleContainer']/p/text())").get()
                                    area = model.xpath("normalize-space(.//span[@data-id='marketingLayoutSqft']/text())").get()
                                    try:
                                        areaf = area.replace(" sq ft", "")
                                    except:
                                        areaf = None
                                    bed = model.xpath("normalize-space(.//span[contains(text(), 'Beds')]/following-sibling::span/text())").get()
                                    bath = model.xpath("normalize-space(.//span[contains(text(), 'Baths')]/following-sibling::span/text())").get()
                                    aprTypes = model.xpath(".//div[@data-id='marketingLayoutCardsContainer']/div")
                                    for aprType in aprTypes:
                                        availability  = aprType.xpath("normalize-space(.//p[@data-id='availableDate']/span/text())").get()
                                        price  = aprType.xpath("normalize-space(.//p[@data-id='price']/text())").get()
                                        apartmentNo  = aprType.xpath("normalize-space(.//p[@data-component='Caption'][last()]/text())").get()
                                        apartmentDetails  = aprType.xpath("normalize-space(.//p[@data-component='Caption'][last()]/parent::div/following-sibling::p/text())").get()
                                        yield{
                                            'Apartment Name': apartmentName,
                                            'Phone': phone.replace("tel:", ""),
                                            'Address': address,
                                            'Office Hours': officeHours.replace("Office Hours: ", ""),
                                            'Type': modelType,
                                            'Area in sq ft': areaf,
                                            'Bed': bed,
                                            'Bath': bath,
                                            'Availability': availability,
                                            'Lease Term(months)': None,
                                            'Price': price,
                                            'Apartment Numbers': apartmentNo,
                                            'Apartment Specs': apartmentDetails,
                                            'Lifestyle': lifestyle,
                                            'Community Amenities': communityAmenities,
                                            'Floor Plan Amenities': floorPlanAmenities,
                                            # 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                                        }

                            driver.execute_script("window.history.go(-1)")
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@id, 'property')]")))
                            time.sleep(4)
                            element = driver.find_element_by_xpath(f"(//div[contains(@id, 'property')])[{count_outer}]")
                            driver.execute_script("return arguments[0].scrollIntoView(true);", element)
                            time.sleep(3)
                            driver.execute_script("scrollBy(0,100);")
                            time.sleep(5)
                        except:
                            self.sendMail('SCRAPER ERROR ALERT: iret apartments', f'Hi,\niret scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "Else part of the parse function failed with some unexcepted error".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/iretApartments/iretApartments/spiders/iret.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                            os._exit(1)

except Exception:
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: iret apartments'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\niret apartments scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/iretApartments/iretApartments/spiders/iret.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
