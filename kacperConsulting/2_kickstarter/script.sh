#!/bin/bash
source /home/p.byom26/residentialReits/wsEnv/bin/activate
cd /home/p.byom26/residentialReits/rrScrapers/kickstarter
scrapy crawl kstr -o dataGCP.csv
