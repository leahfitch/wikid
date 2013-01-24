import os
import os.path
import shutil
import re
import codecs
from wikid.convert import convert
from wikid.index import TextCollectingExtension, make_index

link_re = re.compile('(href|src)="([^#^"][^"]*)"')

def adjust_paths(wiki_dir, file_dir, html):
    """Since compiled files can be served from anywhere
    links in the html need to be changed so they are relative."""
    
    link_matches = link_re.findall(html)
    
    for attr,src_path in link_matches:
        dst_path = src_path
        if '.' not in dst_path:
            if dst_path[-1] == '/':
                dst_path = dst_path[:-1]
            dst_path += '.html'
        if dst_path[0] == '/':
            dst_path = dst_path[1:]
        
        full_path = os.path.join(wiki_dir, dst_path)
        rel_path = os.path.relpath(full_path, start=file_dir)
        
        html = html.replace(
            '%s="%s"' % (attr, src_path),
            '%s="%s"' % (attr, rel_path))
    
    return html


def build_wiki(indir, outdir):
    """Process the markdown at `indir` and put it in `outdir`"""
    
    docs = {}
    
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
        
    os.makedirs(outdir)
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    for f in os.listdir(data_dir):
        src = os.path.join(data_dir, f)
        dst = os.path.join(outdir, f)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)
    
    for inbasedir, dirs, files in os.walk(indir):
        outbasedir = os.path.join(outdir, os.path.relpath(inbasedir, indir))
        for d in dirs:
            os.mkdir(os.path.join(outbasedir, d))
        for f in files:
            fname, ext = os.path.splitext(f)
            if ext == '.md':
                inpath = os.path.join(inbasedir, f)
                outpath = os.path.join(outbasedir, fname+'.html')
                md_text_ext = TextCollectingExtension()
                html = adjust_paths(indir, inbasedir, convert(inpath, [md_text_ext]) )
                html_file = codecs.open(outpath, 'w', 'utf-8')
                html_file.write(html.encode('utf-8'))
                html_file.close()
                path = os.path.relpath(outpath, start=outdir)
                for header_id, text in md_text_ext.treeprocessor.text.items():
                    if header_id:
                        doc_path = path + '#' + header_id
                    else:
                        doc_path = path
                    docs[doc_path] = text
            else:
                shutil.copy(os.path.join(inbasedir, f), os.path.join(outbasedir, f))

    index_js = make_index(docs)
    index_file = open(os.path.join(outdir, 'js', 'search-index.js'), 'w')
    index_file.write(index_js)
    index_file.close()