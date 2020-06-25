# -*- coding: utf-8 -*-
import scrapy


class RevzillaspiderSpider(scrapy.Spider):
    name = 'revzillaSpider'

    def filter_answer(self, value):
        answer = "".join(value[1:])
        return answer

    def filter_question(self, value):
        question = "".join(value)
        return question
    
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.revzilla.com/faq",
            callback=self.parse
        )

    def parse(self, response):
        listings = response.xpath("//section//strong[text()='A)']/parent::p")
        for lists in listings:
            yield{
                'question': self.filter_question(lists.xpath(f"normalize-space(.//preceding-sibling::h2[1]/text())").getall()),
                'answer': self.filter_answer(lists.xpath(".//text()").getall()),
                'url': response.url,
                'category': 'Others',
                'company': 'revzilla'
            }
