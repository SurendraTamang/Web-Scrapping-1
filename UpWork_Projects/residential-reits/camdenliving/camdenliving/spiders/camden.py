# -*- coding: utf-8 -*-
import scrapy
from datetime import date, datetime
import os
import sys
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class CamdenSpider(scrapy.Spider):
        name = 'camden'

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
                return dlmtr.join(i.strip() for i in li)
            except:
                return None
        
        def start_requests(self):
            yield scrapy.Request(
                url="https://www.camdenliving.com",
                # url="https://www.camdenliving.com/apartments/phoenix-az/bedrooms-all/pets-all",
                callback=self.getCities
                # callback=self.communityLists
            )

        def getCities(self, response):
            try:
                cities = response.xpath("//ul[@class='no-bullet-point']/li/a")
                for city in cities:
                    yield scrapy.Request(
                        url=f"https://www.camdenliving.com{city.xpath('.//@href').get()}",
                        callback=self.communityLists
                    )
            except:
                self.sendMail('SCRAPER ERROR ALERT: camden living', f'Hi,\ncamden scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getCities function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/camdenliving/camdenliving/spiders/camden.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def communityLists(self, response):
            try:
                communities = response.xpath("//div[@class='view-content']/div")
                for community in communities:
                    yield scrapy.Request(
                        url=f'''https://www.camdenliving.com{community.xpath(".//a[@class='node-title']/@href").get()}''',
                        callback=self.getCommunityDetails
                    )
            except:
                self.sendMail('SCRAPER ERROR ALERT: camden living', f'Hi,\ncamden scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "communityLists function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/camdenliving/camdenliving/spiders/camden.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
        
        def getCommunityDetails(self, response):
            try:        
                ofcHrsLi = response.xpath("//ul[@class='field--office-hours']/li/text()").getall()
                street = response.xpath("normalize-space(//div[@class='thoroughfare']/text())").get()
                city = response.xpath("normalize-space(//span[@class='locality']/text())").get()
                state = response.xpath("normalize-space(//span[@class='state']/text())").get()
                postalCode = response.xpath("normalize-space(//span[@class='postal-code']/text())").get()
                communityAminitiesImages = response.xpath("//ul[@class='slides']/li/img/@data-original").getall()
                petPolicy = response.xpath("//div[@class='field--pet-policy']/p/text()").getall()
                parkingPolicy = response.xpath("//div[@class='field--parking-policy']/p/text()").getall()
                
                cmntyAmntyList = []
                cmntyAmntis = response.xpath("//div[@class='view-content']/div[@class='item-list']")
                for cmntyAmnty in cmntyAmntis:
                    amntyHeading = cmntyAmnty.xpath("normalize-space(.//h3/span/text())").get()
                    amntyFeatures = cmntyAmnty.xpath(".//div[@class='views-rows']/div/text()").getall()
                    cmntyAmntyList.append(f'''{amntyHeading}={";".join(i.strip() for i in amntyFeatures)}''')

                yield scrapy.Request(
                    url=f"{response.url}/media-gallery",
                    callback=self.communityMediaGallery,
                    meta={
                        'communityName': response.xpath("normalize-space(//div[@class='title-section']/h1/a/text())").get(),
                        'ofcHrs': " | ".join(i.strip() for i in ofcHrsLi if "Appointment" not in i),
                        'address': f"{street}, {city}, {state} {postalCode}",
                        'communityAminities': "|".join(cmntyAmntyList),
                        'communityAminitiesImages': ",".join(j.split("?")[0] for j in communityAminitiesImages),
                        'petPolicy': " | ".join(pet.replace("\xa0", "").strip() for pet in petPolicy if pet.replace("\xa0", "").strip() != None or pet.replace("\xa0", "").strip() != ""),
                        'parkingPolicy': " | ".join(park.replace("\xa0", "").strip() for park in parkingPolicy if park.replace("\xa0", "").strip() != None or park.replace("\xa0", "").strip() != ""),
                        'baseUrl': response.url
                    }
                )
            except:
                self.sendMail('SCRAPER ERROR ALERT: camden living', f'Hi,\ncamden scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getCommunityDetails function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/camdenliving/camdenliving/spiders/camden.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def communityMediaGallery(self, response):
            try:
                imgLi = []
                images = response.xpath("//a/picture")
                for image in images:
                    imgLi.append(image.xpath(".//source/@srcset").get())
                yield scrapy.Request(
                    url=f"{response.request.meta['baseUrl']}/apartments",
                    callback=self.getAppartmentDetails,
                    meta={
                        'communityName': response.request.meta['communityName'],
                        'communityImgUrl': ",".join(k.split("?")[0] for k in imgLi),
                        'ofcHrs': response.request.meta['ofcHrs'],
                        'address': response.request.meta['address'],
                        'communityAminities': response.request.meta['communityAminities'],
                        'communityAminitiesImages': response.request.meta['communityAminitiesImages'],
                        'petPolicy': response.request.meta['petPolicy'],
                        'parkingPolicy': response.request.meta['parkingPolicy']
                    }
                )
            except:
                self.sendMail('SCRAPER ERROR ALERT: camden living', f'Hi,\ncamden scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "communityMediaGallery function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/camdenliving/camdenliving/spiders/camden.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def getAppartmentDetails(self, response):
            try:
                apartments = response.xpath("//div[contains(@class, 'view-available-apartments')]/div/div")
                for apartment in apartments:
                    unitType = apartment.xpath("normalize-space(.//div[contains(@class, 'title')]/text())").get()
                    floorPlan = apartment.xpath(".//a[contains(@title, 'Floor Plan')]/@href").get()
                    try:
                        floorPlan = floorPlan.split("?")[0]
                    except:
                        floorPlan = None
                    units = apartment.xpath(".//div[@class='node-card-bottom-container']/div[contains(@class, 'views-row')]")
                    for unit in units:
                        apartmentAmenities = unit.xpath(".//div[@class='colorbox-hide']//ul/li/span/text()").getall()
                        roomDimp = unit.xpath(".//ul[contains(@class, 'dimensions-imperial')]/li/text()").getall()
                        roomDmet = unit.xpath(".//ul[contains(@class, 'dimensions-metric')]/li/text()").getall()
                        yield{
                            'communityName': response.request.meta['communityName'],
                            'Unit Type': unitType,
                            'Unit Name': unit.xpath("normalize-space(.//div[@class='unit-name']/text())").get(),
                            'Price': unit.xpath("normalize-space(.//div[@class='price']/a/text())").get(),
                            'Floors': unit.xpath("normalize-space(.//strong[contains(text(), 'Floor')]/parent::span/text())").get(),
                            'Area in sq ft': unit.xpath("normalize-space(.//strong[contains(text(), 'SqFt')]/parent::span/text())").get(),
                            'Beds': unit.xpath("normalize-space(.//strong[contains(text(), 'Beds')]/parent::span/text())").get(),
                            'Baths': unit.xpath("normalize-space(.//strong[contains(text(), 'Baths')]/parent::span/text())").get(),
                            'Floor Plan Img': floorPlan,
                            'Availability': unit.xpath("normalize-space(.//span[contains(@class, 'move-in-date')]/text())").get(),
                            'Lease Length': unit.xpath("normalize-space(.//span[contains(text(), 'Lease Length')]/following-sibling::span/text())").get(),
                            'Apartment Amenities': self.checkISEmpty(apartmentAmenities, ","),
                            'Room Dimensions(imperial)': self.checkISEmpty(roomDimp, " | "),
                            'Room Dimensions(metric)': self.checkISEmpty(roomDmet, " | "),
                            'address': response.request.meta['address'],
                            'ofcHrs': response.request.meta['ofcHrs'],
                            'communityImgUrl': response.request.meta['communityImgUrl'],
                            'communityAminities': response.request.meta['communityAminities'],
                            'communityAminitiesImages': response.request.meta['communityAminitiesImages'],
                            'petPolicy': response.request.meta['petPolicy'],
                            'parkingPolicy': response.request.meta['parkingPolicy'],
                            # 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        }
            except:
                self.sendMail('SCRAPER ERROR ALERT: camden living', f'Hi,\ncamden scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getAppartmentDetails function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/camdenliving/camdenliving/spiders/camden.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except :
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: camden living'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\ncamden scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/camdenliving/camdenliving/spiders/camden.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)
