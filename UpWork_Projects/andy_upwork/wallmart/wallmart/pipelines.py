# -*- coding: utf-8 -*-

import mysql.connector
import logging


class MySQLPipeline(object):

    def open_spider(self, spider):
        # Set your database connection details
        self.connection = mysql.connector.connect(host="localhost", user="root", password="3699")

        # Craeting a cursor object, DB & Tables
        self.c = self.connection.cursor()
        self.c.execute("create database if not exists Wallmart")
        self.c.execute("use Wallmart")
        self.c.execute('''
            CREATE TABLE if not exists HomeFurnitureAppliances(
                url VARCHAR(300) PRIMARY KEY,
                productName TEXT,
                price TEXT,
                lvl1_category TEXT,
                lvl2_category TEXT,
                lvl3_category TEXT,
                lvl4_category TEXT
            )
        ''')
        self.connection.commit()
        logging.warning("Connection established to DATABASE !")

    def close_spider(self, spider):
        self.connection.close()
        logging.warning("Connection to DATABASE closed !")

    def process_item(self, item, spider):

        # Stores only the unique listings to the databse.
        try:
            self.c.execute('''
                INSERT INTO HomeFurnitureAppliances (url,productName,price,lvl1_category,lvl2_category,lvl3_category,lvl4_category) VALUES(%s,%s,%s,%s,%s,%s,%s)
            ''', (
                item.get('product_url'),
                item.get('product_name'),
                item.get('product_price'),
                item.get('lvl1_cat'),
                item.get('lvl2_cat'),
                item.get('lvl3_cat'),
                item.get('lvl4_cat')
            ))
            self.connection.commit()
        except:
            logging.warning("Skipped duplicate lsiting")
        
        return item
