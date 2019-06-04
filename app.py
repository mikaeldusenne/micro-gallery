import os
from os.path import join, splitext, basename, dirname
from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
from thumbCreator import create_thumbs
from lib import *

app = Flask(__name__)
# env = Environment(
#     loader=PackageLoader('yourapplication', 'templates'),
#     autoescape=select_autoescape(['html', 'xml'])
# )


    
    
# create a new route at the root of the website
@app.route("/blog/<name>")
def home(name):
    assert '..' not in name
    path = join('static/pages', name, 'files')
    if not os.path.exists(path):
        return "No such path", 400

    with open(join('static/pages', name, 'files.yaml')) as yamlf:
        config = yaml.load( yamlf.read() )
        config['best'] = [str(e) for e in config['best']]

    files = sorted(os.listdir( path ))
    
    def mkurl(fname):
        return join(name, 'files', fname)
    
    def build_item(f):
        ft = filetype(f)
        best = any([(e in f) for e in config['best']])
        def get_thumb(f):
            ext = ".gif" if filetype(f) == "video" else ".jpg"
            return join( 'thumbs', name, splitext(f)[0] + ext )
        # thmb = [join('thumbs/', name, e) for e in files if splitext(f)[0] in e and 'thumb' in e][0]
        thmb = get_thumb(f)
        _class = ' '.join(["element",
                           "best" if best else "",
                           "video" if ft == "video" else "image"
                           ])
        return {'name': f,
                'path':  mkurl(f),
                'thumb': thmb,
                'filetype': ft,
                'best': best,
                'class': _class}

    
    
    mainfiles = [build_item(f) for f in files if 'thumb' not in f]

    return render_template('index.html',
                           title=name,
                           files=mainfiles)

    

if __name__ == "__main__":
    for f in os.listdir('static/pages'):
        if not os.path.exists(join('static/thumbs', f)):
            dest = join('static/thumbs', f)
            os.makedirs(dest)
            create_thumbs(join('static/pages', f), join('static/thumbs', f))
        
    app.run(port = 8888, debug=True, host='0.0.0.0')

    
