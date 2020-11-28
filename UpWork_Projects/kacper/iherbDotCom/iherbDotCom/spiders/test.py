import scrapy
import time
from scrapy import Selector
from scrapy.http import headers
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestSpider(scrapy.Spider):
    name = 'test'

    urls = [
        'https://www.iherb.com/pr/Naturally-Fresh-Spray-Mist-Body-Deodorant-4-fl-oz-120-ml/5966',
        'https://www.iherb.com/pr/Sai-Baba-Super-Hit-Incense-15-g/15442',
        'https://www.iherb.com/pr/Naturally-Fresh-Deodorant-Crystal-Roll-On-Fragrance-Free-3-fl-oz-90-ml/5971'
    ]
    
    def check_br(self, val):
        try:
            if val.endswith('<br>'):
                return val.rstrip(">").rstrip("<br")
            else:
                return val
        except:
            return val

    def start_requests(self):
        yield SeleniumRequest(
            # url="https://www.iherb.com",
            url="https://www.iherb.com/c/Bath-Personal-Care?noi=48",
            wait_time=5,
            callback=self.parse
        )
    
    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        input()

        for url in self.urls:
            bc = []
            driver.get(url)
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='thumbnail-container']/img")))
            except:
                pass
            html2 = driver.page_source
            respObj2 = Selector(text=html2)

            try:
                wrngi = self.check_br(respObj2.xpath("//strong[text()='Advertências']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div class="prodOverviewDetail">''',"").strip()
                wrng = wrngi.replace("\n", "")
            except:
                wrng = None
            try:
                otherIngi = self.check_br(respObj2.xpath("//strong[text()='Outros Ingredientes']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div class="prodOverviewIngred">''',"").strip()
                otherIng = otherIngi.replace("\n", "")
            except:
                otherIng = None
            try:
                descpti = self.check_br(respObj2.xpath("//strong[text()='Descrição']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div itemprop="description">''',"").strip()
                descpt = descpti.replace("\n", "")
            except:
                descpt = None
            yield{
                'Warning': wrng,
                'Oth Ing': otherIng,
                'Dsc': descpt
            }