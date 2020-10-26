import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
import time


class FbadspiderSpider(scrapy.Spider):
    name = 'fbAdSpider'

    # df = pd.read_excel("D:/Web-Scrapping/UpWork_Projects/kacper/fbAdLib/Facebook Ad Library.xlsx", sheet_name='part2')

    # result = re.findall('((?:"[^"]*"|[^:,])*):((?:"[^"]*"|[^,])*)', jsonObj)
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.bsrreit.com/Locations",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        time.sleep(5)
        html = driver.page_source
        respObj = Selector(text=html)
        # print(respObj)
        with open('D:/Web-Scrapping/UpWork_Projects/kacper/fbAdLib/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
            f.close()
