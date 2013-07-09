import os.path
import codecs
import markdown
import re

html_template = u"""<!DOCTYPE html>
<html>
    <head>
        <title>%(title)s</title>
        <link rel="stylesheet" type="text/css" href="css/styles.css">
    </head>
    <body>
        <div id="wikid-content">
            <aside id="wikid-sidebar">
                <div id="wikid-toc"></div>
                <div id="wikid-search">
                    <input type="text" placeholder="Search...">
                    <div class="results"></div>
                    <a href="#" class="cancel">X</a>
                </div>
            </aside>
            <div id="wikid-body">
            %(body)s
            </div>
        </div>
        <script src="js/jquery.js"></script>
        <script src="js/search-index.js"></script>
        <script src="js/toc.js"></script>
        <script src="js/main.js"></script>
    </body>
</html>"""

title_re = re.compile('<h1[^>]+>([^<]+)</h1>')
src_re = re.compile('(href|src)="([^#^"]+)')

def convert(path, extensions=None, extension_configs=None):
    """Get the html from a markdown file as a string. 

    `path` - The path to a markdown file.
    `extensions` - can be a list of markdown extensions to use"""
    
    text = codecs.open(path, 'r', 'utf-8').read()
    
    extension_list = [
        'extra', 
        'meta', 
        'codehilite(force_linenos=True)', 
        'headerid',
        'wikilinks'
    ]
    if extensions:
        extension_list.extend(extensions)

    html = markdown.markdown(text, extensions=extension_list, extension_configs=extension_configs)
    match = title_re.search(html)
    
    base_url = ''
    if extension_configs and 'wikilinks' in extension_configs:
        for k,v in extension_configs['wikilinks']:
            if k == 'base_url':
                base_url = v

    if match:
        title = match.group(1)
    else:
        title = os.path.splitext(os.path.split(path)[-1])[0]
    
    html = (html_template % { 
        'title': title, 
        'body': html,
        'base_url': base_url }).encode('utf-8')
    
    for attr, path in src_re.findall(html):
        if path.startswith('http://') or path.startswith(base_url):
            continue
        full_path = base_url + path
        html = html.replace('%s="%s"' % (attr, path),
                            '%s="%s"' % (attr, full_path))
    
    return html