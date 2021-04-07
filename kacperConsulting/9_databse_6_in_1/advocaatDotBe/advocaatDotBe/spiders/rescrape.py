import scrapy
import pandas as pd


class RescrapeSpider(scrapy.Spider):
    name = 'rescrape'

    df = pd.read_csv("./dataRaw.csv")
    
    def start_requests(self):
        for _,val in self.df.iterrows():
            yield scrapy.Request(
                url=val['Source Url'],
                callback=self.parse,
                meta={
                    'keyword': val['keyword']
                }
            )

    def parse(self, response):
        derdenrekening = response.xpath("normalize-space(//h3[text()='Derdenrekening']/following-sibling::p/text())").get()
        if derdenrekening.startswith("De publicatie van"):
            derdenrekening = None
        yield {
            'Name': f'''{response.xpath("normalize-space(//h2/strong/text())").get()} {response.xpath("normalize-space(//h2/text()[last()])").get()}''',
            'Ingeschreven': response.xpath("normalize-space(//span[contains(text(), 'Ingeschreven')]/a/text())").get(),
            'Rechtsdomeinen': ",".join(i.strip() for i in response.xpath("//h3[text()='Rechtsdomeinen']/following-sibling::ul/li/text()").getall() if i.strip()),
            'Talen': ",".join(i.strip() for i in response.xpath("//h3[text()='Talen']/following-sibling::ul/li/text()").getall() if i.strip()),
            'Derdenrekening': derdenrekening,
            'Contact': ", ".join(i.strip() for i in response.xpath("//h3[text()='Contact']/following-sibling::div/text()").getall() if (i.strip()) and not (i.lower().startswith("tel") or i.lower().startswith("fax"))),
            'Telephone': response.xpath("normalize-space(//div[contains(text(), 'Tel')]/text())").get().replace("Tel.","").strip(),
            'Email': response.xpath("normalize-space(//h3[text()='Contact']/parent::div/div/a[contains(@href, 'mail')]/text())").get(),
            'Certification': " , ".join(i.strip() for i in response.xpath("//h3[text()='Certificaten']/following-sibling::ul/li/text()").getall() if i.strip()),
            'Source Url': response.url,
            'keyword': response.request.meta['keyword']
        }
