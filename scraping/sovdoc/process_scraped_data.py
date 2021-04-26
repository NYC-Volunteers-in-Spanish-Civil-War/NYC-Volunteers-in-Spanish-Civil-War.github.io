#!/usr/bin/python3
"""
A small script that formats the data by document and by tags.

Running:
```
python3 process_scraped_data.py
```

"""
import re
import json
from pprint import pprint

# Each file/folder in the dataset
MASTER_DATA = {}
# A dataset of fields and tags
META_TAGS = {}

sovdoc_data = {item['id']:item for item in json.loads(open('sovdoc_data.json', 'r').read())}
interbrigades_data = json.loads(open('interbrigades_data.json', 'r').read())

# A function to turn various iterations of the directory locations into a single consistent one with only digits seperated by periods.
standardize = lambda text: "_".join(re.findall("\w*(?<!_)\d+", text))

# Loop over sovdoc data and clean, add to master dataset
for item in sovdoc_data:
    id = standardize(sovdoc_data[item]['code'])
    sovdoc_data[item]['sovdoc_id'] = sovdoc_data[item]['id']
    sovdoc_data[item]['id'] = id
    del sovdoc_data[item]['code']
    MASTER_DATA[id] = sovdoc_data[item]

# Change child references to use the standardized id and adding child count
for item in sorted(list(MASTER_DATA.keys())):
    if 'children' in MASTER_DATA[item]:
        MASTER_DATA[item]['children'] = [sovdoc_data[child]['id'] for child in MASTER_DATA[item]['children']]
        MASTER_DATA[item]['child_count'] = len(MASTER_DATA[item]['children'])

# Further flatten/condense image data and adding child count
for item in MASTER_DATA:
    MASTER_DATA[item]['images'] = [
        [img_set[0].replace("http://sovdoc.rusarchives.ru", "") + "/IMG0", img_set[1][0][4:7], img_set[1][-1][4:7], ".JPG"]
        for img_set in MASTER_DATA[item]['images']]
    if MASTER_DATA[item]['images'] and not MASTER_DATA[item]['child_count']:
        MASTER_DATA[item]['child_count'] = sum([int(i[2]) - int(i[1]) for i in MASTER_DATA[item]['images']])
               
# Integrate metadata from the interbrigades files into masterdata and tags dict
for item in interbrigades_data:
    id = standardize(item['id'])
    MASTER_DATA[id]['interbrigades_code'] = item['id']
    MASTER_DATA[id]['interbrigades_id'] = item['node_number']
    del item['node_number']
    del item['id']
    # Remove trailing periods
    MASTER_DATA[id]['meta'] = {k.strip('.'): [v.strip('.') for v in item[k]] for k in item}
    for field in MASTER_DATA[id]['meta']:
        META_TAGS.setDefault(field, {})
        for tag in MASTER_DATA[id]['meta'][field]:
            META_TAGS[field].setDefault(tag, {}).append(id)


    pprint(MASTER_DATA[id])

META_TAGS = { **{'tags': list(META_TAGS.keys())}, **{field:list(META_TAGS[field].keys()) for field in META_TAGS}, **{field + '_'  + tag:META_TAGS[field][tag] for field in META_TAGS for tag in META_TAGS[field]}}

json.dump(MASTER_DATA, open('documents.json', 'w+'))
json.dump(META_TAGS, open('meta_tags.json', 'w+'))


    
