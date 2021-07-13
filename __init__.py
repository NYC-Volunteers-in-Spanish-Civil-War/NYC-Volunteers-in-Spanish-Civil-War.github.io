import os
from flask import Flask
from hashlib import md5
from flask_frozen import Freezer

from routes import *


app = Flask(__name__, static_url_path='')

app.config.from_object('config')

freezer.init_app(app)
volunteer_freezer.init_app(app)
misc_freezer.init_app(app)

basedir = os.path.abspath(os.path.dirname(__file__))

ckeditor = CKEditor(app)

app.register_blueprint(routes)

def hash(s):
    return md5(s.encode('utf-8')).hexdigest()

@app.context_processor
def inject_debug():
    return dict(debug=CONF["debug"])

app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)




if __name__ == '__main__':
    app.run(debug=True)

