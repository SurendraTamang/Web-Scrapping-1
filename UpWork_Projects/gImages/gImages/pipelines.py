# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class GimagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'file_name': item.get('file_name')}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        image_name = request.meta['file_name']
        return 'testing_pipeline/%s.jpg' % (image_name)
