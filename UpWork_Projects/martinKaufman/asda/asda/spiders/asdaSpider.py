# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AsdaspiderSpider(scrapy.Spider):
    name = 'asdaSpider'

    categoryURLs=[
        'https://groceries.asda.com/cat/fresh-food-bakery/103099',
        'https://groceries.asda.com/cat/chilled-food/111621',
        'https://groceries.asda.com/cat/food-cupboard/102870',
        'https://groceries.asda.com/cat/frozen-food/103478',
        'https://groceries.asda.com/cat/vegan-free-from/918746879',
        'https://groceries.asda.com/cat/drinks/102436'
    ]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://groceries.asda.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for categoryURL in self.categoryURLs:
            driver.get(categoryURL)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'explore')]/a")))
            time.sleep(2)
            html1 = driver.page_source
            response1 = Selector(text=html1)

            categories = response1.xpath("//ul[contains(@class, 'explore')]/a")

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])

            for category in categories:
                lvl1Cat = category.xpath("normalize-space(.//text())").get()
                driver.get(f'''https://groceries.asda.com{category.xpath(".//@href").get()}''')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//ul[contains(@class, 'explore')]/a")))
                time.sleep(2)
                html2 = driver.page_source
                response2 = Selector(text=html2)

                subCategories = response2.xpath("//ul[contains(@class, 'explore')]/a")

                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[2])

                for subCategory in subCategories:
                    lvl2Cat = subCategory.xpath("normalize-space(.//text())").get()
                    driver.get(f'''https://groceries.asda.com{subCategory.xpath(".//@href").get()}''')
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//ul[@class=' co-product-list__main-cntr']")))
                    time.sleep(2)
                    elem = driver.find_element_by_xpath("//div[@class='page-navigation']")
                    driver.execute_script("arguments[0].scrollIntoView();", elem)
                    time.sleep(3)
                    html3 = driver.page_source
                    response3 = Selector(text=html3)

                    lvl3Cat = response3.xpath("normalize-space(//h1/text())").get()
                    products = response3.xpath("(//ul[@class=' co-product-list__main-cntr'])[1]/li")

                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[3])

                    for product in products:
                        driver.get(f'''https://groceries.asda.com{product.xpath(".//h3/a/@href").get()}''')
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='s7staticimage']/img")))
                        html4 = driver.page_source
                        response4 = Selector(text=html4)
                        calories = response4.xpath("//div[contains(text(), 'kcal')]/following-sibling::div/text()").get()
                        if calories == "" or calories == None:
                            calories = response4.xpath("//div[contains(text(), 'kcal')]/text()").get()
                        yield {
                            'Name of Food Item': response4.xpath("normalize-space(//h1/text())").get(),
                            'Serving Size of Food Item': response4.xpath("normalize-space(//div[contains(@class, 'nutrition-row--title')]/div[2]/text())").get(),
                            'Price': response4.xpath("normalize-space(//div[@class='pdp-main-details__price-container']/strong/text())").get(),
                            'Number of Calories Per Serving': calories,
                            'Image (link)': response4.xpath("//div[@class='s7staticimage']/img/@src").get(),
                            'Product (link)': driver.current_url,
                            'Quantity': response4.xpath("normalize-space(//div[contains(@class, 'weight')]/text())").get(),
                            'Lvl1 Category': lvl1Cat,
                            'Lvl2 Category': lvl2Cat,
                            'Lvl3 Category': lvl3Cat
                        }

                    driver.close()  
                    driver.switch_to.window(driver.window_handles[2])
                
                driver.close()  
                driver.switch_to.window(driver.window_handles[1])

            driver.close()  
            driver.switch_to.window(driver.window_handles[0])