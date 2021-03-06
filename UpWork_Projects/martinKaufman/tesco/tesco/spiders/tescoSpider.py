import scrapy
import requests


class TescospiderSpider(scrapy.Spider):
    name = 'tescoSpider'
    
    categoryURLs = [
        # 'https://www.tesco.com/groceries/en-GB/shop/fresh-food/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/bakery/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/frozen-food/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/drinks/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/easter/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/pets/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/household/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/home-and-ents/all',
        'https://www.tesco.com/groceries/en-GB/shop/baby/all'
    ]

    # def servSize(self, value):
    #     try:
    #         result = value.replace("Pack size: ", "")
    #         return result
    #     except:
    #         return None

    def start_requests(self):
        for categoryURL in self.categoryURLs:
            yield scrapy.Request(
                url=f"{categoryURL}?page=1&count=48",
                callback=self.productListings
            )

    def productListings(self, response):
        products = response.xpath("//ul[contains(@class,'product-list')]/li")
        for product in products:
            productURL = f'''https://www.tesco.com{product.xpath(".//h3/a/@href").get()}'''
            yield scrapy.Request(
                url=productURL,
                callback=self.parse
            )
        next_page = response.xpath("(//li[@class='pagination-btn-holder'])[last()]/a/@href").get()
        # print("=======================================================")
        # print(pagination_count)
        # print()
        # print(pageEnd)
        # print()
        # print(next_page)
        # print("=======================================================")
        if next_page:
            yield scrapy.Request(
                url=f"https://www.tesco.com{next_page}",
                callback=self.productListings
            )
    
    def parse(self, response):
        name = response.xpath("normalize-space(//h1/text())").get()
        imgUrl = response.xpath("//div[contains(@class,'clickable')]/div/img/@src").get()

        # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45"
        # img_bytes = requests.get(imgUrl, headers={'User-Agent': user_agent}).content
        
        # with open(f"./Images/{name}.jpeg", 'wb') as img_file:
        #     img_file.write(img_bytes)

        yield {
            'Product ID': response.url.split("/")[-1],
            'Product Name': name,
            'Price': f'''?? {response.xpath("//div[@class='price-control-wrapper']//span[@data-auto='price-value']/text()").get()}''',
            'Lvl1 Category': response.xpath("normalize-space(//ol/li[2]//span/text())").get(),
            'Lvl2 Category': response.xpath("normalize-space(//ol/li[3]//span/text())").get(),
            'Lvl3 Category': response.xpath("normalize-space(//ol/li[4]//span/text())").get(),
            'Image URL': imgUrl
        }
        





















        # energy = response.xpath("normalize-space(//table/tbody//td[contains(text(), 'Energy')]/text())").get()
        # calories = response.xpath("normalize-space(//table/tbody//td[contains(text(), 'Energy')]/following-sibling::td/text())").get()
        # sSize = response.xpath("normalize-space(//table/thead/tr/th[2])").get()
        # quantity = self.servSize(response.xpath("normalize-space(//li[contains(text(), 'Pack size')]/text())").get())
        # if quantity == "" or quantity == None:
        #     quantity = response.xpath("//h3[contains(text(), 'Contents')]/following-sibling::p/text()").get()
        # if (energy == "" or energy == None) and (calories == "" or calories == None):
        #     sSize = ""

        # name = response.xpath("normalize-space(//h1/text())").get()
        # price = response.xpath("normalize-space(//span[@data-auto='price-value']/text())").get()
        
        # if price == "":
        #     price = "Out of stock"
        # yield {
        #     'Name of Food Item': name,
        #     'Price': price,
        #     'Serving Size of Food Item': sSize,
        #     'Energy': energy,
        #     'Number of Calories Per Serving': calories,
        #     'Image (link)': response.xpath("//div[contains(@class,'clickable')]/div/img/@src").get(),
        #     'Product (link)': response.url,
        #     'Lvl1 Category': response.xpath("normalize-space(//ol/li[2]//span/span/text())").get(),
        #     'Lvl2 Category': response.xpath("normalize-space(//ol/li[3]//span/span/text())").get(),
        #     'Lvl3 Category': response.xpath("normalize-space(//ol/li[4]//span/span/text())").get(),
        #     'Total Quantity Per Package': quantity
        # }
