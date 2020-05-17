import os
import json
import bisect
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_ckeditor import CKEditor, upload_success, upload_fail

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_HEIGHT'] = 500
ckeditor = CKEditor(app)

@app.route('/', methods=['GET', 'POST'])
def main():
    json_data = {}
    with open('archive/data.json', 'r') as f:
        json_data = json.load(f)
    if request.method == 'POST':
        print request.form.get('student_fname')
        print request.form.get('student_lname')
        print request.form.get('class')
        print request.form.get('volunteer_fname')
        print request.form.get('volunteer_lname')
        out_name = request.form.get('volunteer_lname') + "_" + request.form.get('volunteer_fname') + ".html"
        data = {
            "student_fname": request.form.get('student_fname'),
            "student_lname": request.form.get('student_lname'),
            "class": request.form.get('class'),
            "volunteer_fname": request.form.get('volunteer_fname'),
            "volunteer_lname": request.form.get('volunteer_lname'),
            "data": request.form.get('ckeditor')}
        key = data['volunteer_lname'] + "_" + data['volunteer_fname']
        json_data[key] = data
        with open('archive/data.json', 'w') as f:
            json.dump(json_data, f)
        return render_template("upload.html", data=json_data[key], mega_data=json_data)
    else:
        data = {
            "student_fname": "",
            "student_lname": "",
            "class": "",
            "volunteer_fname": "",
            "volunteer_lname": "",
            "data": ""}
        print "fishy", request.args.get('key')
        if request.args.get('key'):
            data = json_data[request.args.get('key')]
        return render_template("upload.html", data=data, mega_data=json_data)

if __name__ == '__main__':
    app.run(debug=True)
                                 
