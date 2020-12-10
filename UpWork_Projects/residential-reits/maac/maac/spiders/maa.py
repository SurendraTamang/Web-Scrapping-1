import scrapy
import json
from datetime import date, datetime
import os
import sys
import smtplib
from email.message import EmailMessage
import pandas as pd


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class MaaSpider(scrapy.Spider):
        name = 'maa'

        init_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        EMAIL_USER = os.environ.get('EMAIL_USER')
        EMAIL_PASS = os.environ.get('EMAIL_PASS')

        apiLinks = pd.read_excel("/home/p.byom26/residentialReits/rrScrapers/maac/links.xlsx")
        # apiLinks = pd.read_excel("D:/rrScrapers/maac/links.xlsx")

        def sendMail(self, subject, body):
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.EMAIL_USER
            msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
            msg.set_content(body)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.EMAIL_USER, self.EMAIL_PASS)    
                smtp.send_message(msg)

        def checkISEmpty(self, li, dlmtr):
            try:
                return dlmtr.join(li)
            except:
                return None
        
        def start_requests(self):
            for _,value in self.apiLinks.iterrows():
                yield scrapy.Request(
                    url=value['url'],
                    method="POST",
                    callback=self.parse,
                    meta={
                        'checkLink': value['url']
                    }
                )

        def parse(self, response):
            try:
                json_resp = json.loads(response.body)
                communities = json_resp.get('properties')
                if not bool(communities):
                    self.sendMail('SCRAPER ERROR ALERT: maac', f'Hi,\nmaac scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed. API call returned a blank response".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/maac/maac/spiders/maa.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                #     os._exit(1)
                for community in communities:
                    amnty_li = []
                    prmy_amnty_li = []            
                    cmnty_img_url_li = []
                    cmnty_img_desc_li = []        

                    try:
                        for amnty in community.get('Amenities'):
                            amnty_li.append(amnty.get('Name'))
                    except:
                        amnty_li = None
                    try:
                        for prmy_amnty in community.get('PrimaryAmenities'):
                            prmy_amnty_li.append(prmy_amnty.get('Name'))
                    except:
                        prmy_amnty_li = None
                    try:
                        for cmnty_img_url in community.get('Carousel'):
                            cmnty_img_url_li.append(f"https://www.maac.com{cmnty_img_url.get('Image').get('Src')}")
                            cmnty_img_desc_li.append(cmnty_img_url.get('Image').get('Alt'))
                    except:
                        cmnty_img_url_li = None
                        cmnty_img_desc_li = None         

                    propertyID = community.get('PropertyID')
                    if 'x' not in str(propertyID):
                        yield scrapy.Request(
                            url=f'https://www.maac.com/api/apartments/searchbylayout?propertyId={propertyID}&descendingPrice=false',
                            callback=self.getApartmentDetails,
                            method="POST",
                            meta={
                                'communityName': community.get('PropertyName'),
                                'address': community.get('Address'),
                                'lat': community.get('Lat'),
                                'long': community.get('Lng'),
                                'phone': community.get('Phone'),
                                'amenities': self.checkISEmpty(amnty_li, ","),
                                'primaryAmenities': self.checkISEmpty(prmy_amnty_li, ","),
                                'communityUrl': f"https://www.maac.com{community.get('Url')}",
                                'communityImg': self.checkISEmpty(cmnty_img_url_li, "|"),
                                'communityImgDesc': self.checkISEmpty(cmnty_img_desc_li, "|")
                            }
                        )
            except:
                self.sendMail('SCRAPER ERROR ALERT: maac', f'Hi,\nmaac scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed. Encounted a syntax error because of a null value".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/maac/maac/spiders/maa.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def getApartmentDetails(self, response):
            try:
                json_resp = json.loads(response.body)
                layouts = json_resp.get('layouts')
                if not bool(layouts):
                    self.sendMail('SCRAPER ERROR ALERT: maac', f'Hi,\nmaac scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getApartmentDetails function failed. API call returned a blank response".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/maac/maac/spiders/maa.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                    os._exit(1)
                for layout in layouts:
                    appartments = layout.get('Apartments')
                    for appartment in appartments:
                        yield{
                            'Layout Name': layout.get('Name'),
                            'Unit No.': appartment.get('UnitNumber'),
                            'Bed': appartment.get('Beds'),
                            'Bath': appartment.get('Baths'),
                            'Area in sq ft': appartment.get('SqFt'),
                            'Price': f'''{appartment.get('MinPrice')}-{appartment.get('MaxPrice')}''',
                            'Appartment Amenities': self.checkISEmpty(layout.get('Amenities'), ","),
                            'Availability': appartment.get('FormattedMoveIn'),
                            'Floor Plan Image Url': self.checkISEmpty(appartment.get('UnitImageUrls'), ","),
                            'Map Image Url': f"https://www.maac.com{appartment.get('MapUrl')}",
                            'Special Offer': appartment.get('Specials'),
                            'Apply Url': appartment.get('ApplyUrl'),
                            'Community Name': response.request.meta['communityName'],
                            'Address': response.request.meta['address'],
                            'Latitude': response.request.meta['lat'],
                            'Longitude': response.request.meta['long'],
                            'Phone': response.request.meta['phone'],
                            'Community Amenities': response.request.meta['amenities'],
                            'Community Primary Amenities': response.request.meta['primaryAmenities'],
                            'Community Url': response.request.meta['communityUrl'],
                            'Community Images': response.request.meta['communityImg'],
                            'Community Images Description': response.request.meta['communityImgDesc'],
                            # 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        }
            except:
                self.sendMail('SCRAPER ERROR ALERT: maac', f'Hi,\nmaac scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getApartmentDetails function failed. Encounted a syntax error because of a null value".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/maac/maac/spiders/maa.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except Exception:
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: maac'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\nmaac scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/maac/maac/spiders/maa.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
