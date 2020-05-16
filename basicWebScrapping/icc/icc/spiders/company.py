# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class CompanySpider(scrapy.Spider):
    name = 'company'
    #allowed_domains = ['www.icchk.org.hk/business_directory.php?page=1']
    #start_urls = ['http://www.icchk.org.hk/business_directory.php?page=1']

    http_user = 'user'
    http_pass = 'userpass'

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
        end
    '''
    def rm_unwanted_char(self, value):
        try:
            return value.strip(" \xa0")
        except:
            return value

    def start_requests(self):
        yield scrapy.Request(
            url='http://www.icchk.org.hk/business_directory.php?page=1',
            callback=self.listings
        )

    def listings(self, response):
        items = response.xpath("//td[@valign='top']")
        for item in items:
            rel_url = item.xpath(".//a/@href").get()
            abs_url = f'http://www.icchk.org.hk/{rel_url}'
            yield SplashRequest(
                url=abs_url,
                endpoint='execute',
                callback=self.parse,
                args={
                    'lua_source': self.script
                }
            )
        
        next_page = response.xpath("(//div[@style='text-align:center']/a)[last()]/@href").get()
        if next_page:
            yield scrapy.Request(
                url=f'http://www.icchk.org.hk/{next_page}',
                callback=self.listings
            )

    def parse(self, response):

        yield {
            'Company_Name': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Company Name']/parent::td/following-sibling::td/text())").get()),
            'Address': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Address']/parent::td/following-sibling::td/text())").get()),
            'Contact_Name': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Contact']/parent::td/following-sibling::td/text())").get()),
            'Phone': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Phone']/parent::td/following-sibling::td/text())").get()),
            'Fax': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Fax']/parent::td/following-sibling::td/text())").get()),
            'Email': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Email']/parent::td/following-sibling::td/text())").get()),
            'Member_Type': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Member Type']/parent::td/following-sibling::td/text())").get()),
            'Telex': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Telex']/parent::td/following-sibling::td/text())").get()),
            'Website': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='WebSite']/parent::td/following-sibling::td/text())").get()),
            'Subsidary': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Subsidary']/parent::td/following-sibling::td/text())").get()),
            'Management': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Management']/parent::td/following-sibling::td/text())").get()),
            'Business_Nature': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Business Nature']/parent::td/following-sibling::td/text()[2])").get()),
            'Import_Product': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Import Product']/parent::td/following-sibling::td/text())").get()),
            'Export_Product': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Export Product']/parent::td/following-sibling::td/text())").get()),
            'Sub_Product': self.rm_unwanted_char(response.xpath("normalize-space(//b[text()='Sub Product']/parent::td/following-sibling::td/text())").get()),
            'URL': response.url
        }
