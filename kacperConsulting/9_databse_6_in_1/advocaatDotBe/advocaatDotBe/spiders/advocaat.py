import scrapy
from itertools import combinations_with_replacement
from string import ascii_lowercase


class AdvocaatSpider(scrapy.Spider):
    name = 'advocaat'

    alphaLi = list(combinations_with_replacement([i for i in ascii_lowercase],3))
    
    def start_requests(self):
        for alpha in self.alphaLi:
            yield scrapy.Request(
                url=f'''https://advocaat.be/zoek-een-advocaat/zoekresultaten?advancedsearch=1&n={"".join(i for i in alpha)}''',
                callback=self.getCardUrls,
                meta={
                    'keyword': "".join(i for i in alpha),
                }
            )

    def getCardUrls(self, response):
        cards = response.xpath("//div[contains(@class, 'search-result') and contains(@class, 'card')]")
        for card in cards:
            yield scrapy.Request(
                url=f'''https://advocaat.be{card.xpath(".//h2/a/@href").get()}''',
                callback=self.parse,
                meta={
                    'keyword': response.request.meta['keyword']
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
            'Source Url': response.url,
            'keyword': response.request.meta['keyword']
        }
