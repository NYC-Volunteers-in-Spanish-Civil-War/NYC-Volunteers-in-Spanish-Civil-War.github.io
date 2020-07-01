import os
import subprocess
import json
import bisect
import urllib
import requests
import webbrowser
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_ckeditor import CKEditor, upload_success, upload_fail
from hashlib import md5

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_HEIGHT'] = 500
ckeditor = CKEditor(app)

MASTER_FILE = 'archive/data/master.json'
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
def get_data_from_file(filename):
    """ Returns the json data in a given file. """
    with open(filename, 'r') as f:
        return json.load(f)
def write_data_to_file(filename, data):
    """ Writes data to a json file. """
    with open(filename, 'w+') as f:
        json.dump(data, f, indent=4, sort_keys=True)
def get_key_hash(key):
    """ Returns a simple hash of the given key. """
    return md5(key).hexdigest()
def get_data_filename(key):
    """ Returns the location of a keys data file. """
    return 'archive/data/' + key + '.json'
def get_status(key, checksum):
    """ Given the key and the checksum, give the status. """
    url = "https://nyc-volunteers-in-spanish-civil-war.github.io/archive/data/master.json"
    response = urllib.urlopen(url)
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
@app.route('/delete', methods=['POST'])
def delete():
    key = request.form.get('key')
    delete_key_data(key)
    return ('', 204)
@app.route('/delete_image', methods=['POST'])
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
@app.route('/upload_changes', methods=['POST'])
def upload_changes():
    action = request.form.get('action')
    #Returns if any changes have been made locally that need to be pushed
    if action == 'changes_made':
        local_checksum = get_file_checksum(MASTER_FILE)
        url = "https://nyc-volunteers-in-spanish-civil-war.github.io/archive/data/master.json"
        remote_checksum = get_file_checksum(url, True)
        if local_checksum != remote_checksum:
            return ('', 204)
        return ('', 404)
    #Attempts to push changes that need to be pushed
    elif action == 'push_changes':
        local_json = get_data_from_file(MASTER_FILE)
        #First set everything to PUBLISHED
        for key in local_json:
            local_json[key]['status'] = 'PUBLISHED'
        write_data_to_file(MASTER_FILE, local_json)
        #Push the changes to the data
        os.system("git add archive/data/*")
        os.system('git commit -m "Updated archive data."')
        push_command = "git push https://{}:{}@github.com/NYC-Volunteers-in-Spanish-Civil-War/NYC-Volunteers-in-Spanish-Civil-War.github.io.git".format(
            request.form.get('user'),
            request.form.get('pass'))
        try:
            push_result = subprocess.check_output(push_command, shell=True)
            print push_result
            if "Invalid username or password" in push_result:
                return ('', 404)
            return ('', 204)
        except subprocess.CalledProcessError as e:
            return ('', 404)
        return ('', 204)

@app.route('/', methods=['GET', 'POST'])
def main():
    master_data = get_data_from_file(MASTER_FILE)
    if request.method == 'POST':
        new_key = get_key_hash(request.form.get('volunteer_lname') + "_" + request.form.get('volunteer_fname'))
        key = request.form.get('key')
        data = {
            "student_fname": request.form.get('student_fname'),
            "student_lname": request.form.get('student_lname'),
            "class": request.form.get('class'),
            "volunteer_fname": request.form.get('volunteer_fname'),
            "volunteer_lname": request.form.get('volunteer_lname'),
            "data": request.form.get('ckeditor'),
            "volunteer_images": json.loads(request.form.get('volunteer_images_hidden')),
            "school_crests": json.loads(request.form.get('school_crests_hidden'))}
        redir = False
        if key and key != new_key:
            delete_key_data(key)
            key = new_key
            redir = True
        if not key:
            key = new_key
            redir = True
        data_file = get_data_filename(key)
        write_data_to_file(data_file, data)
        [data.pop(k) for k in ["data", "volunteer_images", "school_crests"]]
        update_status_and_checksum(key, data)
        master_data[key] = data
        write_data_to_file(MASTER_FILE, master_data)
        if redir:
            return ({'redirect': '/?key=' + key}, 200)
        return render_template("upload.html", data=data, master_list=master_data, key=key)
    else:
        data = {
            "student_fname": "",
            "student_lname": "",
            "class": "",
            "volunteer_fname": "",
            "volunteer_lname": "",
            "data": "",
            "volunteer_images": "",
            "school_crests": ""}
        if request.args.get('key'):
            data = get_data_from_file(get_data_filename(request.args.get('key')))
        return render_template("upload.html", data=data, master_list=master_data, key=request.args.get('key'))

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000?key=', new=1)
    app.run(debug=True)

