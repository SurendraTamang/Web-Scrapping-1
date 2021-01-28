import scrapy
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
from ..utils import cookie_parser


class DdsipderSpider(scrapy.Spider):
    name = 'ddSipder'

    payload = {
        'delivery_city_slug': 'seattle-wa-restaurants',
        'store_only': False,
        'limit': 50
    }

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.doordash.com/food-delivery",
            wait_time=10,
            callback=self.getCityUrls
        )

    def getCityUrls(self, response):
        driver = response.meta['driver']
        driver.set_window_size(1920, 1080)
        #driver.maximize_window()
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])

        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'MarketLinks_markets')]/div")))
        time.sleep(2)

        for i in range(1,80):            
            stateElem = driver.find_element_by_xpath(f"(//div[contains(@class, 'MarketLinks_markets')]/div/button)[{i}]")
            driver.execute_script("arguments[0].click()", stateElem)
            time.sleep(1)

            htmlInr = driver.page_source
            respObjInr = Selector(text=htmlInr)

            cities = respObjInr.xpath("//div[contains(@class, 'MarketLinks_cities')]/a")
            driver.switch_to.window(driver.window_handles[1])
            for city in cities:
                cty = city.xpath("normalize-space(.//text())").get()
                state = respObjInr.xpath(f'''normalize-space((//div[contains(@class, 'MarketLinks_markets')]/div/button)[{i}]/text())''').get()
                rawUrl = city.xpath(".//@href").get()
                apiUrl = f'''https://api.doordash.com/v2/seo_city_stores/?delivery_city_slug={rawUrl.split("/")[-2]}&store_only=false&limit=50'''

                newOffsetVal = 0
                while True:
                    driver.get(apiUrl)
                    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//pre")))
                    time.sleep(1)

                    htmlOtr = driver.page_source
                    respObjOtr = Selector(text=htmlOtr)

                    jsonText = "".join(respObjOtr.xpath("//pre/text()").getall())
                    json_resp = json.loads(jsonText)
                    stores = json_resp.get('store_data')

                    for store in stores:
                        yield{
                            'State' : state,
                            'City' : cty,
                            'Restaurant name': store.get('name'),
                            'Average rating': store.get('average_rating'),
                            'Number of reviews': store.get('num_ratings'),
                            'gSearchQuery': f'''{store.get('name')},{cty},{state}'''
                        }
                    total = json_resp.get('total')

                    if total <= 50:
                        break
                    else:
                        if newOffsetVal-50 < total:
                            if "offset" in apiUrl:
                                offsetVal = apiUrl.split("offset=")[-1]
                                newOffsetVal = int(offsetVal)+50
                                apiUrl = apiUrl.replace(f'offset={offsetVal}', f'offset={str(newOffsetVal)}')
                            else:
                                apiUrl = f"{apiUrl}&offset=50"
                        else:
                            break
            
            driver.switch_to.window(driver.window_handles[0])
