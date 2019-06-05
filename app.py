import os
from os.path import join, splitext, basename, dirname, relpath
from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
from thumbCreator import create_thumbs
from lib import *

app = Flask(__name__)

@app.route("/blog/<name>")
def home(name):
    name = relpath(name)
    path = join('static/pages', name, 'files')
    
    if '..' in name:
        return "invalid path", 403

    if not os.path.exists(path):
        return "No such path", 400

    with open(join('static/pages', name, 'files.yaml')) as yamlf:
        config = yaml.load( yamlf.read() )
        config['best'] = [str(e) for e in config['best']]

    files = sorted(os.listdir( path ))
    thumbfiles = os.listdir( join('static/thumbs', name) )
    
    def build_item(f):
        best = any([(e in f) for e in config['best']])
        def get_thumb_path(f):
            thmb = [e for e in thumbfiles if splitext(f)[0]==splitext(e)[0]]
            return "" if not len(thmb) else join( 'thumbs', name, thmb[0] )

        return {'path':     join('pages', name, 'files', f),
                'thumb':    get_thumb_path(f),
                'filetype': filetype(f),
                'best':     best}    
    
    mainfiles = [build_item(f) for f in files]

    return render_template('index.html',
                           title=config['title'],
                           files=mainfiles)

    

if __name__ == "__main__":
    for f in os.listdir('static/pages'):
        if not os.path.exists(join('static/thumbs', f)):
            dest = join('static/thumbs', f)
            os.makedirs(dest)
            create_thumbs(join('static/pages', f, 'files'), join('static/thumbs', f))
        
        app.run(port = 8888, debug=True, host='0.0.0.0')

    
