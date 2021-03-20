import scrapy
import csv


class TescospiderSpider(scrapy.Spider):
    name = 'tescoSpider'
    Product_ID = []
    categoryURLs = [
        # 'https://www.tesco.com/groceries/en-GB/shop/fresh-food/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/bakery/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/frozen-food/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/food-cupboard/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/drinks/all',
        'https://www.tesco.com/groceries/en-GB/shop/easter/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/health-and-beauty/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/pets/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/household/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/home-and-ents/all',
        # 'https://www.tesco.com/groceries/en-GB/shop/baby/all'
    ]

    # with open('tescoGrocery.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')
    #     for indx,pid in enumerate(csv_reader):
    #         if indx != 0:
    #             Product_ID.append(pid[0])

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
            if productURL.split("/")[-1] not in self.Product_ID:
                yield scrapy.Request(
                    url=productURL,
                    callback=self.parse
                )
        next_page = response.xpath("(//li[@class='pagination-btn-holder'])[last()]/a/@href").get()
        if next_page:
            yield scrapy.Request(
                url=f"https://www.tesco.com{next_page}",
                callback=self.productListings
            )
    
    def parse(self, response):
        imgUrl = response.xpath("//div[contains(@class,'clickable')]/div/img/@src").get()
        if imgUrl:
            imgUrl = imgUrl.split("?")[0]
        
        postContentLi = []
        
        product_desc = response.xpath("//div[@id='product-description']//ul[contains(@class, 'product-info')]/li/text()").getall()
        if product_desc:
            postContentLi.append("<br>".join(i.strip() for i in product_desc if i))
        
        product_marketing = response.xpath("//div[@id='product-marketing']//ul[contains(@class, 'product-info')]/li/text()").getall()        
        if product_marketing:
            postContentLi.append("<br>".join(i.strip() for i in product_marketing if i))
        
        brand_marketing = response.xpath("//div[@id='brand-marketing']//ul[contains(@class, 'product-info')]/li/text()").getall()
        if brand_marketing:
            postContentLi.append("<br>".join(i.strip() for i in brand_marketing if i))
        
        other_information = response.xpath("//div[@id='other-information']//ul[contains(@class, 'product-info')]/li/text()").getall()
        if other_information:
            postContentLi.append("<br>".join(i.strip() for i in other_information if i))
        
        product_features = response.xpath("//div[@id='features']//ul[contains(@class, 'product-info')]/li/text()").getall()
        if product_features:
            postContentLi.append("<br>".join(i.strip() for i in product_features if i))
        
        pack_size = response.xpath("//div[@id='pack-size']//ul[contains(@class, 'product-info')]/li/text()").get()
        weight = None
        if pack_size:
            weight = pack_size.replace("Pack size:","").strip()
            postContentLi.append(pack_size)

        postContent = None
        if postContentLi:
            postContent = f'''<p>{"<br><br>".join(postContentLi)}</p>'''.replace("\n","<br>")

        # lvl1Category = response.xpath("normalize-space(//ol/li[2]//span/text())").get()
        lvl1Category = "Easter"
        lvl2Category = response.xpath("normalize-space(//ol/li[3]//span/text())").get()
        lvl3Category = response.xpath("normalize-space(//ol/li[4]//span/text())").get()

        regularPrice = response.xpath("normalize-space(//div[@class='price-control-wrapper']//span[@data-auto='price-value']/text())").get()
        if regularPrice and regularPrice != "NaN":
            stockStatus = 'instock'
        else:
            regularPrice = None
            stockStatus = 'outofstock'

        yield {
            'post_title': response.xpath("normalize-space(//h1/text())").get(),
            'post_name': response.xpath("normalize-space(//h1/text())").get(),
            'post_content': postContent,
            'post_status': 'publish',
            'sku': response.url.split("/")[-1],
            'downloadable': 'No',
            'virtual': 'No',
            'visibility': 'visible',
            'stock_status': stockStatus,
            'backorders': 'no',
            'manage_stock': 'no',
            'regular_price': regularPrice,
            'sale_price': None,
            'weight': weight,
            'tax_status': 'taxable',            
            'Images': imgUrl,
            'tax:product_type': 'variable',
            'tax:product_cat': f'''{lvl1Category}|{lvl2Category}>{lvl3Category}''',
            'tax:product_tag': None,
            'tax:product_brand': None
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
