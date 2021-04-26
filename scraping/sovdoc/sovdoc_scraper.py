#!/usr/bin/python3
"""
This is a webscraper that goes through the Russian Archives' Soviet Document collection using an api (http://sovdoc.rusarchives.ru/api/) to collect information relating to the Spanish Civil War. The information is parsed, passed to Google translate when need be, and stored."


Running: 
```

export GOOGLE_APPLICATION_CREDENTIALS="<google translate api JSON verification file>"
python3 -m sovdoc_scraper.py -o sovdoc_data.json


```

"""
from scrapy import Spider, Request, Item, Field
import json
from  pprint import pprint
import os
import requests
from requests.utils import quote
from google.cloud import translate_v2 as translate


# Starting node for the SCW collection
BASE_URL = 94999

def get_sovdoc_url(card_id, info=""):
    """ Returns the sovdoc api endpoint for a given id, info can be "childs" or "images" """
    return "http://sovdoc.rusarchives.ru/api/public/sections/233826/cards/" + str(card_id) + (("/" + info + "?page=1&size=4000") if info else "")

def get_card_id(path):
    """ Returns the card id given a path. """
    return os.path.basename(path.replace('/images', '').replace('/childs', '').replace('?page=1&size=4000', ''))

class SovDocItem(Item):
    id = Field()
    dates = Field()
    
    code = Field()
    name = Field()
    annotation = Field()
    
    docKind = Field()
    notes = Field()
    
    children = Field()
    images = Field()

class SovDocSpider(Spider):
    name = 'sovdoc'
    start_urls = [get_sovdoc_url(BASE_URL)]
    
    def parse(self, response):
        current_url = response.url
        current_id = get_card_id(current_url)

        item = SovDocItem()
        
        # Scrape the info page data and sanitize/format a little to fit into our style
        response_json = json.loads(str(response.body, 'utf-8'))
        response_json['docKind'] = response_json['series']['docKind'] if 'series' in response_json else ''
        response_json['notes'] = response_json['series']['notes'] if 'series' in response_json else ''
        for i in item.fields:
            response_json[i] = response_json[i] if i in response_json and response_json[i] else ''
        child_count = response_json['cnts']['childs']
        response_json['children'] = []
        response_json['images'] = []

        trans_payload = {res:response_json[res] for res in response_json if res in item.fields}
        
        pprint(trans_payload)

        # Grab and translate the fields the need it
        keys = [i for i in {'name', 'annotation', 'docKind', 'notes'} if trans_payload[i]]
        d = [trans_payload[k] for k in keys]
        translate_client = translate.Client()
        trans_return = translate_client.translate(d, target_language='en', source_language='ru')
        trans_return = d
        pprint(trans_return)
        
        # Store the translated fields with the rest of the data
        for i in range(len(keys)):
            trans_payload[keys[i]] = trans_return[i]['translatedText']

        pprint(trans_payload)
        
        # Scan child nodes/images
        item = SovDocItem(trans_payload)
        child_type = 'childs' if child_count else 'images'
        yield Request(url=get_sovdoc_url(current_id, child_type),
                             callback=self.parse_children,
                             meta={'item':item})
        
    def parse_children(self, response):
        result = json.loads(response.body)
        item = response.meta['item']
        # Subdirectory, scan each sub item
        if 'childs' in result.keys():
            item['children'] = [child['id'] for child in result['childs']['data']]
            for child in result['childs']['data']:#[1:2]:
                yield Request(url=get_sovdoc_url(child['id']), callback=self.parse)
                pass
        # Images, store them in the parents image field
        elif 'data' in result.keys():
            # Flatten the list to save space, format: [[basedir1, [file1, file2]], [basedir2, [file1, file2]]]
            res = []
            for i in result['data']:
                head, tail = os.path.split(i['url'])
                if res and res[-1][0] == head:
                    res[-1][1].append(tail)
                else:
                    res.append([head, [tail]])
            item['images'] = res
            
        pprint(item)
        yield item

