import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy import Selector
import time


class AnafSpider(scrapy.Spider):
    name = 'anaf'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.anaf.ro/restante/index.xhtml",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        input()

        while True:
            driver.execute_script(f"window.scrollTo(0, 2000);")
            time.sleep(0.5)
            driver.execute_script(f"window.scrollTo(0, -2000);")
            time.sleep(0.5)
            
            html = driver.page_source
            respObj = Selector(text=html)

            tableContent = respObj.xpath("//tbody/tr")
            for rows in tableContent:
                yield{
                    'column1': f'''{rows.xpath("normalize-space(.//td[1]/text())").get()}''',
                    'column2': f'''{rows.xpath("normalize-space(.//td[2]/text())").get()}''',
                    'column3': f'''{rows.xpath("normalize-space(.//td[3]/text())").get()}''',
                    'column4': f'''{rows.xpath("normalize-space(.//td[4]/text())").get()}''',
                    'column5': f'''{rows.xpath("normalize-space(.//td[5]/text())").get()}''',
                    'column6': f'''{rows.xpath("normalize-space(.//td[6]/text())").get()}''',
                    'column7': f'''{rows.xpath("normalize-space(.//td[7]/text())").get()}''',
                    'column8': f'''{rows.xpath("normalize-space(.//td[8]/text())").get()}''',
                    'column9': f'''{rows.xpath("normalize-space(.//td[9]/text())").get()}''',
                    'column10': f'''{rows.xpath("normalize-space(.//td[10]/text())").get()}''',
                    'column11': f'''{rows.xpath("normalize-space(.//td[11]/text())").get()}''',
                    'column12': f'''{rows.xpath("normalize-space(.//td[12]/text())").get()}''',
                    'column13': f'''{rows.xpath("normalize-space(.//td[13]/text())").get()}''',
                    'column14': f'''{rows.xpath("normalize-space(.//td[14]/text())").get()}''',
                    'column15': f'''{rows.xpath("normalize-space(.//td[15]/text())").get()}''',
                    'column16': f'''{rows.xpath("normalize-space(.//td[16]/text())").get()}''',
                    'column17': f'''{rows.xpath("normalize-space(.//td[17]/text())").get()}''',
                    'column18': f'''{rows.xpath("normalize-space(.//td[18]/text())").get()}''',
                    'column19': f'''{rows.xpath("normalize-space(.//td[19]/text())").get()}''',
                    'column20': f'''{rows.xpath("normalize-space(.//td[20]/text())").get()}''',
                    'column21': f'''{rows.xpath("normalize-space(.//td[21]/text())").get()}''',
                    'column22': f'''{rows.xpath("normalize-space(.//td[22]/text())").get()}''',
                    'column23': f'''{rows.xpath("normalize-space(.//td[23]/text())").get()}''',
                    'column24': f'''{rows.xpath("normalize-space(.//td[24]/text())").get()}'''
                }


            nextPage = respObj.xpath("(//span[contains(@class, 'paginator-next')])[1]/@class").get()
            if "disabled" in nextPage:
                break
            else:
                nextButtonElem = driver.find_element_by_xpath("(//span[contains(@class, 'paginator-next')])[1]/span")
                driver.execute_script("arguments[0].click()", nextButtonElem)
                time.sleep(6)
        
