#!/bin/bash
source /home/p.byom26/residentialReits/wsEnv/bin/activate

cd /home/p.byom26/residentialReits/rrScrapers/iretApartments
scrapy crawl iret -o today.csv
sleep 2
python gBucket.py
sleep 2

cd /home/p.byom26/residentialReits/rrScrapers/americanhomes4rent
scrapy crawl americanhomes -o today.csv
sleep 2
python gBucket.py
sleep 2

cd /home/p.byom26/residentialReits/rrScrapers/udr
scrapy crawl udrdotcom -o today.csv
sleep 2
python gBucket.py
sleep 2

cd /home/p.byom26/residentialReits/rrScrapers/essexapartmenthomes
scrapy crawl essex -o today.csv
sleep 2
python gBucket.py
sleep 2

deactivate
