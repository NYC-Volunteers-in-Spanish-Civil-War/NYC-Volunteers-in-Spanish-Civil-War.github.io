import os
import subprocess
import json
import bisect
import urllib
import webbrowser
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_ckeditor import CKEditor, upload_success, upload_fail


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_HEIGHT'] = 500
ckeditor = CKEditor(app)

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form.get('key')
    json_data = {}
    with open('archive/data.json', 'r') as f:
        json_data = json.load(f)
    del json_data[key]
    with open('archive/data.json', 'w') as f:
        json.dump(json_data, f)
    return ('', 204)
@app.route('/delete_image', methods=['POST'])
def delete_image():
    key = request.form.get('key')
    data = request.form.get('data')
    json_data = {}
    with open('archive/data.json', 'r') as f:
        json_data = json.load(f)
    if data in json_data[key]['volunteer_images']:
        json_data[key]['volunteer_images'].remove(data)
    elif data in json_data[key]['school_crests']:
        json_data[key]['school_crests'].remove(data)
    with open('archive/data.json', 'w') as f:
        json.dump(json_data, f)
    return ('', 204)
@app.route('/upload_changes', methods=['POST'])
def upload_changes():
    action = request.form.get('action')
    #Returns if any changes have been made locally that need to be pushed
    if action == 'changes_made':
        url = "https://nyc-volunteers-in-spanish-civil-war.github.io/archive/data.json"
        published_json = json.loads(urllib.urlopen(url).read())
        local_json = {}
        with open('archive/data.json', 'r') as f:
            local_json = json.load(f)
        if local_json != published_json:
            return ('', 204)
        return ('', 404)
    #Attempts to push changes that need to be pushed
    elif action == 'push_changes':
        os.system("git add archive/data.json")
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
@app.route('/', methods=['GET', 'POST'])
def main():
    json_data = {}
    with open('archive/data.json', 'r') as f:
        json_data = json.load(f)
    if request.method == 'POST':
        out_name = request.form.get('volunteer_lname') + "_" + request.form.get('volunteer_fname') + ".html"
        data = {
            "student_fname": request.form.get('student_fname'),
            "student_lname": request.form.get('student_lname'),
            "class": request.form.get('class'),
            "volunteer_fname": request.form.get('volunteer_fname'),
            "volunteer_lname": request.form.get('volunteer_lname'),
            "data": request.form.get('ckeditor'),
            "volunteer_images": json.loads(request.form.get('volunteer_images_hidden')),
            "school_crests": json.loads(request.form.get('school_crests_hidden'))}
        key = data['volunteer_lname'] + "_" + data['volunteer_fname']
        if request.args.get('key') != key:
            del json_data[request.args.get('key')]
        json_data[key] = data
        with open('archive/data.json', 'w') as f:
            json.dump(json_data, f)
        return render_template("upload.html", data=json_data[key], mega_data=json_data, key=key)
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
            data = json_data[request.args.get('key')]
        return render_template("upload.html", data=data, mega_data=json_data, key=request.args.get('key'))

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000?key=', new=1)
    app.run(debug=True)

