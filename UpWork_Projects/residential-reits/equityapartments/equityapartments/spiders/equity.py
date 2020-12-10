# -*- coding: utf-8 -*-
import scrapy
from datetime import date, datetime
import os
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class EquitySpider(scrapy.Spider):
        name = 'equity'

        init_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        EMAIL_USER = os.environ.get('EMAIL_USER')
        EMAIL_PASS = os.environ.get('EMAIL_PASS')

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
                url="https://www.equityapartments.com/#markets",
                callback=self.getMarkets
            )

        def getMarkets(self, response):
            try:
                markets = response.xpath("//div[@class='row']/div[contains(@class, 'market')]")
                for market in markets:
                    yield scrapy.Request(
                        url=f'''https://www.equityapartments.com{market.xpath(".//a/@href").get()}''',
                        callback=self.getCommunityList
                    )
            except:
                self.sendMail('SCRAPER ERROR ALERT: equityApartments', f'Hi,\nequityApartments scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getMarkets function failed with some unexcepted error. May be the website layout might have been changed / Page didnt load properly".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/equityapartments/equityapartments/spiders/equity.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
        
        def getCommunityList(self, response):
            try:
                communities = response.xpath("//div[@id='property-listings']//div[@class='row property']")
                for community in communities:
                    yield scrapy.Request(
                        url=f'''https://www.equityapartments.com{community.xpath(".//h3/a/@href").get()}''',
                        callback=self.parse,
                        meta={
                            'Community Name': community.xpath("normalize-space(.//h3/a/text())").get(),
                            'Neighbourhood': community.xpath("normalize-space(.//h4/text())").get(),
                            'Latitude': community.xpath(".//div[contains(@class, 'map-hover')]/@lat").get(),
                            'Longitude': community.xpath(".//div[contains(@class, 'map-hover')]/@lon").get(),
                        }
                    )
            except:
                self.sendMail('SCRAPER ERROR ALERT: equityApartments', f'Hi,\nequityApartments scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getCommunityList function failed with some unexcepted error. May be the website layout might have been changed / Page didnt load properly".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/equityapartments/equityapartments/spiders/equity.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def parse(self, response):
            try:
                #   EXTRACT OFFICE HOURS    #        
                ofcHrs = []
                ofcDays = response.xpath("//div[@ng-show='toggleHours']/ul/li")
                for ofcDay in ofcDays:
                    try:
                        ofcHrs.append(f'''{ofcDay.xpath(".//span[1]/text()").get().strip()} {ofcDay.xpath(".//span[2]/text()").get().strip()}-{ofcDay.xpath(".//span[3]/text()").get().strip()}''')
                    except:
                        try:
                            ofcHrs.append(f'''{ofcDay.xpath(".//span[1]/text()").get().strip()} {ofcDay.xpath(".//span[2]/text()").get().strip()}''')
                        except:
                            pass

                #   EXTRACT AMENITY DETAILS    # 
                cmntyAmnty = response.xpath("//h4[contains(text(), 'Community Amenities')]/parent::div/following-sibling::div/div/div/text()").getall()
                cmntyHLftrs = response.xpath("//div[contains(@class, 'highlights')]/div/h3/text()").getall()
                aptAmnty = response.xpath("//h4[contains(text(), 'Apartment Amenities')]/parent::div/following-sibling::div/div/div/text()").getall()

                floorPlans = response.xpath("//div[@id='unit-availability-tile']/div[@class='data-view']/div")
                for floorPlan in floorPlans:
                    apartments = floorPlan.xpath(".//ul[@class='list-group']/li")
                    for apartment in apartments:
                        if apartment.xpath(".//div[contains(@class, 'floorplan')]/img/@src").get():
                            try:
                                spOfr = apartment.xpath(".//div[contains(text(), 'Special Offer')]/i/@popover").get().strip()
                            except:
                                spOfr = None
                            flno = apartment.xpath("normalize-space(.//span[contains(text(), 'sq')]/parent::p/span[contains(text(), 'Floor')]/text())").get()
                            if 'Floor' in flno:
                                flno.replace('Floor','').strip()
                            else:
                                flno = None
                            bed = floorPlan.xpath("normalize-space(.//h4[@class='panel-title']/a/text())").get().replace("Bed", "").strip()
                            if "3+" in bed:
                                bed = apartment.xpath("normalize-space(.//div[contains(@class, 'specs')]/p[contains(text(), 'Bed')]/text())").get().replace("Bed", "").strip()
                            yield{
                                'Community Name': response.request.meta['Community Name'],
                                'Neighbourhood': response.request.meta['Neighbourhood'],
                                'Latitude': response.request.meta['Latitude'],
                                'Longitude': response.request.meta['Longitude'],
                                'Address': response.xpath("normalize-space(//a[contains(@class, 'hero-address visible')]/text())").get(),
                                'Office Hours': " | ".join(ofcHrs),
                                'Phone': response.xpath("//a[@itemprop='telephone']/span[last()]/text()").get(),
                                'Community Amenities': " | ".join(cmntyAmnty),
                                'Apartment Amenities': " | ".join(aptAmnty),
                                'Community Highlighted Features': " | ".join(cmntyHLftrs),
                                'Area in sq ft': apartment.xpath("normalize-space(.//span[contains(text(), 'sq')]/text())").get().replace("sq.ft.","").strip(),
                                'Price': apartment.xpath("normalize-space(.//span[contains(@class, 'pricing')]/text())").get(),
                                'Floor No': flno,
                                'Lease Period in Months': apartment.xpath("normalize-space(.//span[contains(@class, 'time-period')]/text())").get().replace("mo", "").strip(),
                                'Bath': apartment.xpath("normalize-space(.//div[contains(@class, 'specs')]/p[contains(text(), 'Bed')]/text()[last()])").get().replace("Bath", "").strip(),
                                'Bed': bed,
                                'Availability': apartment.xpath("normalize-space(.//div[contains(@class, 'specs')]/p[contains(text(), 'Available')]/text())").get().replace("Available","").strip(),
                                'Special Offer': spOfr,
                                'Floor Plan Img Url': apartment.xpath(".//div[contains(@class, 'floorplan')]/img/@src").get(),
                                # 'Apartment Description': apartment.xpath("normalize-space(.//div[contains(@class, 'specs')]/p[contains(@class, 'description')]/text())").get(),
                                # 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                # 'Source Page': response.url
                            }
            except:
                self.sendMail('SCRAPER ERROR ALERT: equityApartments', f'Hi,\nequityApartments scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed with some unexcepted error. May be the website layout might have been changed / Page didnt load properly".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/equityapartments/equityapartments/spiders/equity.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except :
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: equityApartments'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\nequityApartments scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/equityapartments/equityapartments/spiders/equity.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
