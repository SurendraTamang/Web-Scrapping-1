# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import time
import datetime

class BoroondaraSpiderSpider(scrapy.Spider):
    name = 'boroondara_spider'

    def remove_nonUTF_char(self, value):
        try:
            filter1 = value.replace('\n', ' ').replace('\r', '')
            return filter1
        except:
            return None

    def format_dateTime(self, value):
        try:
            return datetime.datetime.strptime(str(value), '%d/%m/%Y').date()
        except:
            return None

    def activity_filter(self, value):
        act_list = []
        try:
            for item in value:
                act_list.append(self.remove_nonUTF_char(item))
            return f"{' '.join([str(i) for i in act_list])}"
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://eservices.boroondara.vic.gov.au/EPlanning/Common/Common/terms.aspx",
            wait_time=5,
            callback=self.parse
        ) 

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        driver.find_element_by_xpath("//input[@value='I Agree']").click()
        time.sleep(6)
        driver.find_element_by_xpath("//a[text()='Recent applications']").click()
        time.sleep(6)

        html = driver.page_source
        response_obj = Selector(text=html)

        url_list = [
            f'''https://eservices.boroondara.vic.gov.au/EPlanning/Pages/XC.Track/{response_obj.xpath("(//a[text()='This Month']/@href)[1]").get()}''',
            f'''https://eservices.boroondara.vic.gov.au/EPlanning/Pages/XC.Track/{response_obj.xpath("(//a[text()='This Month']/@href)[2]").get()}'''
        ]

        for url in url_list:
            cntr = True
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url)
            time.sleep(6)
            inc_var = 1

            while cntr:
                inc_var += 1
                html1 = driver.page_source
                response_obj1 = Selector(text=html1)
                listings = response_obj1.xpath("//div[@class='MainPanel']/h4")
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[2])
                for lists in listings:
                    app_url = f'''https://eservices.boroondara.vic.gov.au/EPlanning/Pages/XC.Track/{lists.xpath(".//a/@href").get()}'''                    
                    driver.get(app_url)
                    html2 = driver.page_source
                    response_obj2 = Selector(text=html2)
                    lDate = self.remove_nonUTF_char(response_obj2.xpath("normalize-space(//div[text()='Submitted:']/following-sibling::div/text())").get()),
                    dDate = self.remove_nonUTF_char(response_obj2.xpath("normalize-space(translate(//div[text()='Decision:']/following-sibling::div/text(), '\xa0', ''))").get())
                    yield{            
                        'appNum': self.remove_nonUTF_char(response_obj2.xpath("normalize-space(translate(//h1/text(), 'Reference number: ', ''))").get()),
                        'nameLGA': 'Boroondara',
                        'codeLGA': '21110',
                        'address': self.remove_nonUTF_char(response_obj2.xpath("normalize-space(//div[text()='Properties:']/following-sibling::div/a/text())").get()),
                        'activity': self.activity_filter(response_obj2.xpath("//div[text()='Description:']/following-sibling::div/text()").getall()),
                        'applicant': self.remove_nonUTF_char(response_obj2.xpath("normalize-space(//div[text()='Officer:']/following-sibling::div/text())").get()),
                        'lodgeDate': self.format_dateTime(lDate[0]),
                        'decisionDate': self.format_dateTime(dDate),
                        'status': self.remove_nonUTF_char(response_obj2.xpath("normalize-space(//div[text()='Status:']/following-sibling::div/strong/text())").get()),
                        'url' : app_url           
                    }
                driver.close()
                driver.switch_to.window(driver.window_handles[1])

                next_page = response_obj1.xpath(f"//strong/following-sibling::a[text()={inc_var}]")
                if next_page:
                    driver.find_element_by_xpath(f"//strong/following-sibling::a[text()={inc_var}]").click()
                    time.sleep(3)
                else:
                    cntr = False

            driver.close()
            driver.switch_to.window(driver.window_handles[0])