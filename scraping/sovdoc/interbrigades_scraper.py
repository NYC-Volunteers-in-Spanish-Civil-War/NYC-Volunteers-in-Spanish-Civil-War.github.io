#!/usr/bin/python3
"""
This is a webscraper that scrapes the metadata from the Records of the International Brigades located at (http://interbrigades.inforost.org) to supplement the data collected from the SovDoc scraper. Since there is a lot of repetition in the metadata, a dictionary is used to cache translations. The translations also replace numbers with generic symbols so only the text and not the numbers have to match  

Running: 
```
export GOOGLE_APPLICATION_CREDENTIALS="<google translate api JSON verification file>"
python3 -m interbrigades_scraper.py -o interbrigades_data.json


```

"""
from scrapy import Spider, Request, Item, Field
import json
from  pprint import pprint
import os
import requests
from requests.utils import quote
from google.cloud import translate_v2 as translate
import re

# Cached translations
CACHE = {}

# Maps info page labels to correct Item field
MAP_DICT = {"Author(s)": "authors",
            "Language(s)": "languages",
            "Document type": "docType",
            "Names": "names",
            "Organizations": "organizations",
            "Subject": "subject"
}

# A translation client
CLIENT  = translate.Client()

def sanitize(text):
    """ Removes specific numbers from the item and replaces them with placeholders. Returns the new text and the removed numbers. """
    nums = re.findall("\w*(?<!_)\d+", text)
    i = 0
    while re.search("\w*(?<!_)\d+", text):
        text = re.sub("\w*(?<!_)\d+", "_" + str(i), text, 1)
        i += 1
    return text, nums

def add_to_dict(my_dict, text):
    """ Sanitized then translates the text and adds it to the dict. Returns true if added for the first time"""
    sanitized, nums = sanitize(text)
    if sanitized not in my_dict:
        trans_return = CLIENT.translate(sanitized, target_language='en', source_language='ru')
        my_dict[sanitized] = trans_return['translatedText']
    return sanitized, nums
    
def translate(my_dict, text):
    """ Translates the item and saves it into the dict. """
    text, nums = add_to_dict(my_dict, text)
    translated = my_dict[text]
    for i in range(len(nums)):
        translated = translated.replace("_" + str(i), nums[i], 1)
    return translated

def get_interbrigades_url(id):
    """ Returns the interbrigades page api for a given id, info can be "childs" or "images" """
    return "http://interbrigades.inforost.org/nodes/" + id + "?locale=en"


class InterbrigadesItem(Item):
    id = Field()
    node_number = Field()
    
    authors = Field()
    languages = Field()
    docType = Field()
    names = Field()
    organizations = Field()
    occupation = Field()
    subject = Field()

class InterbrigadesSpider(Spider):
    name = 'interbrigades'
    start_urls = ["http://interbrigades.inforost.org/indexes/idnos?per_page=4000"]
    
    def parse(self, response):
        """ Loop through the rows of number ids and archival identifiers, pass that information to  with passing page metadata """
        rows = response.css('.sortable-table tr')
        for row in rows[1:]:
            item = InterbrigadesItem(id=row.css('td:nth-child(2) a::text').get(),
                                     node_number=row.css('td:nth-child(1) a::text').get())
            yield Request(url=get_interbrigades_url(row.css('td:nth-child(1) a::text').get()),
                          callback=self.parse_children,
                          meta={'item':item})
        
    def parse_children(self, response):
        """ Fill in the metadata and translate the required Sections. """
        item = response.meta['item']
        metadata = response.css('#metadata dl')
        for row in metadata:
            key = row.css('dt::text').get()
            vals = row.css('dd a::text ').getall()
            if key in MAP_DICT:
                item[MAP_DICT[key]] = vals
        for field in item.fields - 'id':
            if field in item:
                item[field] = [translate(CACHE, i) for i in item[field]]
        pprint(item)
        yield item

