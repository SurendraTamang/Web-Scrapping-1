#!/bin/bash
source /home/p.byom26/residentialReits/wsEnv/bin/activate

cd /home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes/essexAPI
scrapy crawl essexCmty -o apmtUrls.csv
sleep 2

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

cd /home/p.byom26/residentialReits/rrScrapers/clipperrealty
scrapy crawl clipper -o today.csv
sleep 2
python gBucket.py
sleep 2

cd /home/p.byom26/residentialReits/rrScrapers/maac
scrapy crawl maa -o today.csv
sleep 2
python gBucket.py
sleep 2

cd /home/p.byom26/residentialReits/rrScrapers/camdenliving
scrapy crawl camden -o today.csv
sleep 2
python gBucket.py
sleep 2

cd /home/p.byom26/residentialReits/rrScrapers/avalonCommunities
scrapy crawl avalon -o today.csv
sleep 2
python gBucket.py
sleep 2

cd /home/p.byom26/residentialReits/rrScrapers/equityapartments
scrapy crawl equity -o today.csv
sleep 2
python gBucket.py
sleep 2

cd /home/p.byom26/residentialReits/rrScrapers/aimco
scrapy crawl apiTest -o today.csv
sleep 2
python gBucket.py
sleep 2

deactivate
