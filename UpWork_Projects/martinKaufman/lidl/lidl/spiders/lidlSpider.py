import scrapy
import time
from scrapy import Selector
from selenium.webdriver.common.action_chains import ActionChains
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LidlspiderSpider(scrapy.Spider):
    name = 'lidlSpider'
    
    pageURLs = [
        # 'https://www.lidl.co.uk/en/c/summer-meats/c1451',
        # 'https://www.lidl.co.uk/en/c/in-store-bakery/c1494?ar=7',
        # 'https://www.lidl.co.uk/en/our-products/fruit-veg?ar=7',
        # 'https://www.lidl.co.uk/en/our-products/chilled?ar=7',
        # 'https://www.lidl.co.uk/en/our-products/deluxe/deluxe-breakfast?ar=7',
        # 'https://www.lidl.co.uk/en/our-products/deluxe/deluxe-easy-meals?ar=7',
        # 'https://www.lidl.co.uk/en/our-products/deluxe/deluxe-meat-fish?ar=7',
        # 'https://www.lidl.co.uk/en/our-products/deluxe/deluxe-deli?ar=7',
        'https://www.lidl.co.uk/en/our-products/eggs?ar=7',
        'https://www.lidl.co.uk/en/our-products/frozen?ar=7',
        'https://www.lidl.co.uk/en/our-products/food-cupboard/dried',
        'https://www.lidl.co.uk/en/our-products/food-cupboard/crisps-nuts?ar=7',
        'https://www.lidl.co.uk/en/our-products/food-cupboard/breakfast?ar=7',
        'https://www.lidl.co.uk/en/our-products/food-cupboard/tin-jars?ar=7',
        'https://www.lidl.co.uk/en/our-products/free-from/gluten-free',
        'https://www.lidl.co.uk/en/our-products/free-from/vegan?ar=7',

    ]
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.lidl.co.uk",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        
        for pageURL in self.pageURLs:
            driver.get(pageURL)
            time.sleep(5)
            
            html1 = driver.page_source
            response1 = Selector(text=html1)

            products = response1.xpath("//a[@class='product__body']")

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            
            for product in products:
                if product.xpath(".//span[@class='pricebox__price']"):
                    productURL = f'''https://www.lidl.co.uk{product.xpath(".//@href").get()}'''
                    try:
                        driver.get(productURL)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='multimediabox__preview']")))
                        html2 = driver.page_source
                        response2 = Selector(text=html2)
                        yield{
                            'productName' : response2.xpath("normalize-space(//h1/text())").get(),
                            'servingSize': response2.xpath("normalize-space(//h1/following-sibling::p/text())").get(),
                            'price': response2.xpath("normalize-space(//span[@class='pricebox__price']/text())").get(),
                            'imageURL': response2.xpath("//div[@class='multimediabox__preview']/a/picture/@data-overlay").get(),
                            'url' : driver.current_url
                        }
                    except:
                        pass

            driver.close()  
            driver.switch_to.window(driver.window_handles[0])
        
