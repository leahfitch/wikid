import os
import os.path
import shutil
import re
import json
from wikid.convert import convert
from wikid.index import TextCollectingExtension, make_index

link_re = re.compile('(href|src)="([^#^"][^"]*)"')
    
def walk_wiki_files(path,
    dir_visitor=None,
    non_wiki_visitor=None,
    wiki_visitor=None,
    link_gen=None):
    """Walks a directory looking for wiki files. The first argument is the path to walk,
    the rest are visitors for different things the walk encounters. 
    
    dir_visitor(path)
    `path` -- a path relative to the wiki path
    
    non_wiki_visitor(path)
    `path` -- a path to a file without a .md extension, relative to the wiki path
    
    wiki_visitor(base, name, html, items)
    `base` -- the base path, relative to the wiki path
    `name` -- the name of the markdown file, minus its extension
    `html` -- the html generated from the markdown
    
    Additionally, the caller may wish to pass a `link_gen`. This generates an internal link
    between wiki files. It should look like this:
    
    link_gen(base, name)
    `base` -- the base path relative to the wiki path
    `name` -- the name of the wiki file sans extension
    `id` -- the id of an anchor on the wiki page (may be None)
    
    Returns a list of items collected by `TextCollectingExtension`
    
    """
    items = []
    for base, dirs, files in os.walk(path):
        if '.page-order' in files:
            order = {}
            for i, p in enumerate(open(os.path.join(base, '.page-order')).read().split()):
                order[p.lower() + '.md'] = i
            files.sort(cmp=lambda a,b: cmp(order.get(a.lower(), 10000), order.get(b.lower(), 10000)))
        if dir_visitor:
            for d in dirs:
                dir_visitor(
                    os.path.relpath(os.path.join(base, d), start=path)
                )
        for f in files:
            relbase = os.path.relpath(base, start=path)
            name, ext = os.path.splitext(f)
            if ext == '.md':
                md_text_ext = TextCollectingExtension()
                if link_gen:
                    base_url = link_gen(relbase, '', None)
                else:
                    base_url = os.path.relpath(path, start=base)
                html = convert(os.path.join(base, f), 
                                extensions=[md_text_ext], 
                                extension_configs={'wikilinks': [
                                    ('base_url', base_url+'/'),
                                    ('end_url', '.html')
                                ]})
                for item in md_text_ext.treeprocessor.items:
                    if link_gen:
                        item['path'] = link_gen(relbase, name, item.get('id'))
                    else:
                        item_file_path = os.path.relpath(os.path.join(base, name+'.html'), start=path)
                        item['path'] = item_file_path + ('#'+item['id'] if 'id' in item else '')
                    items.append(item)
                if wiki_visitor:
                    wiki_visitor(relbase, name, html)
            elif non_wiki_visitor:
                non_wiki_visitor(os.path.join(relbase, f))
    return items
    
    
def index_from_items(items):
    return make_index(items)
    
    
def toc_from_items(items):
    headers = []
    for item in items:
        if item.get('id'):
            headers.append({
                'path': item['path'],
                'text': item['title'],
                'depth': item['depth']
            })
    return 'var wikid_toc = ' + json.dumps(headers)
    

class Builder(object):
    
    def __init__(self, indir, outdir):
        self.indir = indir
        self.outdir = outdir
        
    def build(self):
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir)
        os.makedirs(self.outdir)
        
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        for f in os.listdir(data_dir):
            src = os.path.join(data_dir, f)
            dst = os.path.join(self.outdir, f)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)
        
        items = walk_wiki_files(
            self.indir,
            self.dir_visitor,
            self.non_wiki_visitor,
            self.wiki_visitor
        )
        open(os.path.join(self.outdir, 'js', 'toc.js'), 'w').write(toc_from_items(items))
        open(os.path.join(self.outdir, 'js', 'search-index.js'), 'w').write(index_from_items(items))
    
    def dir_visitor(self, path):
        os.mkdir(os.path.join(self.outdir, path))
        
    def non_wiki_visitor(self, path):
        shutil.copy(os.path.join(self.indir, path), 
                    os.path.join(self.outdir, path))
        
    def wiki_visitor(self, base, name, html):
        #html = adjust_paths(self.indir, os.path.join(self.indir, base), html)
        open(os.path.join(self.outdir, base, name+'.html'), 'w').write(html)
        

def build_wiki(indir, outdir):
    builder = Builder(indir, outdir)
    builder.build()
    