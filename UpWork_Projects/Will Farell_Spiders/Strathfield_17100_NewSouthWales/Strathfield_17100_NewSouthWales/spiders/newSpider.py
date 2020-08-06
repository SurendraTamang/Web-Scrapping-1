import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import time



class NewspiderSpider(scrapy.Spider):
    name = 'newSpider'
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
    
    def format_status(self, value):
        try:
            li = value.split(" ")
            return li[0]
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
            while True:
                html = driver.page_source
                resp_obj = Selector(text=html)
                listings = resp_obj.xpath("//div[@id='searchresult']/div")
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                for lists in listings:              
                    url = self.gen_url(lists.xpath(".//a[@class='search']/@href").get())
                    activity = lists.xpath("normalize-space(.//a[@class='search']/parent::div/a/following-sibling::br/following-sibling::text())").get()
                    appNum = lists.xpath("normalize-space(.//a[@class='search']/text())").get()
                    lodged = lists.xpath("normalize-space(.//div[contains(@id, 'More')]/text())").get()
                    if activity.strip() == "Details -":
                        activity_new = None
                    else:
                        activity_new = activity.replace("Details - ", "").strip()
                    driver.get(url)
                    html_new = driver.page_source
                    resp_obj_new = Selector(text=html_new)
                    decisionDate = resp_obj_new.xpath("normalize-space(//div[text()='Decision']/following-sibling::div/text())").get()
                    applicant = resp_obj_new.xpath("normalize-space(//div[text()='Applicant']/following-sibling::div/text())").get()
                    yield{
                        'appNum': appNum,
                        'nameLGA': 'Strathfield',
                        'codeLGA': '17100',
                        'address': resp_obj_new.xpath("normalize-space(//div[text()='Location']/following-sibling::div/a/text())").get(),
                        'activity': activity_new,
                        'applicant': applicant.replace("Applicant - ", ""),
                        'lodgeDate': self.format_dateTime(lodged[8:18]),
                        'decisionDate': self.format_dateTime(decisionDate.replace("Determined: ", "")),
                        'status': self.format_status(resp_obj_new.xpath("normalize-space(//div[@class='detailright']/strong/text())").get()),
                        'url': url
                    }
                driver.close()  
                driver.switch_to.window(driver.window_handles[0])
                cntr += 1
                next_page = resp_obj.xpath(f"//a[text()={cntr}]")
                if next_page:
                    driver.find_element_by_xpath(f"//a[text()={cntr}]").click()
                    time.sleep(6)
                else:
                    break