import scrapy
import os
import sys
import smtplib
from email.message import EmailMessage
from datetime import datetime


try:
    init_time_outer = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    class MmcscraperSpider(scrapy.Spider):
        name = 'mmcScraper'

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
                url="https://mymhcommunity.com/FindACommunity/SearchResults",
                callback=self.getCommunityDetails
            )

        def getCommunityDetails(self, response):
            items = response.xpath("//div[@class='community-search-results']/div[@class='item']")
            if items == '' or items == None:
                self.sendMail('ALERT! --- MyMHCommunity SPIDER FAILED ---', f'Hi,\nmymhcommunity scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getCommunityDetails function failed. It is returning a blank response".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/myMHcommunity/myMHcommunity/spiders/mmcScraper.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
            for item in items:
                phone = item.xpath(".//a[contains(@href, 'tel')]/@href").get()
                yield scrapy.Request(
                    url=f'https://mymhcommunity.com{item.xpath(".//h5/a/@href").get()}',
                    callback=self.getHouses,
                    meta={
                        'communityName': item.xpath("normalize-space(.//h5/a/text())").get(),
                        'communityAddress': item.xpath("normalize-space(.//p/text())").get(),
                        'phone': phone.replace("tel:", "")
                    }
                )        
            nextPage = response.xpath("//a[@title='Next']/@href").get()
            if nextPage:
                yield scrapy.Request(
                    url=f'https://mymhcommunity.com{nextPage}',
                    callback=self.getCommunityDetails
                )

        def getHouses(self, response):
            li = []
            items = response.xpath("//div[@class='home-list-item']")
            if items == '' or items == None:
                self.sendMail('ALERT! --- MyMHCommunity SPIDER FAILED ---', f'Hi,\nmymhcommunity scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {self.init_time}\nThe error is "getHouses function failed. It is returning a blank response".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/myMHcommunity/myMHcommunity/spiders/mmcScraper.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
            amenities = response.xpath("//ul[contains(@class, 'amenities-list')]/li")
            for amenity in amenities:
                am = amenity.xpath("normalize-space(.//div/text()[last()])").get()
                li.append(am)
            comAmenities = ",".join(li)
            for item in items:
                yield scrapy.Request(
                    url=f'''https://mymhcommunity.com{item.xpath(".//a[contains(text(), 'View Details')]/@href").get()}''',
                    callback=self.parse,
                    meta={
                        'communityName': response.request.meta['communityName'],
                        'communityAddress': response.request.meta['communityAddress'],
                        'phone': response.request.meta['phone'],
                        'homeAddress': item.xpath("normalize-space(.//h6/following-sibling::p/text())").get(),
                        'communityAmenities': comAmenities
                    }
                )

        def parse(self, response):
            bed = response.xpath("normalize-space(//strong[contains(text(), 'Bedrooms')]/parent::li/text()[last()])").get()
            bath = response.xpath("normalize-space(//strong[contains(text(), 'Bathrooms')]/parent::li/text()[last()])").get()
            if bed == '' or bath == '':
                self.sendMail('SCRAPER ERROR ALERT: mymhcommunity', f'Hi,\nmymhcommunity scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/myMHcommunity/myMHcommunity/spiders/mmcScraper.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')
                os._exit(1)
            yield{
                'Serial No': response.xpath("normalize-space(//strong[contains(text(), 'Serial')]/parent::li/text()[last()])").get(),
                'Site No': response.xpath("normalize-space(//strong[contains(text(), 'Site')]/parent::li/text()[last()])").get(),
                'Home Address': response.request.meta['homeAddress'],
                'Listing Type': response.xpath("normalize-space(//strong[contains(text(), 'Listing Type')]/parent::li/text()[last()])").get(),
                'Renting Price': response.xpath("normalize-space(//strong[contains(text(), 'For Rent Price')]/parent::li/text()[last()])").get(),
                'Selling Price': response.xpath("normalize-space(//strong[contains(text(), 'For Sale Price')]/parent::li/text()[last()])").get(),
                'Area in SqFeet': response.xpath("normalize-space(//strong[contains(text(), 'Square Feet')]/parent::li/text()[last()])").get(),
                'Bedroom': bed,
                'Bathroom': bath,
                'Model': response.xpath("normalize-space(//strong[contains(text(), 'Model')]/parent::li/text()[last()])").get(),
                'Make': response.xpath("normalize-space(//strong[contains(text(), 'Make')]/parent::li/text()[last()])").get(),
                'Year': response.xpath("normalize-space(//strong[contains(text(), 'Year')]/parent::li/text()[last()])").get(),
                'Home Amenities': response.xpath("normalize-space(//strong[contains(text(), 'Home Amenities:')]/following-sibling::span/text())").get(),
                'Url': response.url,
                'Phone': response.request.meta['phone'],
                'Commuity Name': response.request.meta['communityName'],
                'Commuity Address': response.request.meta['communityAddress'],
                'Community Amenities': response.request.meta['communityAmenities']
            }
except:
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'SCRAPER ERROR ALERT: mymhcommunity'
    msg['From'] = EMAIL_USER
    msg['To'] = 'p.byom26@gmail.com, henrytz369@gmail.com'
    msg.set_content(f'Hi,\nmymhcommunity scraper encountered an error at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\nThe scraping job was initiated at {init_time_outer}\nThe error is "An Unexcepted Error Occured".\nPlease see more information here: /home/p.byom26/residentialReits/rrScrapers/myMHcommunity/myMHcommunity/spiders/mmcScraper.py\nContact p.byom26@gmail.com for help.\n\nSent From\nGCP Ubuntu VM')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)   
        smtp.send_message(msg)
