# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time


class Strathfield17100Spider(scrapy.Spider):
    name = 'Strathfield_17100'

    urls = [
        'http://daenquiry.strathfield.nsw.gov.au/Pages/XC.Track/SearchApplication.aspx?d=thismonth&k=DeterminationDate&t=',
        'http://daenquiry.strathfield.nsw.gov.au/Pages/XC.Track/SearchApplication.aspx?d=thismonth&k=LodgementDate&t='
    ]

    def gen_url(self, value):
        return f'''http://daenquiry.strathfield.nsw.gov.au/{value.strip("../..")}'''

    def format_dateTime(self, value):
        try:
            return datetime.datetime.strptime(value, '%d/%m/%Y').date()
        except:
            return None
    
    def start_requests(self):
        yield SeleniumRequest(
            url="http://daenquiry.strathfield.nsw.gov.au/Common/Common/terms.aspx",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='I Agree']"))).click()
        #time.sleep(5)

        for url in self.urls:
            cntr = 1
            driver.get(url)
            time.sleep(3)
            # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='searchresult']/div")))
            while True:
                html = driver.page_source
                resp_obj = Selector(text=html)
                listings = resp_obj.xpath("//div[@id='searchresult']/div")
                #time.sleep(3)
                
                #time.sleep(3)                
                
                #time.sleep(3)
                for lists in listings:
                    # driver.execute_script("window.open('');")
                    # driver.switch_to.window(driver.window_handles[1])
                    url = self.gen_url(lists.xpath(".//a[@class='search']/@href").get())
                    activity = lists.xpath("normalize-space(.//a[@class='search']/parent::div/text()[last()])").get()
                    appNum = lists.xpath("normalize-space(.//a[@class='search']/text())").get()
                    lodged = lists.xpath("normalize-space(.//div[contains(@id, 'More')]/text())").get()
                    if activity.strip() == "Details -":
                        activity_new = None
                    else:
                        activity_new = activity.replace("Details - ", "").strip()

                    # yield scrapy.Request(
                    #     url=url,
                    #     callback=self.get_data
                    # )
                    #driver.set_page_load_timeout(6)                    
                    # try:
                    #driver.get(url)
                    #time.sleep(8)
                    #driver.execute_script("window.stop();")
                    #except:
                    #pass
                    #time.sleep(3)
                    # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//input[@value='Location']")))
                    # html_new = driver.page_source
                    # resp_obj_new = Selector(text=html_new)
                    yield{
                        'appNum': appNum,
                        'nameLGA': 'Strathfield',
                        'codeLGA': '17100',
                        #'address': resp_obj_new.xpath("normalize-space(//div[text()='Location']/following-sibling::div/a/text())").get(),
                        'address': None,
                        'activity': activity_new,
                        #'applicant': resp_obj_new.xpath("normalize-space(//div[text()='Applicant']/following-sibling::div/text())").get(),
                        'applicant': None,
                        #'lodgeDate': self.format_dateTime(lists.xpath("normalize-space(//*[@id='b_ctl00_ctMain_info_app']/text()[3])").get()),
                        'lodgeDate': self.format_dateTime(lodged.lstrip("Lodged: ")),
                        'decisionDate': None,
                        #'status': resp_obj_new.xpath("normalize-space(//div[@class='detailright']/strong/text())").get(),
                        'status': None,
                        'url': url
                    }

                # driver.close()  
                # driver.switch_to.window(driver.window_handles[0])
                cntr += 1
                next_page = resp_obj.xpath(f"//a[text()={cntr}]")
                if next_page:
                    driver.find_element_by_xpath(f"//a[text()={cntr}]").click()
                    time.sleep(6)
                else:
                    break
                
            
