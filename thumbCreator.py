import cv2
from os.path import join, splitext, basename, dirname
import os
import numpy as np
from lib import *
import math
import imageio
from PIL import Image

thumbsize = (200, 200)

def piltosquareletterbox(image, size=thumbsize):
    background = Image.new('RGBA', size, (0, 0, 0, 0))
    background.paste(image,
                     (int((size[0] - image.size[0]) / 2),
                      int((size[1] - image.size[1]) / 2)))
    return background

def get_thumbnailed_image(image):
    convert = type(image) == np.ndarray
    if convert:
        image = Image.fromarray(image)
    image.thumbnail(thumbsize)
    image = piltosquareletterbox(image)
    if convert:
        image = np.array(image)
    return image

def get_frames(vid):
    cap = cv2.VideoCapture(vid)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    def get(pct):
        cap.set(cv2.CAP_PROP_POS_FRAMES, math.floor(pct * length))
        image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        # image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # image.thumbnail(thumbsize)
        return get_thumbnailed_image(image)
    
    # images = [get(p) for p in [0,0.25,0.5,0.75,0.99]] #  np.linspace(0,1,10)*0.99]
    images = [get(p) for p in np.linspace(0,1,10)*0.99]
    return images

def get_image(img):
    return get_thumbnailed_image( Image.open(img) )

def create_thumbs(src, dest):
    print('create_thumbs for ', src)
    def create_thumb(f):
        print('creating thumbnail for', f)
        if filetype(f) == 'video':
            newname = splitext(f)[0] + ".gif"
            images = get_frames(join(src, f))
            imageio.mimsave(join(dest, newname), images, duration=0.8)
        else:
            get_image(join(src, f)).convert('RGB').save(join(dest, f))
    files = os.listdir(src)
    for f in files:
        create_thumb(f)

        
    
if __name__ == '__main__':
    create_thumbs('static/pages/etretat/files', 'static/thumbs/etretat/')
