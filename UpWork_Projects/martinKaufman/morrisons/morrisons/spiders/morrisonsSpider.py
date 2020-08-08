import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class MorrisonsspiderSpider(scrapy.Spider):
    name = 'morrisonsSpider'

    categoryURLs = [
        'https://groceries.morrisons.com/browse/meat-fish-179549',
        'https://groceries.morrisons.com/browse/fruit-veg-176738',
        'https://groceries.morrisons.com/browse/fresh-176739',
        'https://groceries.morrisons.com/browse/bakery-cakes-102210',
        'https://groceries.morrisons.com/browse/food-cupboard-102705',
        'https://groceries.morrisons.com/browse/frozen-180331',
        'https://groceries.morrisons.com/browse/drinks-103644'
    ]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://groceries.morrisons.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for categoryURL in self.categoryURLs:
            driver.get(categoryURL)
            
            html1 = driver.page_source
            response1 = Selector(text=html1)

            catURLs = response1.xpath("//div[contains(@class, 'level-0')]/ul/li")

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])

            for catURL in catURLs:
                url = f'''https://groceries.morrisons.com{catURL.xpath(".//a/@href").get()}'''
                driver.get(url)
                driver.execute_script("window.scrollTo(0, 1500);")
                time.sleep(3)

                html2 = driver.page_source
                response2 = Selector(text=html2)

                subCatURLs = response2.xpath("//div[contains(@class, 'level-0')]/ul/li")
                if subCatURLs:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[2])
                    for subCatURL in subCatURLs:
                        url = f'''https://groceries.morrisons.com{subCatURL.xpath(".//a/@href").get()}'''
                        driver.get(url)
                        driver.execute_script("window.scrollTo(0, 1500);")
                        time.sleep(3)

                        html3 = driver.page_source
                        response3 = Selector(text=html3)
                        products = response3.xpath("//ul[contains(@class, 'fops-shelf')]/li")
                        # driver.execute_script("window.open('');")
                        # driver.switch_to.window(driver.window_handles[3])
                        for product in products:
                            url = f'''https://groceries.morrisons.com{product.xpath(".//div[@role='presentation']/a/@href").get()}'''
                            if url != "https://groceries.morrisons.com/None":
                                yield scrapy.Request(
                                    url=url,
                                    callback=self.prodDetails,
                                    dont_filter=True
                                )
                                # driver.get(url)
                                # try:
                                #     WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h2[@class='bop-price__current ']/text()")))
                                # except:
                                #     pass
                                # html4 = driver.page_source
                                # response4 = Selector(text=html4)
                                # yield {
                                #     'productName': response4.xpath("normalize-space(//header[@class='bop-title']/h2/text())").get(),
                                #     'quantity': response4.xpath("normalize-space(//header[@class='bop-title']/h2/span/text())").get(),
                                #     'price': response4.xpath("normalize-space(//h2[@class='bop-price__current ']/text())").get(),
                                #     'img_url': response4.xpath("//img[@role='presentation']/@src").get(),
                                #     'url': driver.current_url,
                                #     'cal1': response4.xpath("//table/tbody/tr[2]/td[1]").get(),
                                #     'cal2': response4.xpath("//table/tbody/tr[2]/td[2]").get(),
                                #     'cal3': response4.xpath("//table/tbody/tr[2]/td[3]").get()
                                # }
                        # driver.close()  
                        # driver.switch_to.window(driver.window_handles[2])
                    driver.close()  
                    driver.switch_to.window(driver.window_handles[1])
                else:
                    products = response2.xpath("//ul[contains(@class, 'fops-shelf')]/li")
                    # driver.execute_script("window.open('');")
                    # driver.switch_to.window(driver.window_handles[2])
                    for product in products:
                        url = f'''https://groceries.morrisons.com{product.xpath(".//div[@role='presentation']/a/@href").get()}'''
                        if url != "https://groceries.morrisons.com/None":
                            yield scrapy.Request(
                                url=url,
                                callback=self.prodDetails,
                                dont_filter=True
                            )
                            # driver.get(url)
                            # try:
                            #         WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h2[@class='bop-price__current ']/text()")))
                            # except:
                            #     pass
                            # html4 = driver.page_source
                            # response4 = Selector(text=html4)
                            # yield {
                            #     'productName': response4.xpath("normalize-space(//header[@class='bop-title']/h2/text())").get(),
                            #     'quantity': response4.xpath("normalize-space(//header[@class='bop-title']/h2/span/text())").get(),
                            #     'price': response4.xpath("normalize-space(//h2[@class='bop-price__current ']/text())").get(),
                            #     'img_url': response4.xpath("//img[@role='presentation']/@src").get(),
                            #     'url': driver.current_url,
                            #     'cal1': response4.xpath("//table/tbody/tr[2]/td[1]").get(),
                            #     'cal2': response4.xpath("//table/tbody/tr[2]/td[2]").get(),
                            #     'cal3': response4.xpath("//table/tbody/tr[2]/td[3]").get()
                            # }

                    # driver.close()  
                    # driver.switch_to.window(driver.window_handles[1])

            driver.close()  
            driver.switch_to.window(driver.window_handles[0])

    def prodDetails(self, response):
        yield {
            'productName': response.xpath("normalize-space(//header[@class='bop-title']/h2/text())").get(),
            'quantity': response.xpath("normalize-space(//header[@class='bop-title']/h2/span/text())").get(),
            'price': response.xpath("normalize-space(//h2[@class='bop-price__current ']/text())").get(),
            'img_url': f'''https://groceries.morrisons.com{response.xpath("//img[@role='presentation']/@src").get()}''',
            'url': response.url,
            'cal1': response.xpath("//table/tbody/tr[2]/td[1]/text()").get(),
            'cal2': response.xpath("//table/tbody/tr[2]/td[2]/text()").get(),
            'cal3': response.xpath("//table/tbody/tr[2]/td[3]/text()").get()
        }
        