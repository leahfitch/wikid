import glob
import os
import os.path
import shutil
import fnmatch
from .toc import TOCIndexer
from .search import SearchIndexer

class Stage(object):
    
    def __init__(self, name):
        self.name = name
    
    def run(self, builder):
        raise NotImplementedError


class CopyAndSwitchStage(Stage):
    
    def __init__(self, name, target_path):
        super(CopyAndSwitchStage, self).__init__(name)
        self.target_path = target_path
        self.copied_project = None
        
    def run(self, builder):
        builder.project = builder.project.copy(self.target_path)
        
        
class CopyDefaultDataStage(Stage):
    
    def run(self, builder):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        for f in os.listdir(data_dir):
            src = os.path.join(data_dir, f)
            dst = builder.project.paths.full(f)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)


class RemoveStage(Stage):
    
    def __init__(self, name, patterns):
        super(RemoveStage, self).__init__(name)
        self.patterns = patterns
        
    def run(self, builder):
        for p in self.patterns:
            p = builder.project.paths.full(p)
            for f in glob.glob(p):
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
                    
                    
class RecursiveRemoveStage(Stage):
    
    def __init__(self, name, patterns):
        super(RecursiveRemoveStage, self).__init__(name)
        self.patterns = patterns
        
    def run(self, builder):
        to_remove = []
        for base, dirs, files in os.walk(builder.project.paths.base):
            paths = [os.path.join(base, f) for f in dirs + files]
            for p in self.patterns:
                to_remove += fnmatch.filter(paths, p)
        for f in to_remove:
            if os.path.isdir(f):
                shutil.rmtree(f)
            else:
                os.remove(f)


class IndexerStage(Stage):
    indexer = None
    path = None
    
    def run(self, builder):
        indexer = self.indexer(builder.data['documents'])
        js_file = builder.project.create_file(self.path)
        js_file.contents(content=indexer.to_js())
                
                
class SearchStage(IndexerStage):
    indexer = SearchIndexer
    path = 'js/index.js'
    
    
class TOCStage(IndexerStage):
    indexer = TOCIndexer
    path = 'js/toc.js'

    
class Builder(object):
    
    def __init__(self, project):
        self.project = project
        self.data = {}
        self.stages = []
        
    def set_stages(self, stages):
        self.stages = stages
        
    def run(self):
        print "Building..."
        if self.project.was_modified():
            for stage in self.stages:
                print "...."+stage.name
                stage.run(self)
    
    def clear(self):
        self.data = {}
