import scrapy
import csv


class TescowoocomSpider(scrapy.Spider):
    name = 'tescoWooCom'
    sku_id = []
    sku_id_new = []

    # with open('tescoGrocery.csv') as csv_file:
    with open('test.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for indx,pid in enumerate(csv_reader):
            if indx != 0:
                sku_id.append(pid[0])

    def start_requests(self):
        for i in self.sku_id:
            # if self.sku_id not in self.sku_id_new:
            yield scrapy.Request(
                url=f"https://www.tesco.com/groceries/en-GB/products/{i}",
                callback=self.parse
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

        lvl1Category = response.xpath("normalize-space(//ol/li[2]//span/text())").get()
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
