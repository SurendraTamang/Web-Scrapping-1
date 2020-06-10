# -*- coding: utf-8 -*-

import mysql.connector
import logging


class MySQLPipeline(object):
    # user = ""
    # password = ""

    def open_spider(self, spider):
        # Set your database connection details
        self.connection = mysql.connector.connect(host="localhost", user="root", password="3699")

        # Craeting a cursor object, DB & Tables
        self.c = self.connection.cursor()
        self.c.execute("create database if not exists nsw_db")
        self.c.execute("use nsw_db1")
        self.c.execute('''
            CREATE TABLE if not exists nsw_listings(
                id VARCHAR(300) PRIMARY KEY,
                publication_dt DATETIME,
                document_dt DATETIME,
                source TEXT,
                lei TEXT,
                company_name TEXT,
                description TEXT,
                description_url TEXT,
                category TEXT,
                classification TEXT
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
                INSERT INTO nsw_listings (id,publication_dt,document_dt,source,lei,company_name,description,description_url,category,classification) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (
                item.get('id'),
                item.get('publication_dt'),
                item.get('document_dt'),
                item.get('source'),
                item.get('lei'),
                item.get('company_name'),
                item.get('description'),
                item.get('description_url'),
                item.get('category'),
                item.get('classification')
            ))
            self.connection.commit()
        except:
            logging.warning("Skipped duplicate lsiting")
        
        return item