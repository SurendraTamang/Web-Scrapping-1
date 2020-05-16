# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyperclip

class PluginSpider(scrapy.Spider):
    name = 'plugin'

    place_ids = [
        'ChIJqenHL_PQ3ocROSBjP8S1nAs',
        'ChIJTWtMZ3223IcRcUdNJX5Uk00',
        'ChIJVXKiGGrP3ocRjslbaJPV1_U',
        'ChIJPTgKnAcm34cRUpKauRQrwoM'
    ]

    def start_requests(self):
        yield SeleniumRequest(
            url="https://webdevelopment111.com/directory/wp-admin/options-general.php?page=grw",
            wait_time=10,
            callback=self.parse
        )

    def parse(self, response):
        #global error_check

        driver = response.meta['driver']
        driver.set_window_size(1366, 768)
        login = driver.find_element_by_xpath("//input[@id='user_login']")
        login.send_keys("Byomakesh")
        time.sleep(2)
        password = driver.find_element_by_xpath("//input[@id='user_pass']")
        password.send_keys("4Temp2Test!")
        time.sleep(2)
        password.send_keys(Keys.ENTER)
        time.sleep(5)
        shortcode_tab = driver.find_element_by_xpath("//div[@class='nav-tab-wrapper']/a[text()='Shortcode']")
        shortcode_tab.click()
        time.sleep(5)
        for id in self.place_ids:
            driver.find_element_by_xpath("//input[@class='grw-place-id']").clear()
            place_id_box =  driver.find_element_by_xpath("//input[@class='grw-place-id']")
            place_id_box.send_keys(id)
            connect_button =  driver.find_element_by_xpath("//button[text()='Connect Google']")
            connect_button.click()
            time.sleep(5)

            # try:
            #     error_check = driver.find_element_by_xpath("//b[text()='Google error']")
            # except:
            text_area = driver.find_element_by_xpath("//textarea[@id='rplg_shortcode']")
            text_area.click()
            time.sleep(1)
            result = pyperclip.paste()
            time.sleep(1)

            yield{
                'URL': result.encode('UTF-8')

            }
       
