# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import date, datetime
import os
import sys
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class EssexcmtySpider(scrapy.Spider):
        name = 'essexCmty'

        def start_requests(self):
            yield scrapy.Request(
                url='https://www.essexapartmenthomes.com/apartments',
                callback=self.getAPIurl
            )
        def getAPIurl(self, response):
            try:
                urls = response.xpath("//div[@class='region-links-container']/a/@href").getall()
                for url in urls:
                    fmtURL = url.split("?")[-1].replace(" ", "%20")
                    yield scrapy.Request(
                        url=f'https://www.essexapartmenthomes.com/EPT_Feature/Search/GetSearchResults?{fmtURL}',
                        method='GET',
                        callback=self.getCommunityLists
                    )
            except:
                self.sendMail('SCRAPER ERROR ALERT: essexCommunityAPI', f'Hi,\nessexCommunityAPI scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getAPIurl function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes/essexAPI/essexAPI/spiders/essexCmty.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
        
        def getCommunityLists(self, response):
            try:
                json_resp = json.loads(response.body)
                communities = json_resp.get('communities')
                for community in communities:
                    yield scrapy.Request(
                        url=f"https://www.essexapartmenthomes.com/apartments/{community.get('itemname')}/amenities",
                        callback=self.parse,
                        meta = {
                            'communityName': community.get('name'),
                            'address': community.get('address'),
                            'city': community.get('city'),
                            'state': community.get('state'),
                            'zipcode': community.get('zipcode'),
                            'coordinate': community.get('coordinate'),
                            'phone': community.get('phonenumber'),
                            'communityImages': community.get('imagelist'),
                            'floorPlansUrl': f"https://www.essexapartmenthomes.com/apartments/{community.get('itemname')}/floor-plans-and-pricing",
                        }
                    )
            except:
                self.sendMail('SCRAPER ERROR ALERT: essexCommunityAPI', f'Hi,\nessexCommunityAPI scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getCommunityLists function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes/essexAPI/essexAPI/spiders/essexCmty.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        # def getCommunityDetails(self, response):
        #     ofcHrs = []
        #     days = response.xpath("//div[contains(@class, 'office-hours')]/table/tr")
        #     for day in days:
        #         ofcHrs.append(" ".join(day.xpath(".//td/text()").getall()))

        #     yield scrapy.Request(
        #         url=f"{response.url}/amenities",
        #         callback=self.parse,
        #         meta={
        #             'communityName': response.request.meta['communityName'],
        #             'address': response.request.meta['address'],
        #             'city': response.request.meta['city'],
        #             'state': response.request.meta['state'],
        #             'zipcode': response.request.meta['zipcode'],
        #             'coordinate': response.request.meta['coordinate'],
        #             'phone': response.request.meta['phone'],
        #             'communityImages': response.request.meta['communityImages'],
        #             'floorPlansUrl': response.request.meta['floorPlansUrl'],
        #             'ofcHrs': " | ".join(x.strip() for x in ofcHrs)
        #         }
        #     )

        def parse(self, response):
            try:
                cmntyAmnty = response.xpath("//h2[contains(text(), 'Community Amenities')]/parent::div/following-sibling::div/ul[contains(@class, 'amenities-list')]/li/text()").getall()
                apmtAmnty = response.xpath("//h2[contains(text(), 'Apartment Features')]/parent::div/following-sibling::div/ul[contains(@class, 'amenities-list')]/li/text()").getall()
                yield{
                    'Community Name': response.request.meta['communityName'],
                    'Address': response.request.meta['address'],
                    'City': response.request.meta['city'],
                    'State': response.request.meta['state'],
                    'Zip Code': response.request.meta['zipcode'],
                    'Coordinate': response.request.meta['coordinate'],
                    'Phone': response.request.meta['phone'],
                    'Community Images': response.request.meta['communityImages'],
                    # 'Office Hours': response.request.meta['ofcHrs'],
                    'Community Amenities': "|".join(y.strip() for y in cmntyAmnty),
                    'Apartment Amenities': "|".join(z.strip() for z in apmtAmnty),
                    'Floor Plans Url': response.request.meta['floorPlansUrl'],
                }
            except:
                self.sendMail('SCRAPER ERROR ALERT: essexCommunityAPI', f'Hi,\nessexCommunityAPI scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes/essexAPI/essexAPI/spiders/essexCmty.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except :
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: essexApartmentHomes'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\nessexApartmentHomes scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes/essexAPI/essexAPI/spiders/essexCmty.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
