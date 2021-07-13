"""
Handles the main editor for managing site content.
"""
from flask import render_template
from . import *


STATIC_DATA = {}

def get_file_checksum(filename, url=False):
    """ Returns md5 checksum of given file or url. """
    hash_md5 = md5()
    if not url:
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    else:
        r = requests.get(filename)
        for chunk in r.iter_content(4096):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
def get_key_hash(key):
    """ Returns a simple hash of the given key. """
    print(key)
    return md5(key.encode('utf-8')).hexdigest()
def get_data_filename(key):
    """ Returns the location of a keys data file. """
    return 'archive/data/' + key + '.json'
def get_status(key, checksum):
    """ Given the key and the checksum, give the status. """
    url = "https://nyc-volunteers-in-spanish-civil-war.github.io/archive/data/master.json"
    response = urllib.request.urlopen(url)
    published_json = json.loads(response.read())
    if key not in published_json.keys():
        return "UNPUBLISHED"
    clean = lambda data: {key:data[key] for key in data if key != "status"}
    if published_json[key]["checksum"] == checksum:
        return "PUBLISHED"
    return "MODIFIED"
def delete_key_data(key):
    """ Deletes a user from local memory. Returns the local master data. """
    json_data = get_data_from_file(MASTER_FILE)
    del json_data[key]
    os.remove(get_data_filename(key))
    write_data_to_file(MASTER_FILE, json_data)
    return json_data
def update_status_and_checksum(key, key_data):
    """ Updates the status and checksum of a given key. """
    checksum = get_file_checksum(get_data_filename(key))
    status = get_status(key, checksum)
    key_data['checksum'] = checksum
    key_data['status'] = status

def update_static_data():
    """ Updates a global dictionary linking volunteer names to their data. """
    master_data = get_data_from_file(MASTER_FILE)
    for key in master_data:
        data = get_data_from_file(get_data_filename(key))
        name = quote_plus(data['volunteer_fname'] + " " + data['volunteer_lname'])
        name = data['volunteer_fname'] + " " + data['volunteer_lname']
        STATIC_DATA[name] =  data



@routes.route('/delete', methods=['POST'])
def delete():
    key = request.form.get('key')
    delete_key_data(key)
    return ('', 204)
@routes.route('/delete_image', methods=['POST'])
def delete_image():
    key = request.form.get('key')
    data = request.form.get('data')
    data_file = get_data_filename(key)
    json_data = get_data_from_file(data_file)
    if data in json_data['volunteer_images']:
        json_data['volunteer_images'].remove(data)
    elif data in json_data['school_crests']:
        json_data['school_crests'].remove(data)
    write_data_to_file(data_file, json_data)
    master_data = get_data_from_file(MASTER_FILE)
    update_status_and_checksum(key, master_data[key])
    write_data_to_file(MASTER_FILE, master_data)
    return ('', 204)
