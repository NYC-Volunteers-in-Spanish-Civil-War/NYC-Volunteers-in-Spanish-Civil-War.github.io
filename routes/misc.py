"""
Handles rendering simpler pages that don't require pulling data. Some useful helper functions
"""
from . import *

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



@freezer.register_generator
@misc_freezer.register_generator
def misc_gen():
    return ['/index.html', '/context.html', '/archive/index.html', '/sources.html', '/map.html', '/contact.html']


@routes.route('/')
@routes.route('/index.html')
@routes.route('/context.html')
@routes.route('/archive/')
@routes.route('/archive/index.html')
@routes.route('/sources.html')
@routes.route('/map.html')
@routes.route('/contact.html')
def misc():
    print((request.path[1::] + ("index.html" if request.path[-1] == "/" else ""))) 
    return render_template(request.path[1::] + ("index.html" if request.path[-1] == "/" else ""))


@routes.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@routes.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@routes.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)
@routes.route('/favicon.ico')
def send_favicon():
    return send_from_directory('.', "favicon.ico")

@freezer.register_generator
def site_map():
    yield '/sitemap.xml'

@routes.route('/sitemap.xml')
def site_map():
    master_data = get_data_from_file(MASTER_FILE)
    documents = get_data_from_file('documents/documents.json')
    tags = get_data_from_file('documents/meta_tags.json')
    date = datetime.date.today()
    return render_template('sitemap.xml', master_data=master_data, documents=documents, tags=tags, date=date)


