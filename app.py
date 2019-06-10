import os
from os.path import join, splitext, basename, dirname, relpath
from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader, select_autoescape
import yaml
from thumbCreator import create_thumb
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
    files = sorted(os.listdir( pathfiles ))

    if not os.path.exists(pathfiles):
        return "No such path", 400

    with open(pathyaml) as yamlf:
        config = yaml.load( yamlf.read() )

    coverpath = (join(name, config['cover'])
                 if ("cover" in config.keys()
                     and os.path.exists(join('static', name, config['cover'])))
                 else None)
    
    def build_item(f):
        best = any([(str(e) in f) for e in config['best']])
        
        return {'path':     join('pages', name, 'files', f),
                'thumb':    get_thumb_path(f, name),
                'filetype': filetype(f),
                'best':     best}    

    return render_template('index.html',
                           title = config['title'],
                           files = map(build_item, files),
                           cover = coverpath)

def get_thumb_path(f, name):
    thmb = [e for e in os.listdir(join('static/thumbs', name)) if splitext(f)[0]==splitext(e)[0]]
    return None if not len(thmb) else join( 'thumbs', name, thmb[0] )


def init_thumbnails():
    for f in os.listdir('static/pages'):
        pagedir  = join('static/pages', f, 'files')
        thumbdir = join('static/thumbs', f)
        if not os.path.exists(thumbdir):
            os.makedirs(thumbdir)
        for e in os.listdir(pagedir):
            thmbpath = get_thumb_path(e, f)
            if thmbpath is None:
                create_thumb(join(pagedir,e), thumbdir)
    

if __name__ == "__main__":
    init_thumbnails()
    app.run(port = 8888, debug=True, host='0.0.0.0')
