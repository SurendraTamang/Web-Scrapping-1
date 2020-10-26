import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


class PickupspiderSpider(scrapy.Spider):
    name = 'pickupSpider'

    df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/kacper/pickup/Locations.xlsx", sheet_name='mainData')

    def formatAddress(self, address):
        li = []
        for i in address:
            if i != None:
                li.append(i.strip())
        return " ".join(i for i in li)
    
    def formatDay(self, days):
        li = []
        for i in days:
            if i != "" and i != "\n    ":
                li.append(i.strip())
        return " | ".join(i for i in li)

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.pickup.fr/trouver-un-relais",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        i = 0
        driver = response.meta['driver']
        driver.maximize_window()
        time.sleep(2)
        try:
            driver.find_element_by_xpath("//a[contains(@class,'cookie')]").click()
        except:
            pass
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 200);") 
        for _,value in self.df.iterrows():
            i += 1
            if i % 100 == 0:
                driver.refresh()
                time.sleep(5)
                driver.execute_script("window.scrollTo(0, 200);")
            driver.switch_to.frame(0)
            time.sleep(2)
            driver.find_element_by_xpath("//input[@id='address-input']").clear()
            # time.sleep(2)
            search_input = driver.find_element_by_xpath("//input[@id='address-input']")
            if value['location'].count("-") > 1:
                search_input.send_keys(value['location'])
            else:
                search_input.send_keys(f"{value['location']} FRANCE")
            time.sleep(2)
            search_input.send_keys(Keys.DOWN)
            time.sleep(1)
            search_input.send_keys(Keys.ENTER)
            time.sleep(5)
            scr1 = driver.find_element_by_xpath("(//div[@class='list'])[last()]/div[last()]")
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
            time.sleep(2)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")            
            
            html = driver.page_source
            resp_obj = Selector(text=html)

            # text_file = open("test.txt", "w")
            # text_file.write(html)
            # text_file.close()

            places = resp_obj.xpath("(//div[@class='list'])[last()]/div")
            print(places)

            for place in places:
                transportation_type = place.xpath(".//div[contains(@id, 'duration')]/following-sibling::div/@style").get()
                wheelChairAccess = place.xpath(".//img[@alt='icon_accessible']")
                sunday = place.xpath(".//img[@alt='icon_calendar']/parent::div/following-sibling::div/p[contains(text(), 'Dim')]")
                saturday = place.xpath(".//img[@alt='icon_calendar']/parent::div/following-sibling::div/p[contains(text(), 'Sam')]")
                oA = place.xpath("normalize-space(.//img[@alt='icon_parking']/parent::div/following-sibling::div/p[2]/text())").get()
                if oA:
                    openAfter = oA.replace("Après ", "")
                else:
                    openAfter = None
                if sunday:
                    sunday = "Available"
                else:
                    sunday = "Not Available"
                if saturday:
                    saturday = "Available"
                else:
                    saturday = "Not Available"
                if wheelChairAccess:
                    wheelChairAccess = "Available"
                else:
                    wheelChairAccess = "Not Available"
                if 'display:none' in transportation_type:
                     transportation_type = "Drive"
                else:
                    transportation_type = "Walk"
                yield{
                    'city': value['location'],
                    'name': place.xpath("normalize-space(.//div[@class='list__title-bloc-left-label txt-regular']/text())").get(),
                    'address': self.formatAddress(place.xpath(".//p[@class='list__content']/text()").getall()),
                    'duration': f'''{place.xpath("normalize-space(.//div[contains(@id, 'duration')]/text())").get()} {transportation_type}''',
                    'distance': place.xpath("normalize-space(.//div[contains(@class, 'distance')]/text())").get(),
                    'days': self.formatDay(place.xpath(".//div[contains(@class, 'schedule')]/p/text()").getall()),
                    # 'days': place.xpath(".//div[contains(@class, 'schedule')]/p/text()").getall(),
                    'openAfter': openAfter,
                    'wheelChairAccess': wheelChairAccess,
                    'Sunday': sunday,
                    'Saturday': saturday
                }
            driver.switch_to.default_content()

