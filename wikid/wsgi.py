import os
import os.path
import mimetypes
from wikid import build
from wikid.convert import convert


class WikidNotFoundError(Exception):
    pass


class WikidApp(object):
    
    def __init__(self, path, port):
        self.path = path
        self.port = port
        self.paths = [
            path,
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        ]
        self.handlers = {
            'js/search-index.js': self.handle_search_index_request,
            'js/toc.js': self.handle_toc_request
        }
        self.last_modified = 0
        self.search_index = None
        self.toc = None
        
        
    def __call__(self, environ, start_response):
        
        path = environ['PATH_INFO']
        
        if path[0] == os.sep:
            path = path[1:]
        
        if not path:
            path = 'index'
        
        try:
            result, content_type = self.handle(path)
        except WikidNotFoundError, e:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return ["I couldn't find anything at this location."]

        start_response('200 OK', [('Content-Type', content_type)])
        return [result]
        
        
    def handle(self, path):
        if path[-1] == '/':
            path = path[:-1]
            
        full_path = self.find_matching_path(path)
        
        if not full_path:
            full_path = self.find_matching_path(path + '.md')
            if not full_path:
                handler = self.handlers.get(path)
                if handler:
                    return handler()
                else:
                    raise WikidNotFoundError()
        
        if os.path.splitext(full_path)[1] == '.md':
            result = convert(full_path, 
                            extension_configs={'wikilinks':[
                                ('base_url', 'http://localhost:%d/' % self.port)
                            ]})
            content_type = 'text/html; charset=utf-8'
        else:
            content_type, _ = mimetypes.guess_type(full_path)
            result = open(full_path, 'rb').read()
        
        return result, content_type
        
        
    def find_matching_path(self, path):
        for base_path in self.paths:
            new_path = os.path.join(base_path, path)
            if os.path.exists(new_path):
                return new_path


    def handle_search_index_request(self):
        self.update_index()
        return self.search_index, 'text/javascript'
        
        
    def handle_toc_request(self):
        self.update_index()
        return self.toc, 'text/javascript'


    def update_index(self):
        if not self.was_modified():
            return
        
        print "Updating index ...",
        
        def link_gen(base, name, id=None):
            if base.startswith('./'):
                base = base[2:]
            elif base == '.':
                base = ''
            path = '/'
            if name != 'index':
                path += os.path.join(base, name)
            if id:
                path += '#'+id
            return path
                
        
        items = build.walk_wiki_files(self.path, link_gen=link_gen)
        self.search_index = build.index_from_items(items)
        self.toc = build.toc_from_items(items)
        
        print 'done.'


    def was_modified(self):
        modified = 0
        for root, dirs, files in os.walk(self.path):
            for f in files:
                stat = os.stat(os.path.join(root, f))
                modified = max(self.last_modified, stat.st_mtime)
        was_modified = self.last_modified < modified
        self.last_modified = modified
        return was_modified