import os.path
import re
import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from .build import (
    Builder, Stage, CopyAndSwitchStage, 
    CopyDefaultDataStage, RecursiveRemoveStage,
    SearchStage, TOCStage
)
from .files import MarkdownFile, create as create_file
from .templates import html_template


class RootGrabbingTreeprocessor(Treeprocessor):
    
    def __init__(self, *args, **kwargs):
        Treeprocessor.__init__(self, *args, **kwargs)
        self.root = None
        
    def run(self, root):
        self.root = root


class RootGrabbingExtension(Extension):

    def __init__(self, *args, **kwargs):
        Extension.__init__(self, *args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.treeprocessor = RootGrabbingTreeprocessor(md)
        md.treeprocessors.add('textcollector', self.treeprocessor, '<attr_list')
        
        
class MarkdownProcessStage(Stage):
    title_re = re.compile('<h1[^>]+>([^<]+)</h1>')
    protocol_re = re.compile('[^:]+:')
    src_re = re.compile('(href|src)="([^#^"]+)')
    
    def run(self, builder):
        builder.data['documents'] = []
        for f in builder.project.walk():
            if isinstance(f, (MarkdownFile,)):
                self.process_file(builder, f)
    
    def process_file(self, builder, f):
        base, ext = os.path.splitext(f.path())
        base_path = builder.project.paths.debase(
            os.path.dirname(f.path())
        )
        html, root = self.convert(f)
        builder.data['documents'].append({
            'root': root,
            'path': builder.project.paths.debase(f.path())
        })
        html = self.fix_links(html, base_path, builder.project.paths)
        html_file = create_file(base + '.html')
        html_file.contents(content=html)
        
    def convert(self, f):
        root_ext = RootGrabbingExtension()
        html = markdown.markdown(f.contents(), extensions=[
        'extra',
            'meta', 
            'codehilite(force_linenos=True)', 
            'headerid',
            root_ext
        ])
        
        match = self.title_re.search(html)
        if match:
            title = match.group(1)
        else:
            title = os.path.splitext(os.path.split(f.path())[-1])[0]
        
        return html_template % {
            'title': title,
            'body': html
        }, root_ext.treeprocessor.root
        
    def fix_links(self, html, base_path, path_resolver):
        for attr, path in self.src_re.findall(html):
            if self.protocol_re.match(path):
                continue
            new_path = path_resolver.relative(base_path, path)
            html = html.replace('%s="%s"' % (attr, path),
                                '%s="%s"' % (attr, new_path))
        return html


class MarkdownBuilder(Builder):
    
    def __init__(self, project, target_path):
        super(MarkdownBuilder, self).__init__(project)
        self.stages = [
            CopyAndSwitchStage('Copy source', target_path),
            CopyDefaultDataStage('Copy base theme files'),
            MarkdownProcessStage('Process markdown files'),
            TOCStage('Build table of contents'),
            SearchStage('Build search index'),
            RecursiveRemoveStage('Remove markdown files', ['*.md'])
        ]