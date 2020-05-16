# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
import time

class CoursesSpider(scrapy.Spider):
    name = 'courses'
    # allowed_domains = ['www.udemy.com']
    # start_urls = ['https://www.udemy.com/']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.udemy.com/courses/business/home-business',
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        time.sleep(2)
        html = driver.page_source
        response_obj = Selector(text=html)

        listings = response_obj.xpath("//div[@class='curriculum-course-card--container--1ZgwU']/div")
        for listing in listings:
            course_url = f'''https://www.udemy.com{listing.xpath(".//a/@href").get()}'''
            
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(course_url)
            time.sleep(2)

            course_html = driver.page_source
            course_response_obj = Selector(text=course_html)

            title = course_response_obj.xpath("normalize-space(//h1[@class='clp-lead__title ']/text())").get()
            sub_title = course_response_obj.xpath("normalize-space(//div[@class='clp-lead__headline']/text())").get()
            price = course_response_obj.xpath("normalize-space(//div[contains(@class, 'course-price-text')]//span[2]/span/text())").get()
            ratings = course_response_obj.xpath("normalize-space((//div[@class='rate-count']/span/text())[5])").get()
            avg_ratings = course_response_obj.xpath("normalize-space((//div[@class='rate-count']/span/span/text())[4])").get()

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            yield{
                'title': title,
                'sub_title': sub_title,
                'price': price,
                'ratings': ratings,
                'avg_ratings': avg_ratings,
                'url': course_url
            }

        # next_page = response_obj.xpath("//span[@aria-label='Next']/parent::a/@href").get()
        # if next_page:
        #     yield SeleniumRequest(
        #         url=f"https://www.udemy.com{next_page}",
        #         wait_time=5,
        #         callback=self.parse
        #     )      
