# -*- coding: utf-8 -*-
from numpy.lib.function_base import flip
import scrapy
from urllib.parse import urljoin
import json
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class ApitestSpider(scrapy.Spider):
        name = 'apiTest'

        # apiUrls = pd.read_excel('D:/sipun/rrScrapers/aimco/workingURLs.xlsx')
        apiUrls = pd.read_excel('/home/p.byom26/residentialReits/rrScrapers/aimco/workingURLs.xlsx')

        def checkNone(self, value):
            if value:
                return value
            else:
                return None
        
        def start_requests(self):
            for _,val in self.apiUrls.iterrows():
                yield scrapy.Request(
                    url=val['apiUrl'],
                    # url="https://www.vantagepointeapts.com/en/apartments/floor-plans/_jcr_content.floorplans.json",
                    method="GET",
                    callback=self.parse,
                    meta={
                        'communityName': val['communityName'],
                        'address': val['address']
                    }
                )

        def parse(self, response):
            try:
                json_resps = json.loads(response.body)
                for json_resp in json_resps:
                    #   EXTRACTION OF FLOOR INTERIOR IMAGE URL  #
                    intImgUrlLi = []
                    try:
                        intImgs = eval(json_resp.get('interiorPhotos'))
                    except:
                        intImgs = None
                    if intImgs:
                        for intImg in intImgs:
                            intImgUrlLi.append(urljoin(response.url, intImg.get("path").strip()))
                        intImgUrl = ",".join(intImgUrlLi)
                    else:
                        intImgUrl = None            
                    #   EXTRACTION OF FLOOR INTERIOR IMAGE URL ENDS  #

                    #   EXTRACTION OF FLOOR PLAN IMAGE URL  #
                    fpiu = None
                    try:
                        fpiuJson = eval(json_resp.get('diagrams'))
                    except:
                        fpiuJson = json_resp.get('diagrams')
                    if isinstance(fpiuJson, str):
                        try:
                            fpiu = urljoin(response.url, fpiuJson.strip())
                        except:
                            fpiu = None
                    elif isinstance(fpiuJson, list):
                        try:
                            fpiu = urljoin(response.url, fpiuJson[0].get("path").strip())
                        except:
                            fpiu = None
                    #   EXTRACTION OF FLOOR PLAN IMAGE URL ENDS  #

                    yield{
                        'Community Name': response.request.meta['communityName'],
                        'Address': response.request.meta['address'],
                        'Property ID': json_resp.get('propertyId'),
                        'Unit Type': json_resp.get('floorPlanName'),
                        'Unit No': json_resp.get('unitName'),
                        'Floor': json_resp.get('floor'),
                        'Price': f'''{json_resp.get('minRent')} - {json_resp.get('maxRent')}''',
                        'Deposit Amount': json_resp.get('depositAmount'),
                        'Move In Date': json_resp.get('moveInDate'),
                        'Availability': json_resp.get('available'),
                        'Bed': json_resp.get('bedrooms'),
                        'Bath': json_resp.get('bathrooms'),
                        'Amenities': ",".join(json_resp.get('amenities')),
                        'Area in sq ft': json_resp.get('sqft'),
                        'Floor Plan Img Url': fpiu,
                        'Interior Img Url': intImgUrl,
                        'Apartment Url': urljoin(response.url, json_resp.get('path').strip()),
                        # 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    }
            except:
                self.sendMail('SCRAPER ERROR ALERT: aimco communities', f'Hi,\naimco scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/aimco/aimco/spiders/apiTest.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except :
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: aimco communities'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\naimco scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/aimco/aimco/spiders/apiTest.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)