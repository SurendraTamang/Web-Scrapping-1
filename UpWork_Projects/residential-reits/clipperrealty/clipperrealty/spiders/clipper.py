import scrapy
from datetime import datetime
import os
import sys
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class ClipperSpider(scrapy.Spider):
        name = 'clipper'

        communityList = ['Tribeca House - 50 Murray', 'Tribeca House - 53 Park Place', 'Flatbush Gardens', 'The Aspen', '141 Livingston', '250 Livingston Street - 233 Schermerhorn', 'The Columbia Heights']
        links = [
            'https://www.flatbushgardens.net/cs/brooklyn-ny-apartments.asp',
            'http://www.aspennewyork.com/cs/new-york-city-ny-apartments.asp',
            'https://www.tribecahouseny.com/tribeca-apartment-availability'
        ]

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
                url="https://www.clipperrealty.com/pages/properties.asp",
                callback=self.parse
            )

        def parse(self, response):
            communities = response.xpath("//div[@class='nameOverlay']/text()").getall()
            newCmtyList = []
            for cmty in communities:
                if cmty not in self.communityList:
                    newCmtyList.append(cmty)
            # Send a mail if one/more new commuity listings are found. 
            if len(newCmtyList) > 0:
                self.sendMail('SCRAPER NEW COMMUNITY LISTING FOUND ALERT: clipper', f'Hi,\nA new community listing has been found with the name - {cmty}. Code need to be updated for the new listing.\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/clipperrealty/clipperrealty/spiders/bsrSpider.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

            for link in self.links:
                if 'flatbushgardens' in link:
                    yield scrapy.Request(
                        url=link,
                        callback=self.flatbushAspen,
                        meta={
                            'cName': 'Flatbush Gardens'
                        }
                    )
                elif 'aspennewyork' in link:
                    yield scrapy.Request(
                        url=link,
                        callback=self.flatbushAspen,
                        meta={
                            'cName': 'The Aspen'
                        }
                    )
                elif 'tribecahouseny' in link:
                    yield scrapy.Request(
                        url=link,
                        callback=self.tribecahouseny
                    )
                else:
                    pass
        
        def flatbushAspen(self, response):
            try:
                cName = response.request.meta['cName']
                street = response.xpath("normalize-space(//span[@itemprop='streetAddress']/text())").get()
                locality = response.xpath("normalize-space(//span[@itemprop='addressLocality']/text())").get()
                region = response.xpath("normalize-space(//span[@itemprop='addressRegion']/text())").get()
                postalCode = response.xpath("normalize-space(//span[@itemprop='postalCode']/text())").get()
                phone = response.xpath("//a[contains(@href, 'tel')]/@href").get()
                models = response.xpath("//tbody/tr")
                for model in models:
                    bed = model.xpath("normalize-space(.//td[1]/text())").get()
                    if cName == "Flatbush Gardens":
                        if bed == "Studio":
                            area = "400"
                        elif bed == 1 or bed == "1":
                            area = "600-650"
                        elif bed == 2 or bed == "2":
                            area = "800"
                        else:
                            area = None
                        price = f'${model.xpath("normalize-space(.//td[3]/text())").get()}'
                        floorPlan = f'https://www.flatbushgardens.net/cs/{model.xpath("normalize-space(.//td[4]/a/@href)").get()}'
                        availability = None
                        oHours = 'Mon-Thur 10am-6pm | Fri & Sun 10am-5pm'
                    elif cName == "The Aspen":
                        area = None
                        price = f'${model.xpath("normalize-space(.//td[4]/text())").get()}'
                        availability = f'{model.xpath("normalize-space(.//td[3]/text())").get()}'
                        floorPlan = f'http://www.aspennewyork.com/cs/{model.xpath("normalize-space(.//td[5]/a/@href)").get()}'
                        oHours = None
                    yield{
                        'Community Name': cName,
                        'Building Name': None,
                        'Residence': None,
                        'Bed': bed,
                        'Bath': None,
                        'Area in sq ft': area,
                        'Price': price,
                        'Amenities': None,
                        'Address': f'{street.replace(",", "").strip()}, {locality.replace(",", "").strip()}, {region.strip()} {postalCode.strip()}',
                        'Phone': phone.replace("tel:", ""),
                        'Office Hours': oHours,
                        'Availability': availability,
                        'Floor Plan Url': floorPlan,
                        #'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                    }
            except:
                self.sendMail('SCRAPER ERROR ALERT: clipper realty', f'Hi,\nclipper scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "flatbushAspen function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/clipperrealty/clipperrealty/spiders/clipper.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def tribecahouseny(self, response):
            try:
                buildings = response.xpath("//tbody/tr")
                for building in buildings:
                    bName = building.xpath("normalize-space(.//td[contains(@class, 'building')]/text())").get()
                    if "53 Park" in bName:
                        cName = "Tribeca House - 53 Park Place"
                        address = '53 Park Pl, New York City, NY 10007'
                    elif "50 Murray" in bName:
                        cName = "Tribeca House - 50 Murray"
                        address = '50 Murray Street, New York City, NY 10007'
                    yield{
                        'Community Name': cName,
                        'Building Name': bName,
                        'Residence': building.xpath("normalize-space(.//td[contains(@class, 'residence')]/text())").get(),
                        'Bed': building.xpath("normalize-space(.//td[contains(@class, 'bedrooms')]/text())").get(),
                        'Bath': building.xpath("normalize-space(.//td[contains(@class, 'bathrooms')]/text())").get(),
                        'Area in sq ft': building.xpath("normalize-space(.//td[contains(@class, 'size')]/text())").get(),
                        'Price': f'''${building.xpath("normalize-space(.//td[contains(@class, 'price')]/text())").get()}''',
                        'Amenities': "Roof Deck, Basketball Court, Gym, Spa, Parking, Children's Playroom, Concierge, Lounge, Games Room",
                        'Address': address,
                        'Phone': '(212) 233-6766',
                        'Office Hours': 'Mon-Thur 10am-6pm | Fri 10am-4:30pm | Sun 11am-5pm',
                        'Availability': None,
                        'Floor Plan Url': building.xpath(".//td[contains(@class, 'viewPlan')]/a/@href").get(),
                        #'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    }
            except:
                self.sendMail('SCRAPER ERROR ALERT: clipper realty', f'Hi,\nclipper scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "tribecahouseny function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/clipperrealty/clipperrealty/spiders/clipper.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except Exception:
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: clipper realty'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\nclipper scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/clipperrealty/clipperrealty/spiders/clipper.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
