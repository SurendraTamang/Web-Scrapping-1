import scrapy


class KtspiderSpider(scrapy.Spider):
    name = 'ktSpider'

    urls = [
        'http://id-kootenai-assessor.governmax.com/propertymax/GRM/tab_parcel_v0709.asp?t_nm=base_new&l_cr=1&t_wc=|parcelid=000020000010&sid=FB3DFF2587EF4E3B9EF447504CCB53B0',
        'http://id-kootenai-assessor.governmax.com/propertymax/GRM/tab_parcel_v0709.asp?t_nm=base_new&l_cr=2&t_wc=|parcelid=000020000020&sid=FB3DFF2587EF4E3B9EF447504CCB53B0',
        'http://id-kootenai-assessor.governmax.com/propertymax/GRM/tab_parcel_v0709.asp?t_nm=base_new&l_cr=3&t_wc=|parcelid=000020000030&sid=FB3DFF2587EF4E3B9EF447504CCB53B0'
    ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
    
    def parse(self, response):
        print("test")
        print(response)
