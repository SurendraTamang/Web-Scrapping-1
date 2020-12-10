import scrapy
import pandas as pd


class UpcSpider(scrapy.Spider):
    name = 'upc'

    df = pd.read_csv("/home/p.byom26/residentialReits/rrScrapers/upcCode/inputData.csv")
    # df = pd.read_csv("D:/rrScrapers/upcCode/iherbData.csv")

    def checkNan(self, val):
        if val == "data_not_avl":
            return None
        else:
            return val
    
    def start_requests(self):
        for _,val in self.df.iterrows():
            yield scrapy.Request(
                url=val['Product url'],
                callback=self.parse,
                meta={
                    'Product Name': val['Product Name'],
                    'Product Image URL': val['Product Image URL'],
                    'Expiry Date': val['Expiry Date'],
                    'Shipping Weight': val['Shipping Weight'],
                    'Product Code': val['Product Code'],
                    'Dimensions': val['Dimensions'],
                    'Package Quantity': val['Package Quantity'],
                    'Brand Name': val['Brand Name'],
                    'Normal Quantity': val['Normal Quantity'],
                    'Normal Price': val['Normal Price'],
                    'Best Value Quantity': val['Best Value Quantity'],
                    'Best Value price': val['Best Value price'],
                    'Breadcrumbs': val['Breadcrumbs'],
                    'Warning': val['Warning'],
                    'Other Ingrediants': val['Other Ingrediants'],
                    'Description': val['Description'],
                    'Product url':val['Product url']
                }
            )

    def parse(self, response):
        yield{
            'Product Name': self.checkNan(response.request.meta['Product Name']),
            'Product Image URL': self.checkNan(response.request.meta['Product Image URL']),
            'Expiry Date': self.checkNan(response.request.meta['Expiry Date']),
            'Shipping Weight': self.checkNan(response.request.meta['Shipping Weight']),
            'Product Code': self.checkNan(response.request.meta['Product Code']),
            'upc code': f'''{response.xpath("normalize-space(//li[contains(text(), 'UPC')]/span/text())").get()}''',
            'Dimensions': self.checkNan(response.request.meta['Dimensions']),
            'Package Quantity': self.checkNan(response.request.meta['Package Quantity']),
            'Brand Name': self.checkNan(response.request.meta['Brand Name']),
            'Normal Quantity': self.checkNan(response.request.meta['Normal Quantity']),
            'Normal Price': self.checkNan(response.request.meta['Normal Price']),
            'Best Value Quantity': self.checkNan(response.request.meta['Best Value Quantity']),
            'Best Value price': self.checkNan(response.request.meta['Best Value price']),
            'Breadcrumbs': self.checkNan(response.request.meta['Breadcrumbs']),
            'Warning': self.checkNan(response.request.meta['Warning']),
            'Other Ingrediants': self.checkNan(response.request.meta['Other Ingrediants']),
            'Description': self.checkNan(response.request.meta['Description']),
            'Product url': self.checkNan(response.request.meta['Product url']),
        }
