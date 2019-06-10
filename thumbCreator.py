import cv2
from os.path import join, splitext, basename, dirname
import os
import numpy as np
from lib import *
import math
import imageio
from PIL import Image
import contextlib

thumbsize = (200, 200)
video_n_frames = 10

def with_np_as_pil(f):
    '''
    convert numpy array to Pillow image to apply f, 
    and then back to array
    '''
    def g(img):
        return np.array( f( Image.fromarray(img) ))
    return g


def get_thumbnailed_image(image, size=thumbsize):
    '''
    create a square image, letterboxed to the desired size
    '''
    image = image.copy()
    image.thumbnail(size)
    background = Image.new('RGB', size, (0, 0, 0))
    background.paste(image,
                     (int((size[0] - image.size[0]) / 2),
                      int((size[1] - image.size[1]) / 2)))
    return background


def get_frames(vidpath, which = np.linspace(0, 1, video_n_frames)):
    '''
    return frames from a video as a list of np.array.
    @param vidpath: the path to the video
    @param which: list of values between 0 and 1 representing the frames to get as a
                  % of the total number of frames
    '''
    cap = cv2.VideoCapture(vidpath)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    def get(pct):
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(length-1, math.floor(pct * length)))
        image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
        return with_np_as_pil(get_thumbnailed_image)(image)
    
    return [get(p) for p in which]


def create_thumb(f, dest):
    print('creating thumbnail for', f)
    if filetype(f) == 'video':
        newname = splitext(basename(f))[0] + ".gif"
        images = get_frames(f)
        imageio.mimsave(join(dest, newname), images, duration=0.8)
    elif filetype(f) == 'image':
        (get_thumbnailed_image( Image.open(f) )
         .save(join(dest, basename(f))))
    else:
        print('ERROR: unknown filetype for', f)

