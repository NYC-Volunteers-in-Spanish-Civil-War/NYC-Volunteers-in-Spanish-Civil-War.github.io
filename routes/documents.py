"""
Handles freezing the sovdoc pages.
"""
from . import *

@routes.route('/documents/<filename>.json')
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

@routes.route('/documents/')
@routes.route('/documents/<id>.html')
def document_page(id=""):
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


@routes.route('/documents/tags/<field>/<tag>.html')
def document_tag_page(field, tag):
    key = tag if tag else field if field else 'tags'
    tags = json.loads(open('scraping/sovdoc/meta_tags.json', 'r').read())
    data = json.loads(open('scraping/sovdoc/documents.json', 'r').read())

    return render_template('documents/tag.html', data=data, tags=tags,
                           field=field, tag=tag, key=key,  hash=hash)

@routes.route('/documents/tags/<field>/index.html')
@routes.route('/documents/tags/<field>/')
def document_field_page(field):
    return document_tag_page(field, "")

@routes.route('/documents/tags/index.html')
@routes.route('/documents/tags/')
def document_tags_page():
    return document_tag_page("", "")
