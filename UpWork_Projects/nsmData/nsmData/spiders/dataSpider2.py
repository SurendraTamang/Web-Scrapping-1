# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import date, datetime, timedelta


class Dataspider2Spider(scrapy.Spider):
    name = 'dataSpider2'

    total_count = 0
    start_dt = datetime(2010, 12, 24).date()
    end_dt = datetime(2010, 12, 31).date()
    today = date.today()

    def payload_dt(self,value):
        if value == None:
            return None
        else:
            return f"{str(value)[8:]}/{str(value)[5:7]}/{str(value)[:4]}"

    def format_dateTime(self, dt):
        try:
            f_dt1 = dt.replace('T', ' ')
            f_dt2 = f_dt1.replace('Z', '')
            dt_final = datetime.strptime(f_dt2, "%Y-%m-%d %H:%M:%S")
            return dt_final
        except:
            return None

    def gen_payload(self, start, frm_dt, to_dt):
        payload = {
            "from": start,
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
                                "from": self.payload_dt(frm_dt),
                                "to": self.payload_dt(to_dt)
                            }
                        }
                    ]
            }
        }
        return payload

    def start_requests(self):
        while self.end_dt <= self.today:
            self.start_dt = self.end_dt + timedelta(days=1)
            self.end_dt += timedelta(days=7)
            self.start = 0            
            
            yield scrapy.Request(
                url='https://api.data.fca.org.uk/search?index=fca-nsm-searchdata',
                method='POST',
                body=json.dumps(self.gen_payload(self.start, self.start_dt, self.end_dt)),
                headers={
                    'Content-Type': 'application/json'
                },
                callback=self.parse
            )
            
    def parse(self, response):
        resp_dict = json.loads(response.body)
        self.total_count = resp_dict.get('hits').get('total')
        print(self.total_count)
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

        if self.start < self.total_count:
            yield scrapy.Request(
                url='https://api.data.fca.org.uk/search?index=fca-nsm-searchdata',
                method='POST',
                body=json.dumps(self.gen_payload(self.start, self.start_dt, self.end_dt)),
                headers={
                    'Content-Type': 'application/json'
                },
                callback=self.parse
            )
