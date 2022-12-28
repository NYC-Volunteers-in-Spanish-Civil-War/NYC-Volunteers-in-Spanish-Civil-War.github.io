"""
Handles generating pages for volunteer biographies
"""
from . import *


@routes.route('/archive/data/<path:path>')
def send_archive_data(path):
    return send_from_directory('archive/data', path)


@freezer.register_generator
@volunteer_freezer.register_generator
def volunteer_page_gen():
    CONF["debug"] = False
    if not STATIC_DATA:
        update_static_data()
    for key in STATIC_DATA:
        yield "/archive/" + key + ".html"
    yield "/archive/index.html"
    yield "/sitemap.xml"
    CONF["debug"] = True
        
@routes.route('/archive/<person>.html')
def volunteer_page(person):
    if not STATIC_DATA:
        update_static_data()
    return render_template('archive/volunteer.html',
                           person=person,
                           data=STATIC_DATA[person])

