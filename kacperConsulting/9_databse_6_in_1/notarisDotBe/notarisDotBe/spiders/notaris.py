import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
import pandas as pd
import time


class NotarisSpider(scrapy.Spider):
    name = 'notaris'

    postCodes = pd.read_excel("./postcode.xlsx")
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.notaris.be",
            callback=self.getListings
        )

    def getListings(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        time.sleep(2)

        try:
            cookieBtnElem = driver.find_element_by_xpath("//b[contains(text(), 'cookies')]")
            driver.execute_script("arguments[0].click()", cookieBtnElem)
        except:
            pass

        time.sleep(2)
        
        for _,val in self.postCodes.iterrows():
            driver.get(f'''https://www.notaris.be/notaris/zoek/{val['code']}''')
            time.sleep(2)
            html = driver.page_source
            respObj = Selector(text=html)
            resultUrls = respObj.xpath("//div[@id='info-content']/a[@style != 'display: none;']/@href").getall()
            for url in resultUrls:
                yield scrapy.Request(
                    url=f"https://www.notaris.be{url}",
                    callback=self.parse
                )

    def parse(self, response):
        notaryInfo = response.xpath("//article[@class='notary-info']/p/text()").getall()
        btw = None
        for ni in notaryInfo:
            if sum(c.isdigit() for c in ni) > 4:
                btw = ni.strip()
        yield{
            'Name': response.xpath("normalize-space(//h1/text())").get(),
            'Kantoor': response.xpath("normalize-space(//p[contains(text(), 'Kantoor')]/a/text())").get(),
            'Kantoor Url': f'''https://www.notaris.be{response.xpath("//p[contains(text(), 'Kantoor')]/a/@href").get()}''',
            'Address 1': response.xpath("normalize-space((//a[@class='address']/text())[1])").get(),
            'Address 2': response.xpath("normalize-space((//a[@class='address']/text())[2])").get(),
            'Telephone': response.xpath("normalize-space(//a[contains(@href, 'tel')]/text())").get(),
            'Email': response.xpath("normalize-space(//a[contains(@href, 'mail')]/text())").get(),
            'Taalkennis in kantoor': response.xpath("normalize-space(//p[contains(text(), 'Taalkennis in kantoor')]/text())").get().replace("Taalkennis in kantoor:","").strip(),
            'BTW': btw,
            'Source Url': response.url
        }
