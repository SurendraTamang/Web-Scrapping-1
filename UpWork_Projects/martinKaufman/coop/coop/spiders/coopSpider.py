# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class CoopspiderSpider(scrapy.Spider):
    name = 'coopSpider'
    
    categoryURLs = [
        'https://quickshop.coop.co.uk/category/0600',
        'https://quickshop.coop.co.uk/category/0700',
        'https://quickshop.coop.co.uk/category/0800',
        'https://quickshop.coop.co.uk/category/0900',
        'https://quickshop.coop.co.uk/category/0950',
        'https://quickshop.coop.co.uk/category/0975',
        'https://quickshop.coop.co.uk/category/01000',
        'https://quickshop.coop.co.uk/category/01200',
        'https://quickshop.coop.co.uk/category/01300',
        'https://quickshop.coop.co.uk/category/01500',
        'https://quickshop.coop.co.uk/category/01800',
        'https://quickshop.coop.co.uk/category/01400'
    ]

    def extractImgUrl(self, value):
        try:
            li = value.split(" ")
            return "".join(i for i in li[len(li)-2])
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.coop.co.uk",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        for categoryURL in self.categoryURLs:
            driver.get(categoryURL)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='category-list']/div")))
            time.sleep(2)
            try:
                driver.find_element_by_xpath("//button[text()='Accept and close']").click()
            except:
                pass            

            html1 = driver.page_source
            response1 = Selector(text=html1)

            lvl1Cat = response1.xpath("//h1/text()").get()
            subCatURLs = response1.xpath("//div[@class='category-list']/div")

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            
            for subCatURL in subCatURLs:
                driver.get(f'''https://quickshop.coop.co.uk{subCatURL.xpath(".//a/@href").get()}''')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//article[@class='product-card']")))
                time.sleep(2)

                # Handling Pagination
                while True:
                    html2 = driver.page_source
                    response2 = Selector(text=html2)
                    nextPage = response2.xpath("//button[text()='Show more products']")
                    if nextPage:
                        driver.find_element_by_xpath("//button[text()='Show more products']").click()
                        time.sleep(5)
                    else:
                        break

                lvl2Cat = response2.xpath("//h1/text()").get()
                products = response2.xpath("//article[@class='product-card']")
                
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[2])                
                
                for product in products:
                    try:
                        driver.get(f'''https://quickshop.coop.co.uk{product.xpath(".//a/@href").get()}''')
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//section[@class='product-view--image']/img")))
                        time.sleep(1)
                        html3 = driver.page_source
                        response3 = Selector(text=html3)
                        #calories = response3.xpath("//dd/text()").get()
                        yield {
                            'Name of Food Item': response3.xpath("normalize-space(//h1/text())").get(),
                            'Serving Size of Food Item': response3.xpath("//h3[contains(text(), 'Nutritional values')]/text()").get(),
                            'Price': response3.xpath("normalize-space(//span[@class='product-view--price']/text())").get(),
                            'Number of Calories Per Serving': response3.xpath("//dd/text()").get(),
                            'Image (link)': self.extractImgUrl(response3.xpath("//section[@class='product-view--image']/img/@srcset").get()).replace("1280w,", ""),
                            'Product (link)': driver.current_url,
                            'Quantity': response3.xpath("//h3[text()='Weight']/following-sibling::p/text()").get(),
                            'Lvl1 Category': lvl1Cat,
                            'Lvl2 Category': lvl2Cat
                        }
                    except:
                        pass
                
                driver.close()  
                driver.switch_to.window(driver.window_handles[1])            
            driver.close()  
            driver.switch_to.window(driver.window_handles[0])
