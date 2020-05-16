# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3

class MongoDBPipeline(object):
    collection_name = "Best Deals"
    # @classmethod
    # def from_crawler(cls, crwaler):
    #     logging.warning(crwaler.settings.get("MONGO_URI"))

    def open_spider(self, spider):
        #logging.warning("SPIDER OPENED FROM PIPELINE")
        self.client = pymongo.MongoClient("mongodb+srv://byom26:test123@cluster0-pljg5.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client["ComputerDeals"]

    def close_spider(self, spider):
        #logging.warning("SPIDER CLOSED FROM PIPELINE")
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

class SQLitePipeline(object):
    def open_spider(self, spider):
        self.connection = sqlite3.connect("ComputerDeals")
        try: # => To handle the error if database already exists
            self.c = self.connection.cursor()
            self.c.execute('''
                CREATE TABLE bestDeals(
                    name TEXT,
                    link TEXT,
                    storeName TEXT,
                    price TEXT
                )
            ''')
        except sqlite3.OperationalError:
            pass
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO bestDeals (name,link,storeName,price) VALUES(?,?,?,?)
        ''', (
            item.get('name'),
            item.get('link'),
            item.get('store_name'),
            item.get('price')
        ))
        self.connection.commit()
        return item
