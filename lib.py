from os.path import join, splitext, basename, dirname

def filetype(f):
    _, ext = splitext(f)
    if ext == ".jpg":
        return 'image'
    elif ext == ".mp4":
        return 'video'
    else:
        return 'unknown'
