from mimetypes import MimeTypes

def filetype(f):
    m = MimeTypes().guess_type(f)[0]
    return None if m[0] is None else m.split('/')[0]
