"""
Coordinates all routing
"""

import os
import subprocess
import json
import urllib
import requests
import datetime
import jinja2
from flask_ckeditor import CKEditor, upload_success, upload_fail
from hashlib import md5
from flask_frozen import Freezer
from pprint import pprint
from urllib.parse import quote_plus
from flask import Flask, Blueprint, request, redirect, url_for, render_template, jsonify, send_from_directory

from flask import Blueprint, Flask
routes = Blueprint("routes", __name__)

CONF = {"debug": True}

freezer = Freezer(None, with_no_argument_rules=False, log_url_for=False)

volunteer_freezer = Freezer(None, with_no_argument_rules=False, log_url_for=False)

misc_freezer = Freezer(None, with_no_argument_rules=False, log_url_for=False)

MASTER_FILE = 'archive/data/master.json'

def get_data_from_file(filename, url=False):
    """ Returns the json data in a given file. """
    if not url:
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        response = urllib.request.urlopen(filename)
        return json.loads(response.read())
def write_data_to_file(filename, data):
    """ Writes data to a json file. """
    with open(filename, 'w+') as f:
        json.dump(data, f, indent=4, sort_keys=True)


from .misc import *
from .build_hooks import *
from .editor import *
from .volunteers import *
from .documents import *


