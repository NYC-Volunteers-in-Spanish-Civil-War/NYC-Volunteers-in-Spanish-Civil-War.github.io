"""
Hooks that trigger freezing various page combinations
"""
from . import *

@routes.route('/trigger_document_build')
def trigger_document_build():
    global DEBUG
    DEBUG = False
    for i in freezer.freeze_yield():
        print(i)
    DEBUG = True
    return '200', 200

@routes.route('/trigger_archive_build')
def trigger_archive_build():
    global DEBUG
    DEBUG = False
    for i in volunteer_freezer.freeze_yield():
        print(i)
    DEBUG = True
    return '200', 200

@routes.route('/trigger_misc_build')
def trigger_misc_build():
    global DEBUG
    DEBUG = False
    for i in misc_freezer.freeze_yield():
        print(i)
    DEBUG = True
    return '200', 200


