import mimetypes
import os, os.path
import codecs

__all__ = ['File', 'JavaScriptFile', 'CSSFile', 'MarkdownFile', 'HTMLFile', 'create']

class File(object):
    default_encoding = None
    
    def __init__(self, path, mimetype="text/plain"):
        self._path = path
        self._mimetype = mimetype
        
    def path(self):
        return self._path
        
    def exists(self):
        return os.path.exists(self._path)
        
    def mimetype(self):
        return self._mimetype
        
    def contents(self, content=None, encoding=None):
        if content is not None:
            return self.write(content, encoding=encoding)
        else:
            return self.read(encoding=encoding)
        
    def write(self, content='', encoding=None):
        encoding = encoding if encoding else self.default_encoding
        if encoding:
            fp = codecs.open(self._path, 'w', encoding=encoding)
        else:
            fp = open(self._path, 'w')
        fp.write(content)
        fp.close()
        
    def read(self, encoding=None):
        if self.exists():
            encoding = encoding if encoding else self.default_encoding
            if encoding:
                return codecs.open(self._path, 'r', encoding=encoding).read()
            else:
                return open(self._path, 'rb').read().decode()
        else:
            return u''
            
    def remove(self):
        if self.exists():
            os.remove(self._path)
    
    
class JavaScriptFile(File):
    default_encoding = 'utf-8'
    
class CSSFile(File):
    default_encoding = 'utf-8'
    
class HTMLFile(File):
    default_encoding = 'utf-8'

class MarkdownFile(File):
    default_encoding = 'utf-8'
    

extensions = {
    '.md': 'text/x-markdown'
}

classes = {
    'application/javascript': JavaScriptFile,
    'text/css': CSSFile,
    'text/x-markdown': MarkdownFile,
    'text/html': HTMLFile
}

def get_type(path):
    mimetype, encoding = mimetypes.guess_type(path)
    if mimetype is None:
        base, ext = os.path.splitext(path)
        mimetype = extensions.get(ext, 'text/plain')
    return mimetype

def create(path):
    mimetype = get_type(path)
    cls = classes.get(mimetype, File)
    return cls(path, mimetype=mimetype)