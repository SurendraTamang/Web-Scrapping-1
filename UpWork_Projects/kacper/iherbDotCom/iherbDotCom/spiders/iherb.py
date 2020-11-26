import scrapy
import time
from scrapy import Selector
from scrapy.http import headers
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class IherbSpider(scrapy.Spider):
    name = 'iherb'

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
            url="https://in.iherb.com/c/baby-kids?noi=48",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.maximize_window()
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[0])
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'language-select')]"))).click()
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='country-column'])[2]//i"))).click()
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='country-column'])[2]//div[@data-val='pt-BR']"))).click()
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Guardar preferências']"))).click()
        # WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Guardar preferências']"))).click()
        time.sleep(60)
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pagination']")))

        while True:
            html1 = driver.page_source
            respObj1 = Selector(text=html1)

            driver.switch_to.window(driver.window_handles[1])
            products = respObj1.xpath("//div[@class='products clearfix']/div//a[contains(@class, 'product-link')]")
            for product in products:
                bc = []
                driver.get(product.xpath(".//@href").get())
                try:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='thumbnail-container']/img")))
                    html2 = driver.page_source
                    respObj2 = Selector(text=html2)
                    breadCrumbs = respObj2.xpath("//a[text()='Categorias']/following-sibling::a")
                    prodImages = respObj2.xpath("//div[@class='thumbnail-container']/img/@data-large-img").getall()
                    if len(prodImages) > 3:
                        pimgStr = ",".join(prodImages[:3])
                    else:
                        pimgStr = ",".join(prodImages)
                    for breadCrumb in breadCrumbs:
                        bc.append(breadCrumb.xpath("normalize-space(.//text())").get())
                    try:
                        wrng = self.check_br(respObj2.xpath("//strong[text()='Advertências']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div class="prodOverviewDetail">''',"").strip()
                    except:
                        wrng = None
                    try:
                        otherIng = self.check_br(respObj2.xpath("//strong[text()='Outros Ingredientes']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div class="prodOverviewIngred">''',"").strip()
                    except:
                        otherIng = None
                    try:
                        descpt = self.check_br(respObj2.xpath("//strong[text()='Descrição']/parent::h3/following-sibling::div").get()[:-6]).replace('''<div itemprop="description">''',"").strip()
                    except:
                        descpt = None
                    np = respObj2.xpath("normalize-space((//div[@class='product-grouping-row'])[last()]/div/div[contains(@class, 'attribute-tile')][1]//span[contains(@class, 'price')]/bdi/text())").get()
                    bvp = respObj2.xpath("normalize-space((//div[@class='product-grouping-row'])[last()]/div/div[contains(@class, 'attribute-tile')][2]//span[contains(@class, 'price')]/bdi/text())").get()
                    if (np == "" and bvp == "") or (np == None and bvp == None):
                        np = respObj2.xpath("normalize-space(//div[@class='product-action-container']//div[contains(text(), 'Nosso preço')]/following-sibling::div[@id='price']/text())").get()
                        bvp = respObj2.xpath("normalize-space(//section[contains(@id,'price')]//b/text())").get()

                    yield{
                        'Product Name': respObj2.xpath("normalize-space(//h1[@id='name']/text())").get().replace("\xa0","").strip(),
                        'Product Image URL': pimgStr,
                        'Expiry Date': respObj2.xpath("//li[contains(text(), 'Data de validade')]/text()").getall()[1].strip(),
                        'Shipping Weight': respObj2.xpath("normalize-space(//span[@class='product-weight']/text())").get(),
                        'Product Code': respObj2.xpath("normalize-space(//span[@itemprop='sku']/text())").get(),
                        'UPC Code': respObj2.xpath("normalize-space(//li[contains(text(), 'UPC')]/span/text())").get(),
                        'Dimensions': f'''{respObj2.xpath("normalize-space(//span[@id='dimensions']/text())").get()},{respObj2.xpath("normalize-space(//span[@id='actual-weight']/text())").get()}''',
                        'Package Quantity': respObj2.xpath("normalize-space(//li[contains(text(), 'Quantidade')]/text())").get().replace("Quantidade:","").strip(),
                        'Brand Name': respObj2.xpath("normalize-space(//span[@itemprop='name']/bdi/text())").get(),
                        'Normal Quantity': respObj2.xpath("normalize-space((//div[@class='product-grouping-row'])[last()]/div/div[contains(@class, 'attribute-tile')][1]//div[@class='attribute-name']/text())").get(),
                        'Normal Price': np,
                        'Best Value Quantity': respObj2.xpath("normalize-space((//div[@class='product-grouping-row'])[last()]/div/div[contains(@class, 'attribute-tile')][2]//div[@class='attribute-name']/text())").get(),
                        'Best Value price': bvp,
                        'Breadcrumbs': f'''{respObj2.xpath("normalize-space(//a[text()='Categorias']/text())").get()},{",".join(bc)}''',
                        'Warning': wrng,
                        'Other Ingrediants': otherIng,
                        'Description': descpt,
                        'Product url': product.xpath(".//@href").get(),
                    }
                except:
                    yield{
                        'Product Name': None,
                        'Product Image URL': None,
                        'Expiry Date': None,
                        'Shipping Weight': None,
                        'Product Code': None,
                        'UPC Code': None,
                        'Dimensions': None,
                        'Package Quantity': None,
                        'Brand Name': None,
                        'Normal Quantity': None,
                        'Normal Price': None,
                        'Best Value Quantity': None,
                        'Best Value price': None,
                        'Breadcrumbs': None,
                        'Warning': None,
                        'Other Ingrediants': None,
                        'Description': None,
                        'Product url': product.xpath(".//@href").get(),
                    }
            driver.switch_to.window(driver.window_handles[0])
            nextPage = respObj1.xpath("//a[@class='pagination-next']/@href").get()
            if nextPage:
                driver.get(f'https://www.iherb.com{nextPage}')
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='pagination']")))
                time.sleep(1)
            else:
                break

