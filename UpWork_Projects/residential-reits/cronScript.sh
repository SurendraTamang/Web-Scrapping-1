#!/bin/bash
source /home/p.byom26/residentialReits/wsEnv/bin/activate
cd /home/p.byom26/residentialReits/rrScrapers/bsrreit
scrapy crawl bsrSpider -o today.csv
sleep 2
python gBucket.py
sleep 2
cd /home/p.byom26/residentialReits/rrScrapers/myMHcommunity
scrapy crawl mmcScraper -o today.csv
sleep 2
python gBucket.py
sleep 2
cd /home/p.byom26/residentialReits/rrScrapers/iretApartments
scrapy crawl iret -o today.csv
sleep 2
python gBucket.py
sleep 2
deactivate
