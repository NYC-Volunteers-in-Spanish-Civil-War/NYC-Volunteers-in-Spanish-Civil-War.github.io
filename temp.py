import json
from hashlib import md5
json_data = {}
with open('archive/data.json', 'r') as f:
    json_data = json.load(f)
master_json = {}
for key in json_data:
    print key
    print json_data[key].keys()
    data = json_data[key]
    master_keys = ["status", "volunteer_lname", "volunteer_fname", "student_lname", "student_fname", "class"]
    master_data = {}
    for k in master_keys:
        master_data[k] = data[k]
    master_json[md5(key).hexdigest()] = master_data
    with open('archive/data/' + md5(key).hexdigest() + '.json', 'w+') as s:
        json.dump(data, s, indent=4, sort_keys=True)
with open('archive/data/master.json', 'w+') as f:
        json.dump(master_json, f, indent=4, sort_keys=True)
