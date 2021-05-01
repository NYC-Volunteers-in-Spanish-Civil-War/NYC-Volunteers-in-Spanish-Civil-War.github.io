import os
import subprocess
import json
import bisect
import urllib
import requests
import webbrowser
import datetime
import jinja2
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, send_from_directory
from flask_ckeditor import CKEditor, upload_success, upload_fail
from hashlib import md5
from flask_frozen import Freezer
from pprint import pprint
from urllib.parse import quote_plus

app = Flask(__name__, static_url_path='')
freezer = Freezer(app, with_no_argument_rules=False, log_url_for=False)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_HEIGHT'] = 500

app.config['FREEZER_BLACKLIST'] = ['*ckeditor*', 'ckeditor.static']
app.config['FREEZER_DESTINATION_IGNORE'] = ['.git*', 'env*', 'scraping*', 'templates', 'update.py', '*.json', 'images*', 'js*', 'favicon.ico', 'css*', 'robots.txt', 'CNAME', '*.md', 'run.sh', '.emacs*', 'requirements.txt']
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_IGNORE_404_NOT_FOUND'] = True
app.config['FREEZER_DESTINATION'] = ''
#app.config['FREEZER_SKIP_EXISTING'] = True

ckeditor = CKEditor(app)

def hash(s):
    return md5(s.encode('utf-8')).hexdigest()

DEBUG = True


@app.context_processor
def inject_debug():
    return dict(debug=DEBUG)
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)


MASTER_FILE = 'archive/data/master.json'
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
def get_data_from_file(filename, url=False):
    """ Returns the json data in a given file. """
    if not url:
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        response = urllib.urlopen(filename)
        return json.loads(response.read())
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

def update_static_data():
    """ Updates a global dictionary linking volunteer names to their data. """
    master_data = get_data_from_file(MASTER_FILE)
    for key in master_data:
        data = get_data_from_file(get_data_filename(key))
        name = quote_plus(data['volunteer_fname'] + " " + data['volunteer_lname'])
        name = data['volunteer_fname'] + " " + data['volunteer_lname']
        STATIC_DATA[name] =  data
@freezer.register_generator
def misc_gen():
    return ['/index.html', '/context.html', '/archive/index.html', '/sources.html', '/map.html', '/contact.html']


@app.route('/')
@app.route('/index.html')
@app.route('/context.html')
@app.route('/archive/')
@app.route('/archive/index.html')
@app.route('/sources.html')
@app.route('/map.html')
@app.route('/contact.html')
def misc():
    print((request.path[1::] + ("index.html" if request.path[-1] == "/" else ""))) 
    return render_template(request.path[1::] + ("index.html" if request.path[-1] == "/" else ""))

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)
@app.route('/archive/data/<path:path>')
def send_archive_data(path):
    return send_from_directory('archive/data', path)

@freezer.register_generator
def site_map():
    yield '/sitemap.xml'
@app.route('/sitemap.xml')
def site_map():
    master_data = get_data_from_file(MASTER_FILE)
    documents = get_data_from_file('documents/documents.json')
    tags = get_data_from_file('documents/meta_tags.json')
    date = datetime.date.today()
    return render_template('sitemap.xml', master_data=master_data, documents=documents, tags=tags, date=date)



@app.route('/documents/<filename>.json')
def document_data(filename):
    data = json.loads(open('documents/' + filename + '.json', 'r').read())
    return data
@freezer.register_generator
def document_page_gen():
    data = json.loads(open('scraping/sovdoc/documents.json', 'r').read())
    i = 0.0
    for d in data:
        i += 1        
        print("Sovdoc Documents: " + str(i / len(data)))
        yield '/documents/' + d + '.html'
    yield '/documents/index.html'
@app.route('/documents/<id>.html')
def document_page(id):
    print(id)
    id = id if id != "index" else ""
    tags = json.loads(open('scraping/sovdoc/meta_tags.json', 'r').read())
    return render_template('documents/index.html', data=json.loads(open('scraping/sovdoc/documents.json', 'r').read()), tags=tags, id=id, hash=hash)

@freezer.register_generator
def document_tag_page_gen():
    queue = ['tags/']
    tags = json.loads(open('scraping/sovdoc/meta_tags.json', 'r').read())
    clean_name = lambda name: name.replace('.html', '').strip('/').split('/')[-1]
    i = 0.0
    while queue and (node := queue.pop(0)):
        i += 1
        if '.html' not in node:
            children = [node + child + ('.html' if any(['545' in c for c in tags[clean_name(child)]]) else '/')  for child in tags[clean_name(node)]]
            queue += children
        print("Sovdoc Tags: " + str(i / len(tags)))
        yield '/documents/' + node
    yield '/documents/tags/index.html'

@app.route('/documents/tags/<field>/<tag>.html')
def document_tag_page(field, tag):
    key = tag if tag else field if field else 'tags'
    tags = json.loads(open('scraping/sovdoc/meta_tags.json', 'r').read())
    data = json.loads(open('scraping/sovdoc/documents.json', 'r').read())

    return render_template('documents/tag.html', data=data, tags=tags,
                           field=field, tag=tag, key=key,  hash=hash)
@app.route('/documents/tags/<field>/index.html')
@app.route('/documents/tags/<field>/')
def document_field_page(field):
    return document_tag_page(field, "")
@app.route('/documents/tags/index.html')
@app.route('/documents/tags/')
def document_tags_page():
    return document_tag_page("", "")


@app.route('/trigger_build')
def trigger_document_build():
    global DEBUG
    DEBUG = False
    for i in freezer.freeze_yield():
        print(i)
    DEBUG = True
    return '200', 200

@freezer.register_generator
def volunteer_page_gen():
    if not STATIC_DATA:
        update_static_data()
    for key in STATIC_DATA:
        yield "/archive/" + key + ".html"
        
@app.route('/archive/<person>.html')
def volunteer_page(person):
    if not STATIC_DATA:
        update_static_data()
    return render_template('archive/volunteer.html',
                           person=person,
                           data=STATIC_DATA[person])
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
                
            os.system('git add archive/data/' + key + '.json')
            
        write_data_to_file(MASTER_FILE, remote_json)
        os.system("git add archive/data/master.json")
        write_data_to_file(MASTER_FILE, local_json)
        
        os.system('git commit -m "' + message + '"')
        push_command = "git push https://{}:{}@github.com/NYC-Volunteers-in-Spanish-Civil-War/NYC-Volunteers-in-Spanish-Civil-War.github.io.git".format(
            request.form.get('username'),
            request.form.get('password'))
        try:
            push_result = subprocess.check_output(push_command, shell=True)
            print(push_result)
            if "Invalid username or password" in push_result:
                return ('', 404)
            return ('', 204)
        except subprocess.CalledProcessError as e:
            return ('', 404)
        return ('', 204)

@app.route('/upload.html', methods=['GET', 'POST'])
def main():
    master_data = get_data_from_file(MASTER_FILE)
    tags = set([tag for key in master_data for tag in master_data[key]['tags']])
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
            "sources": request.form.get('sources'),
            "volunteer_images": json.loads(request.form.get('volunteer_images_hidden')),
            "school_crests": json.loads(request.form.get('school_crests_hidden')),
            "tags": json.loads(request.form.get('tags'))}
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
        update_static_data()
        if redir:
            return ({'redirect': '/?key=' + key}, 200)
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

if __name__ == '__main__':
    #webbrowser.open('http://127.0.0.1:5000?key=', new=1)
    app.run(debug=True)

