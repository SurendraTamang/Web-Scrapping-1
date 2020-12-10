# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy import Selector
import pandas as pd
import time


class MvsabcSpider(scrapy.Spider):
    name = 'mvsabc'

    df = pd.read_excel("D:/sipun/Web-Scrapping/UpWork_Projects/kacper/mvsabcRegistry/cities.xlsx")
    cities = df['city'].tolist()

    def start_requests(self):
        yield SeleniumRequest(
            url="https://publicregistry.mvsabc.com/Pages/en_US/Forms/Public/Register/Default.aspx?ReturnUrl=%2f",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        cntr = 0
        driver = response.meta['driver']
        driver.maximize_window()
        
        for city in self.cities:
            driver.get(f'''https://publicregistry.mvsabc.com/Pages/en_US/Forms/Public/Register/Search.aspx?dealerLicenceNo=&dealerName=&dealerCity={city.replace(" ","%20")}&searchType=dealership&searchFrom=publicSearch&businessType=1''')
            time.sleep(2)
            # driver.get("https://publicregistry.mvsabc.com/Pages/en_US/Forms/Public/Register/Search.aspx?dealerLicenceNo=&dealerName=&dealerCity=Coquitlam&searchType=dealership&searchFrom=publicSearch&businessType=1")

            while True:
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[contains(@id, 'BodyContent')]")))
                except:
                    break

                html1 = driver.page_source
                respObj1 = Selector(text=html1)

                cntr += 1
                bNames = respObj1.xpath("//tbody/tr[contains(@id, 'BodyContent')]")
                for bName in bNames:
                    bidRaw = bName.xpath(".//td/a/@href").get()
                    filter1 = bidRaw.replace("/Pages/en_US/Forms/Public/Register/Search.aspx?eId=", "")
                    bID = filter1.replace("&searchType=salesperson&searchFrom=dealerShipResults&businessType=1","")                

                    yield scrapy.Request(
                        url=f'''https://publicregistry.mvsabc.com/Pages/en_US/Forms/Public/Register/View.aspx?id={bID}&dealerLicenceNo=&dealerName=&dealerCity=Coquitlam&searchType=dealership&searchFrom=publicSearch&pageNumber=0&businessType=1''',
                        callback=self.getBusinessDetails,
                        meta={
                            'bssnName': bName.xpath("normalize-space(.//td[1]/text())").get(),
                            'licsNo': bName.xpath("normalize-space(.//td[2]/text())").get(),
                            'City': bName.xpath("normalize-space(.//td[3]/text())").get(),
                        }
                    )
                pages = respObj1.xpath("//div[contains(@class, 'rgNumPart')]/a/span/text()").getall()
                if cntr != len(pages):
                    driver.find_element_by_xpath(f"(//div[contains(@class, 'rgNumPart')]/a/span)[{cntr+1}]").click()
                    time.sleep(3)
                else:
                    cntr = 0
                    break

    def getBusinessDetails(self, response):
        address = response.xpath("//span[contains(@id, 'address')]/text()").getall()
        conditions = response.xpath("//span/div[contains(text(), 'Condition')]/text()[last()]").getall()
        try:
            condF1 = conditions[0].replace("Condition :", "")
            condF11 = condF1.replace("\n", "")
            cond1 = condF11.replace("Issued pending:", "").strip()
        except:
            cond1 = None
        try:
            condF2 = conditions[1].replace("Condition :", "")
            condF22 = condF2.replace("\n", "")
            cond2 = condF22.replace("Issued pending:", "").strip()
        except:
            cond2 = None
        try:
            condF3 = conditions[2].replace("Condition :", "")
            condF33 = condF3.replace("\n", "")
            cond3 = condF33.replace("Issued pending:", "").strip()
        except:
            cond3 = None
        try:
            condF4 = conditions[3].replace("Condition :", "")
            condF44 = condF4.replace("\n", "")
            cond4 = condF44.replace("Issued pending:", "").strip()
        except:
            cond4 = None
        try:
            condF5 = conditions[4].replace("Condition :", "")
            condF55 = condF5.replace("\n", "")
            cond5 = condF55.replace("Issued pending:", "").strip()
        except:
            cond5 = None
        yield{
            'Legal Name': response.xpath("normalize-space(//span[contains(@id, 'legalName')]/text())").get(),
            'Trade Name': response.xpath("normalize-space(//span[contains(@id, 'TradeName')]/text())").get(),
            'Reg No': str(response.xpath("normalize-space(//span[contains(@id, 'registrationNo')]/text())").get()),
            'Address': ", ".join(addr.strip() for addr in address),
            'Phone No': str(response.xpath("normalize-space(//span[contains(@id, 'phoneNumber')]/text())").get()),
            'Fax': response.xpath("normalize-space(//span[contains(@id, 'fax')]/text())").get(),
            'Website': response.xpath("normalize-space(//span[contains(@id, 'webSite')]/text())").get(),
            'Email': response.xpath("normalize-space(//span[contains(@id, 'email')]/text())").get(),
            'License Expiry': response.xpath("normalize-space(//span[contains(@id, 'licExpiry')]/text())").get(),
            'Category': response.xpath("normalize-space(//span[contains(@id, 'category')]/text())").get(),
            'Status': response.xpath("normalize-space(//span[contains(@id, 'Status')]/text())").get(),
            'Condition 1': cond1,
            'Condition 2': cond2,
            'Condition 3': cond3,
            'Condition 4': cond4,
            'Condition 5': cond5,
            'Page Url': response.url
        }
