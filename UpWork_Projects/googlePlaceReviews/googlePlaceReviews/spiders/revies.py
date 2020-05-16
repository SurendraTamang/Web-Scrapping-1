# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import pyperclip


class ReviesSpider(scrapy.Spider):
    name = 'revies'
    # allowed_domains = ['www.google.com']
    # start_urls = ['http://www.google.com/']

    # def check_element_present(self, value):
    #     try:
    #         driver.find_element_by_xpath(value)
    #     except NoSuchElementException:
    #         return False
    #     return True

    def start_requests(self):
        yield SeleniumRequest(
            url="https://www.google.com/search?hl=en&sxsrf=ALeKk03hmClnXr3tL9nS2FlxlyyE6U-FCg%3A1587800866332&source=hp&ei=IuujXvv9Efmb4-EP9OK98AQ&q=Willow+Spring+Trail+California+&oq=Willow+Spring+Trail+California+&gs_lcp=CgZwc3ktYWIQAzIHCCMQrgIQJ1D4NFj4NGDqPGgCcAB4AIAB0AGIAdABkgEDMi0xmAEAoAECoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwj7lvCUi4PpAhX5zTgGHXRxD04Q4dUDCAc&uact=5",
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):

        driver = response.meta['driver']
        driver.find_element_by_xpath("//input[@aria-label='Search']").clear()
        #time.sleep(3)
        search_box = driver.find_element_by_xpath("//input[@aria-label='Search']")
        #search_box.send_keys("Willow Spring Trail California")
        search_box.send_keys("mysore palace")
        #search_box.send_keys("Routeburn Track: Key Summit to Lake Sylvan Otago")
        #search_box.send_keys("Sylter Ellenbogen List Schleswig-Holstein")
        search_box.send_keys(Keys.ENTER)
        #driver.execute_script("window.scrollBy(0,1000);")
        time.sleep(3)

        # if driver.find_element_by_xpath("//cite[text()='www.tripadvisor.com']"):
        initial_html = driver.page_source
        response_obj = Selector(text=initial_html)
        if len(response_obj.xpath("//cite[text()='www.tripadvisor.com']"))>0:
            tripadvisor_url = response_obj.xpath("//cite[text()='www.tripadvisor.com']/parent::div/parent::a/@href").get()

            driver.execute_script("window.open('');")
            #time.sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            driver.get(tripadvisor_url)
            time.sleep(10)
            print(f"CURRENT URL: {driver.current_url}")
            driver.close()
            #time.sleep(3)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(5)
        elif len(response_obj.xpath("//span[text()='View all Google reviews']"))>0:
            reviews = driver.find_element_by_xpath("//span[text()='View all Google reviews']")
            reviews.click()
            time.sleep(5)
            dateOfPost = driver.find_element_by_xpath("(//span[text()='Like'])[last()]")
            for _ in range(5):                
            #scroll_action = ActionChains(driver)
            #scroll_action.move_to_element(dateOfPost).perfowm().send_keys(Keys.ARROW_DOWN)
            #dateOfPost.click()
            #dateOfPost.send_keys(Keys.ARROW_DOWN)
            #driver.find_element_by_xpath("//g-review-stars[@style]/following-sibling::span[1]").send_keys(Keys.END)
                time.sleep(3)
            
                driver.execute_script('arguments[0].scrollIntoView(true);', dateOfPost)
            #driver.execute_script("window.scrollBy(0,1000);")
                time.sleep(2)
                dateOfPost = driver.find_element_by_xpath("(//span[text()='Like'])[last()]")
            gReviewsHTML = driver.page_source
            gReviewsHTML_response = Selector(text=gReviewsHTML)
            listings = gReviewsHTML_response.xpath("//div[@data-google-review-count]/div")
            overall_rating = gReviewsHTML_response.xpath("//div[@class='review-score-container']/div/span/text()").get()
            total_reviews = gReviewsHTML_response.xpath("//g-review-stars/following-sibling::div/span/text()").get()
            for listing in listings:
                if len(listing.xpath(".//div[@style='vertical-align:top']/div[2]/span/text()"))==0:
                    user_review = listing.xpath(".//span[@class='review-full-text']/text()").getall()
                else:
                    user_review = listing.xpath(".//div[@style='vertical-align:top']/div[2]/span/text()").get()
                #more = driver.find_element_by_xpath("(//a[text()='More'])[2]")
                # more.click()
                # driver.execute_script("window.scrollBy(0,1000);")
                # time.sleep(5)
                yield{
                    'overall_rating': overall_rating,
                    'total_noOF_reviews': total_reviews,
                    'user_review': user_review
                }
        else:
            pass

    def tripAdvisor(self, response):
        driver = response.meta['driver']
        curr_url = driver.curr_url
        if "tripadvisor.in" in curr_url:
            pass
        elif "tripadvisor.com" in curr_url:
            pass

    
    # def googleReviews(self, response):
    #     pass