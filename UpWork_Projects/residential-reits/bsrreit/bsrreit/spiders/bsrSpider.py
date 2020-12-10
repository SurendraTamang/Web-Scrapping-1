import scrapy
import json
from datetime import date, datetime
import os
import sys
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class BsrspiderSpider(scrapy.Spider):
        name = 'bsrSpider'

        init_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        EMAIL_USER = os.environ.get('EMAIL_USER')
        EMAIL_PASS = os.environ.get('EMAIL_PASS')

        reqHeaders = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,sk;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Cookie': '_ga=GA1.2.1849973957.1601865499; _gid=GA1.2.501218214.1601865499; ARRAffinity=1065498437e49ed27544ec9e123507371f88b62e500ea156753f5a95459fa30f',
            'Host': 'www.bsrreit.com',
            'Origin': 'https://www.bsrreit.com',
            'Referer': 'https://www.bsrreit.com/Locations',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        def sendMail(self, subject, body):
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.EMAIL_USER
            msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
            msg.set_content(body)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.EMAIL_USER, self.EMAIL_PASS)    
                smtp.send_message(msg)

        def start_requests(self):
            yield scrapy.Request(
                url='https://www.bsrreit.com/Locations/_DoQuery',
                headers=self.reqHeaders,
                method='POST',
                callback=self.parse
            )

        def parse(self, response):
            json_resp = json.loads(response.body)
            items = json_resp.get('Results')
            if not bool(items):
                self.sendMail('SCRAPER ERROR ALERT: bsrreit', f'Hi,\nbsrreit scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed. API call returned a blank response".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/bsrreit/bsrreit/spiders/bsrSpider.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
            for item in items:            
                yield scrapy.Request(
                    url=f'''{item.get('url')}/Marketing/FloorPlans''',
                    callback=self.houseDetails,
                    meta={
                        'title': item.get('title'),
                        'address': item.get('address'),
                        'address2': item.get('address2'),
                        'city': item.get('city'),
                        'state': item.get('state'),
                        'postalCode': item.get('postalCode'),
                        'tel': item.get('tel'),
                        'rating': item.get('rating'),
                        'url': item.get('url'),
                        'lat': item.get('lat'),
                        'lon': item.get('lon')
                    }
                )

        def houseDetails(self, response):
            items = response.xpath("//div[@id='floorplans']/div")
            for item in items:
                type = item.xpath("normalize-space(.//h4/text())").get()
                if type == '':
                    self.sendMail('SCRAPER ERROR ALERT: bsrreit', f'Hi,\nbsrreit scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "houseDetails function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/bsrreit/bsrreit/spiders/bsrSpider.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                    os._exit(1)
                yield{
                    'UniqueKey': f'''{response.request.meta['title']}_{response.request.meta['state']}_{response.request.meta['postalCode']}_{item.xpath("normalize-space(.//h4/text())").get()}''',
                    'Title': response.request.meta['title'],
                    'Address': response.request.meta['address'],
                    'Address2': response.request.meta['address2'],
                    'City': response.request.meta['city'],
                    'State': response.request.meta['state'],
                    'PostalCode': response.request.meta['postalCode'],
                    'Telephone': response.request.meta['tel'],
                    'Rating': response.request.meta['rating'],
                    'Url': response.request.meta['url'],
                    'Latitude': response.request.meta['lat'],
                    'Longitude': response.request.meta['lon'],
                    'Type': type,
                    'Bed': item.xpath("normalize-space(.//ul[@class='list-divider']/li[contains(text(), 'Bed')])").get(),
                    'Bath': item.xpath("normalize-space(.//ul[@class='list-divider']/li[contains(text(), 'Bath')])").get(),
                    'FloorArea': item.xpath("normalize-space(.//ul[@class='list-divider']/li[contains(text(), 'sqft')])").get(),
                    'Price': item.xpath("normalize-space(.//p[@class='pricing']/text())").get(),
                    'Availabilty': item.xpath("normalize-space(.//p[@class='availability']/text())").get()
                }
except Exception:
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: bsrreit'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\nbsrreit scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/bsrreit/bsrreit/spiders/bsrSpider.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
