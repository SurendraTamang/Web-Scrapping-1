# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import time

class BoroondaraSpiderSpider(scrapy.Spider):
    name = 'boroondara_spider'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://eservices.boroondara.vic.gov.au/EPlanning/Common/Common/terms.aspx",
            wait_time=5,
            callback=self.parse
        ) 

    def parse(self, response):
        cntr = True
        driver = response.meta['driver']
        driver.find_element_by_xpath("//input[@value='I Agree']").click()
        time.sleep(6)
        driver.find_element_by_xpath("//a[text()='Recent applications']").click()
        time.sleep(6)

        #main_window = browser.current_window_handle
        html = driver.page_source
        response_obj = Selector(text=html)

        url_list = [
            f'''https://eservices.boroondara.vic.gov.au/EPlanning/Pages/XC.Track/{response_obj.xpath("(//a[text()='Last Month']/@href)[1]").get()}''',
            f'''https://eservices.boroondara.vic.gov.au/EPlanning/Pages/XC.Track/{response_obj.xpath("(//a[text()='Last Month']/@href)[2]").get()}'''
        ]

        for url in url_list:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url)
            time.sleep(6)

            while cntr:
                html1 = driver.page_source
                response_obj1 = Selector(text=html1)
                listings = response_obj1.xpath("//div[@class='MainPanel']/h4")
                for lists in listings:
                    app_url = f'''https://eservices.boroondara.vic.gov.au/EPlanning/Pages/XC.Track/{lists.xpath(".//a/@href").get()}'''
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[2])
                    driver.get(app_url)
                    time.sleep(3)
                    html2 = driver.page_source
                    response_obj2 = Selector(text=html2)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])    

                    # yield{            
                    #     'appNum': self.remove_nonUTF_char(response.xpath("normalize-space(//h1/text())").get()),
                    #     'nameLGA': 'Boroondara',
                    #     'codeLGA': '21110',
                    #     'address': self.remove_nonUTF_char(response.xpath("normalize-space(//div[text()='Properties:']/following-sibling::div/a/text())").get()),
                    #     'activity': self.remove_nonUTF_char(response.xpath("normalize-space(//div[text()='Description:']/following-sibling::div/text())").getall()),
                    #     'applicant': self.remove_nonUTF_char(response.xpath("normalize-space(//div[text()='Officer:']/following-sibling::div/text())").get()),
                    #     'lodgeDate': self.convert_dateTime(response.xpath("normalize-space(//div[text()='Submitted:']/following-sibling::div/text())").get()),
                    #     'decisionDate': self.convert_dateTime(response.xpath("normalize-space(//div[text()='Decision:']/following-sibling::div/text())").get()),
                    #     'status': self.remove_nonUTF_char(response.xpath("normalize-space(//div[text()='Status:']/following-sibling::div/strong/text())").get()),
                    #     'url' : app_url           
                    # }

                driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(5)