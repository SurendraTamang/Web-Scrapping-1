# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage


init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
try:
    class AvalonSpider(scrapy.Spider):
        name = 'avalon'

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
                # url="https://www.avaloncommunities.com/colorado",
                # callback=self.getCommunityList
                url="https://www.avaloncommunities.com/apartment-locations",
                callback=self.getStateUrls
            )

        def getStateUrls(self, response):
            try:
                states = response.xpath("//div[@class='row']/div/h3")
                for state in states:
                    yield scrapy.Request(
                        url=f'https:{state.xpath(".//a/@href").get()}',
                        callback=self.getCommunityList
                    )
            except:
                self.sendMail('SCRAPER ERROR ALERT: avalon communities', f'Hi,\navalon scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getStateUrls function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/avalonCommunities/avalonCommunities/spiders/avalon.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def getCommunityList(self, response):
            try:
                communities = response.xpath("//ul[contains(@class, 'communities-list')]/li")
                for community in communities:
                    yield scrapy.Request(
                        url=f'''https://www.avaloncommunities.com{community.xpath(".//h2/a/@href").get()}''',
                        callback=self.getCommunityDetails,
                        meta={
                            'communityName': community.xpath("normalize-space(.//h2/a/text())").get(),
                            'address': community.xpath("normalize-space(.//div[@class='address']/text())").get()
                        }
                    )
            except:
                self.sendMail('SCRAPER ERROR ALERT: avalon communities', f'Hi,\navalon scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getCommunityList function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/avalonCommunities/avalonCommunities/spiders/avalon.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def getCommunityDetails(self, response):
            try:
                communityImgs = response.xpath("//div[@class='item-wrapper']/img/@data-src").getall()
                communityImgs.append(response.xpath("//div[@class='item-wrapper']/img/@src").get())
                officeHours = response.xpath("(//p[@id='hours-more-data'])[1]/span/span/text()").getall()
                phone = response.xpath("//p[@class='address-phone']/span[last()]/text()").get()
                apartmentAmenities = response.xpath("(//h6[contains(text(), 'Apartment')]/following-sibling::div/ul)[1]/li/span/text()").getall()
                communityAmenities = response.xpath("(//h6[contains(text(), 'Community')]/following-sibling::div/ul)[1]/li/span/text()").getall()

                try:
                    ciu = ",".join(cImg.split("?")[0] for cImg in communityImgs)
                except:
                    ciu = None

                # apartmentTypes = response.xpath("//ul[@class='apartments-list']/li")
                # for apartmentType in apartmentTypes:
                #     if (apartmentType.xpath(".//@class").get()) != "specials":
                yield scrapy.Request(
                    # url=f'''https://www.avaloncommunities.com{apartmentType.xpath(".//a/@href").get()}''',
                    url = f"{response.url}/apartments",
                    callback=self.parse,
                    meta={
                        'communityName': response.request.meta['communityName'],
                        'address': response.request.meta['address'],
                        'communityImagesUrl': ciu,
                        'officeHours': " | ".join(officeHour.strip() for officeHour in officeHours),
                        'phone': phone,
                        'apartmentAmenities': "|".join(i.strip() for i in apartmentAmenities if i!= None or i!= "" or i!= " "),
                        'communityAmenities': "|".join(j.strip() for j in communityAmenities if j!= None or j!= "" or j!= " "),
                        'communityUrl': response.url
                    }
                )
            except:
                self.sendMail('SCRAPER ERROR ALERT: avalon communities', f'Hi,\navalon scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getCommunityDetails function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/avalonCommunities/avalonCommunities/spiders/avalon.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)

        def parse(self, response):
            try:        
                apartments = response.xpath("//ul[contains(@class, 'apartment-cards')]/li")
                for apartment in apartments:
                    apartmentNo = apartment.xpath("normalize-space(.//div[contains(@class, 'title')]/text())").get()
                        
                    if apartmentNo != "Unavailable":
                        houseDetails =  apartment.xpath("normalize-space(.//div[contains(@class, 'details')]/text())").get()  
                        floorPlan = apartment.xpath(".//ul/li/img/@data-src").get()
                        availability = apartment.xpath("normalize-space(.//div[@class='availability']/text())").get()
                        
                        try:
                            bed = houseDetails.split("•")[-3].strip().split(" ")[0]
                            if bed == "Furnished":
                                bed = None
                        except:
                            bed = None
                        try:
                            lease = int(''.join(filter(str.isdigit, apartment.xpath(".//div[@class='price']/text()[last()]").get())))
                        except:
                            lease = None            
                        if availability != None:
                            availabilityNew = availability.replace("Available ", "")
                        else:
                            availabilityNew = None
                        yield{
                            'Apartment No': apartmentNo.replace("Apartment ", ""),
                            'Floor Plan': floorPlan.split("?")[0],
                            'Lease in months': lease,
                            'Availability': availabilityNew,
                            'Price': apartment.xpath("normalize-space(.//div[@class='price']/span/text())").get(),
                            'Bed': bed,
                            'Bath': houseDetails.split("•")[-2].strip().split(" ")[0],
                            'Area in sq ft': houseDetails.split("•")[-1].strip().replace(" sqft", ""),
                            'Apartment Amenities': response.request.meta['apartmentAmenities'],
                            'Community Name': response.request.meta['communityName'],
                            'Address': response.request.meta['address'],
                            'Community Img Url': response.request.meta['communityImagesUrl'],
                            'Office Hours': response.request.meta['officeHours'],
                            'Phone': response.request.meta['phone'],
                            'Community Amenities': response.request.meta['communityAmenities'],
                            'Community Url': response.request.meta['communityUrl'],
                            'Apartment Url': f'''{response.url.split("/apartments")[0]}/{apartment.xpath(".//a/@href").get()}''',
                            # 'Timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            # 'Current Page': response.url
                        }
            except:
                self.sendMail('SCRAPER ERROR ALERT: avalon communities', f'Hi,\navalon scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "parse function failed".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/avalonCommunities/avalonCommunities/spiders/avalon.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
except :
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: avalon communities'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\navalon scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/avalonCommunities/avalonCommunities/spiders/avalon.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)    
        smtp.send_message(msg)