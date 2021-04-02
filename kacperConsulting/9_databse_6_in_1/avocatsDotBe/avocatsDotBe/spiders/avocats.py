import scrapy
from urllib.parse import unquote


class AvocatsSpider(scrapy.Spider):
    name = 'avocats'
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://avocats.be/fr/lawyer-search?field_nom_value=&field_pr_nom_value=&field_code_postal_value=&field_ville_value=&field_liste_barreau_value=All&field_liste_des_mati_res_value=All&field_liste_aide_juridique_value=All",
            callback=self.getListings
        )

    def getListings(self, response):
        tableRows = response.xpath("//table/tbody/tr")
        for tableRow in tableRows:
            yield scrapy.Request(
                url=f'''https://avocats.be{tableRow.xpath(".//td/a/@href").get()}''',
                callback=self.parse
            )
        nextPage = response.xpath("//a[contains(text(), 'Suivant')]/@href").get()
        if nextPage:
            yield scrapy.Request(
                url=f'''https://avocats.be/fr/{nextPage}''',
                callback=self.getListings
            )

    def parse(self, response):
        emailImg = response.xpath("//div[contains(text(), 'mail')]/following-sibling::div/div/img/@src").get()
        email = None
        if emailImg:
            emailImg = emailImg.split("/")[-1].replace(".png","")
            email = unquote(emailImg)

        yield {
            'Name': response.xpath("normalize-space(//div[contains(@class, 'field-name-field-pr-nom')]/text())").get(),
            'Postal Address': response.xpath("normalize-space(//div[contains(@class, 'field-name-field-code-postal')]/text())").get(),
            'Barreau': response.xpath("normalize-space(//div[contains(@class, 'field-name-field-barreau')]/div/div/text())").get(),
            'Matières préférentielles': ",".join(i.strip() for i in response.xpath("//strong[contains(text(), 'préférentielles')]/parent::div/text()").getall() if i.strip()),
            'Aide juridique': ",".join(i.strip() for i in response.xpath("//strong[contains(text(), 'juridique')]/parent::div/text()").getall() if i.strip()),
            'Email': email,
            'Source Url': response.url
        }
