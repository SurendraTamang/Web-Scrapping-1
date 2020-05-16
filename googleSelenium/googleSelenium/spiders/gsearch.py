# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector    
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
import csv


class GsearchSpider(scrapy.Spider):
    name = 'gsearch'
    # allowed_domains = ['www.google.com']
    # start_urls = ['https://www.google.com']
    def insta_followers2(self, value):
        try:
            li = value.split(" ")
            keyword = "followers"
            if keyword in value.lower():
                return li[0]
            else:
                return None
        except:
            return None

    def insta_following2(self, value):
        try:
            li = value.split(" ")
            keyword = "following"
            if keyword in value.lower():
                return li[2]
            else:
                return None
        except:
            return None
    
    def insta_followers1(self, value):
        try:
            li = value.split(" ")
            keyword = "followers"
            if keyword in value.lower():
                return li[0]
            else:
                return None
        except:
            return None

    def insta_following1(self, value):
        try:
            li = value.split(" ")
            keyword = "following"
            if keyword in value.lower():
                return li[2]
            else:
                return None
        except:
            return None

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com",
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        #li = ['google', 'facebook', 'youtube']
        driver = response.meta['driver']
        driver.set_window_size(1920, 1080)
        with open('C:/Users/byom/Desktop/WebScrapping/players/searchPara.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                search_input = driver.find_element_by_xpath("//input[@title='Search']")
                search_input.send_keys(row[0])
                #driver.save_screenshot("search_key.png")
                search_input.send_keys(Keys.ENTER)
                #driver.save_screenshot("search_result.png")

                html = driver.page_source
                response_obj = Selector(text=html)

                yield {
                    'player_name': row[1],
                    'instagram_url_1' : response_obj.xpath("(//div[@class='g'])[1]/div[@class='rc']/div[@class='r']/a/@href").get(),
                    'following_1' : self.insta_following1(response_obj.xpath("((//div[@class='g'])[1]/div[@class='rc']/div[@class='s']/div/span/text())[last()]").get()),
                    'followers_1' : self.insta_followers1(response_obj.xpath("((//div[@class='g'])[1]/div[@class='rc']/div[@class='s']/div/span/text())[last()]").get()),
                    'instagram_url_2' : response_obj.xpath("(//div[@class='g'])[2]/div[@class='rc']/div[@class='r']/a/@href").get(),
                    'following_2' : self.insta_following2(response_obj.xpath("((//div[@class='g'])[2]/div[@class='rc']/div[@class='s']/div/span/text())[1]").get()),
                    'followers_2' : self.insta_followers2(response_obj.xpath("((//div[@class='g'])[2]/div[@class='rc']/div[@class='s']/div/span/text())[1]").get())
                }
