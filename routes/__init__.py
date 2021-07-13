"""
Coordinates all routing
"""

import os
import subprocess
import json
import urllib
import requests
import jinja2
from flask_ckeditor import CKEditor, upload_success, upload_fail
from hashlib import md5
from flask_frozen import Freezer
from pprint import pprint
from urllib.parse import quote_plus
from flask import Flask, Blueprint, request, redirect, url_for, render_template, jsonify, send_from_directory

from flask import Blueprint, Flask
routes = Blueprint("routes", __name__)

freezer = Freezer(None, with_no_argument_rules=False, log_url_for=False)

volunteer_freezer = Freezer(None, with_no_argument_rules=False, log_url_for=False)

misc_freezer = Freezer(None, with_no_argument_rules=False, log_url_for=False)


from .editor import *
from .volunteers import *
from .build_hooks import *
from .documents import *
from .misc import *

