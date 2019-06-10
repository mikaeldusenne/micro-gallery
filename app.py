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
    if '..' in name:
        return "invalid path", 403
    
    pagepath  = join('static', 'pages', name)
    pathfiles = join(pagepath, 'files')
    pathyaml  = join(pagepath, 'files.yaml')
    thumbpath = join('static', 'thumbs', name)
    
    if not os.path.exists(pathfiles):
        return "No such path", 400

    with open(pathyaml) as yamlf:
        config = yaml.load( yamlf.read() )

    files = sorted(os.listdir( pathfiles ))
    thumbfiles = os.listdir( thumbpath )
    
    def build_item(f):
        best = any([(str(e) in f) for e in config['best']])
        
        def get_thumb_path(f):
            thmb = [e for e in thumbfiles if splitext(f)[0]==splitext(e)[0]]
            return "" if not len(thmb) else join( 'thumbs', name, thmb[0] )

        return {'path':     join('pages', name, 'files', f),
                'thumb':    get_thumb_path(f),
                'filetype': filetype(f),
                'best':     best}    

    return render_template('index.html',
                           title = config['title'],
                           files = map(build_item, files))

    

if __name__ == "__main__":
    for f in os.listdir('static/pages'):
        if not os.path.exists(join('static/thumbs', f)):
            dest = join('static/thumbs', f)
            os.makedirs(dest)
            create_thumbs(join('static/pages', f, 'files'), join('static/thumbs', f))
        
        app.run(port = 8888, debug=True, host='0.0.0.0')

    