@routes.route('/upload_changes', methods=['POST'])
def upload_changes():
    action = request.form.get('action')
    url = "https://nyc-volunteers-in-spanish-civil-war.github.io/archive/data/master.json"
    #Returns if any changes have been made locally that need to be pushed
    if action == 'changes_made':
        local_checksum = get_file_checksum(MASTER_FILE)
        
        remote_checksum = get_file_checksum(url, True)
        if local_checksum != remote_checksum:
            local_json = get_data_from_file(MASTER_FILE)
            remote_json = get_data_from_file(url, True);

            data = {
                "created": {key:local_json[key] for key in list(set(local_json.keys()) - set(remote_json.keys()))},
                "deleted": {key:remote_json[key] for key in list(set(remote_json.keys()) - set(local_json.keys()))},
                "modified": {key:local_json[key] for key in set(remote_json.keys()) & set(local_json.keys()) if remote_json[key]['checksum'] != local_json[key]['checksum']}
            }
            local_set = set([(key, local_json[key]['checksum']) for key in local_json.keys()])
            return (data, 200)
        return ('', 404)
    #Attempts to push changes that need to be pushed
    elif action == 'push_changes':
        volunteer_name = lambda d: d['volunteer_fname'] + ' ' + d['volunteer_lname']
        local_json = get_data_from_file(MASTER_FILE)
        remote_json = get_data_from_file(url, True);

        changes = json.loads(request.form.get('changes'))
        message = ""
        #First set everything to PUBLISHED        
        for key in local_json:
            local_json[key]['status'] = 'PUBLISHED'
        for change in changes:
            key, type = change['key'], change['type']
            if type == 'deleted':
                message += 'Deleted record for ' + volunteer_name(remote_json[key]) + '. '
                del remote_json[key]
            elif type == 'created':
                message += 'Added record for ' + volunteer_name(local_json[key]) + '. '
                remote_json[key] = local_json[key]
            else:
                message += 'Modifed record for ' + volunteer_name(local_json[key]) + '. '
                remote_json[key] = local_json[key]
                
        os.system('git add archive/')
        write_data_to_file(MASTER_FILE, remote_json)
        os.system("git add archive/data/master.json")
        write_data_to_file(MASTER_FILE, local_json)
        os.system('git add sitemap.xml')
        os.system('git commit -m "' + message + '"')
        push_command = "git push https://{}:{}@github.com/NYC-Volunteers-in-Spanish-Civil-War/NYC-Volunteers-in-Spanish-Civil-War.github.io.git".format(
            request.form.get('username'),
            request.form.get('password'))
        try:
            push_result = subprocess.check_output(push_command, shell=True, text=True)
            if "Invalid username or password" in push_result:
                return ('', 404)
            return ('', 204)
        except subprocess.CalledProcessError as e:
            return ('', 404)
        return ('', 204)

@routes.route('/upload.html', methods=['GET', 'POST'])
def upload():
    master_data = get_data_from_file(MASTER_FILE)
    tags = set([tag for key in master_data for tag in master_data[key]['tags']])
    write_data_to_file("archive/data/tags.json",
                       {t:{"description":"",
                           "locations":[key for key in master_data if t in master_data[key]['tags']]}
                        for t in tags})
    tags = get_data_from_file("archive/data/tags.json")
    if request.method == 'POST':
        new_key = get_key_hash(request.form.get('volunteer_lname') + "_" + request.form.get('volunteer_fname'))
        key = request.form.get('key')
        key = key if key != 'None' else ''
        data = {
            "student_fname": request.form.get('student_fname'),
            "student_lname": request.form.get('student_lname'),
            "class": request.form.get('class'),
            "volunteer_fname": request.form.get('volunteer_fname'),
            "volunteer_lname": request.form.get('volunteer_lname'),
            "data": request.form.get('ckeditor'),
            "sources": request.form.get('sources'),
            "volunteer_images": json.loads(request.form.get('volunteer_images_hidden')),
            "school_crests": json.loads(request.form.get('school_crests_hidden')),
            "tags": json.loads(request.form.get('tags'))}
        redir = False
        if key and key != new_key:
            delete_key_data(key)
        if not key or key != new_key:
            key = new_key
            redir = True

        data_file = get_data_filename(key)
        write_data_to_file(data_file, data)
        [data.pop(k) for k in ["volunteer_images", "school_crests"]]
        update_status_and_checksum(key, data)
        master_data[key] = data
        write_data_to_file(MASTER_FILE, master_data)
        update_static_data()
        trigger_archive_build()
        if redir:
            return ({'redirect': 'upload.html?key=' + key}, 200)
        return data['status']
    else:
        data = {
            "student_fname": "",
            "student_lname": "",
            "class": "",
            "volunteer_fname": "",
            "volunteer_lname": "",
            "data": "",
            "sources": "",
            "volunteer_images": "",
            "school_crests": "",
            "tags": ""}
        if request.args.get('key'):
            data = get_data_from_file(get_data_filename(request.args.get('key')))
        return render_template("upload.html", data=data, master_list=master_data, key=request.args.get('key'), tags=tags)


