# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from selenium.webdriver.common.action_chains import ActionChains
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class NetballSpider(scrapy.Spider):
    name = 'netball'

    def gen_url(self, value):
        new = value.replace("&popup=1", "&save=0")
        return f"http://my.netball.com.au{new}&popup=1"
    
    def start_requests(self):
        yield SeleniumRequest(
            url="http://my.netball.com.au",
            wait_time=5,
            callback=self.get_listings
        )

    def get_listings(self, response):
        cntr = 1
        driver = response.meta['driver']
        driver.maximize_window()
        driver.get("http://my.netball.com.au/common/pages/public/clubfinder.aspx?pcode=2000&save=0&entityid=38925")
        time.sleep(6)

        while cntr <= 3:
            html = driver.page_source
            resp_obj = Selector(text=html)
            
            listings = resp_obj.xpath("//table/tbody/tr[@class='FinderRow']/td[1]")

            for li in listings:
                listing_url = self.gen_url(li.xpath(".//a/@href").get())
                yield scrapy.Request(
                    url=listing_url,
                    callback=self.parse
                )
            cntr += 1
            driver.find_element_by_xpath(f"//a[text()={cntr}]").click()
            time.sleep(5)

    def parse(self, response):
        address = response.xpath("normalize-space(//*[@id='leftPane']/div[1]/p[1]/text()[3])").get()
        yield{
            'ClubName': response.xpath("normalize-space(//h3/text())").get(),
            'AssociationName': response.xpath("normalize-space(//div[@id='affiliates']//a/text())").get(),
            'ClubAddress': address.replace("Address: ", ""),
            'ClubEmail': response.xpath("normalize-space(//a[contains(text(), '.com')]/text())").get(),
            'ClubWebsite': response.xpath("normalize-space(//div[contains(@id, 'website')]/a/@href)").get(),
            'ClubFacebookAddress': response.xpath("normalize-space(//div[contains(@id, 'facebook')]/a/@href)").get()
        }
            