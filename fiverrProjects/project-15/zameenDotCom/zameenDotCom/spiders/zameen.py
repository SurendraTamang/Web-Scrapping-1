import scrapy
import json


class ZameenSpider(scrapy.Spider):
    name = 'zameen'
    
    urls = [
        'https://www.zameen.com/Plots/Lahore_DHA_Defence-9-1.html',
        'https://www.zameen.com/Plots/Lahore_DHA_Defence-9-2.html',
    ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.getPropertyID
            )

    def getPropertyID(self, response):
        plots = response.xpath("//div/ul/li[@role='article']")
        for plot in plots:
            yield scrapy.Request(
                url=f'''https://www.zameen.com/nfpage/async/show-numbers?property_id={plot.xpath(".//a/@href").get().split("-")[1]}''',
                method="POST",
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50',
                    'x-requested-with': 'XMLHttpRequest'
                },
                callback=self.parse,
                meta={
                    'adStatus': plot.xpath("normalize-space(.//div[contains(@aria-label, 'label')]/text())").get(),
                    'status': plot.xpath("normalize-space(.//span[contains(@aria-label, ' badge')]/text())").get(),
                    'companyName': plot.xpath("normalize-space(.//div[contains(@aria-label, 'Location')]/text())").get(),
                    'plotArea': plot.xpath("normalize-space(.//span[contains(@aria-label, 'Area')]//div/span/text())").get(),
                }
            )

    def parse(self, response):
        json_resp = json.loads(response.body)
        yield {
            'Plot Area': response.request.meta['plotArea'],
            'Name': json_resp.get('result').get('number').get('contact_person'),
            'Number1': json_resp.get('result').get('number').get('mobile'),
            'Number2': json_resp.get('result').get('number').get('phone'),
            'Company Name': response.request.meta['companyName'],
            'Status': response.request.meta['status'],
            'Ad Status': response.request.meta['adStatus'],
        }
