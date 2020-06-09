# -*- coding: utf-8 -*-
import scrapy
import time
import json
from datetime import date, datetime


class NsmspiderSpider(scrapy.Spider):
    name = 'nsmSpider'

    start = 0
    total_count = 0
    today = str(date.today())

    def format_dateTime(self, dt):
        try:
            f_dt1 = dt.replace('T', ' ')
            f_dt2 = f_dt1.replace('Z', '')
            dt_final = datetime.strptime(f_dt2, "%Y-%m-%d %H:%M:%S")
            return dt_final
        except:
            return None

    payload = {
        "from": 0,
        "size": "1000",
        "sort": "publication_date",
        "keyword": None,
        "sortorder": "desc",
        "criteriaObj": {
            "criteria": [
                {
                    "name": "lei",
                    "value": [
                        "",
                        "",
                        "",
                        ""
                    ]
                }
            ],
            "dateCriteria": [
                {
                    "name": "publication_date",
                    "value": {
                        "from": None,
                        "to": f"{today[8:]}/{today[5:7]}/{today[:4]}"
                    }
                }
            ]
        }
    }

    def start_requests(self):
        yield scrapy.Request(
            url='https://api.data.fca.org.uk/search?index=fca-nsm-searchdata',
            method='POST',
            body=json.dumps(self.payload),
            headers={
                'Content-Type': 'application/json'
            },
            callback=self.parse
        )

    def parse(self, response):
        resp_dict = json.loads(response.body)
        self.total_count = resp_dict.get('hits').get('total')
        listings = resp_dict.get('hits').get('hits')
        for lists in listings:        
            yield{
                'id': lists['_source'].get('seq_id'),
                'publication_dt': self.format_dateTime(lists['_source'].get('publication_date')),
                'document_dt': self.format_dateTime(lists['_source'].get('document_date')),
                'source': lists['_source'].get('source'),
                'lei': lists['_source'].get('lei'),
                'company_name': lists['_source'].get('company'),
                'description': lists['_source'].get('headline'),
                'description_url': f"https://data.fca.org.uk/artefacts/{lists['_source'].get('download_link')}",
                'category': lists['_source'].get('type'),
                'classification': lists['_source'].get('classifications')
            }   
            
        self.start += 1000
        if self.start < self.total_count:         # Comment out this line, once we set the spider to crawl at an interval of 10 minutes. 
        #if self.start < 2000:                    # Uncomment this line, once we set the spider to crawl at an interval of 10 minutes 
            payload = {
                "from": self.start,
                "size": "1000",
                "sort": "publication_date",
                "keyword": None,
                "sortorder": "desc",
                "criteriaObj": {
                    "criteria": [
                        {
                            "name": "lei",
                            "value": [
                                "",
                                "",
                                "",
                                ""
                            ]
                        }
                    ],
                    "dateCriteria": [
                        {
                            "name": "publication_date",
                            "value": {
                                "from": None,
                                "to": f"{self.today[8:]}/{self.today[5:7]}/{self.today[:4]}"
                            }
                        }
                    ]
                }
            }
            #print(payload)
            time.sleep(30)
            yield scrapy.Request(
                url='https://api.data.fca.org.uk/search?index=fca-nsm-searchdata',
                method='POST',
                body=json.dumps(payload),
                headers={
                    'Content-Type': 'application/json'
                },
                callback=self.parse
            )
