import os.path
import codecs
import markdown
import re

html_template = u"""<!DOCTYPE html>
<html>
    <head>
        <title>%(title)s</title>
        <link rel="stylesheet" type="text/css" href="/css/styles.css">
    </head>
    <body>
        <div id="wikid-content">
        %(body)s
        </div>
        <div id="wikid-search">
            <input type="text" placeholder="Search...">
            <div class="results"></div>
            <a href="#" class="cancel">X</a>
        </div>
        <script src="/js/jquery.js"></script>
        <script src="/js/search-index.js"></script>
        <script src="/js/search.js"></script>
    </body>
</html>"""

title_re = re.compile('<h1[^>]+>([^<]+)</h1>')

def convert(path, extensions=None):
    """Get the html from a markdown file as a string. 

    `path` - The path to a markdown file.
    `extensions` - can be a list of markdown extensions to use"""

    text = codecs.open(path, 'r', 'utf-8').read() + "\n\n[TOC]"
    
    extension_list = ['extra', 'codehilite(force_linenos=False)', 'headerid', 'toc(title=Table of Contents)', 'wikilinks']
    if extensions:
        extension_list.extend(extensions)

    html = markdown.markdown(text, extensions=extension_list)
    match = title_re.search(html)

    if match:
        title = match.group(1)
    else:
        title = os.path.splitext(os.path.split(path)[-1])[0]
    
    return (html_template % { 'title': title, 'body': html }).encode('utf-8')