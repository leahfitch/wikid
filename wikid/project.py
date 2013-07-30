import os
import os.path
import shutil
from paths import PathResolver
from files import create as create_file


class Project(object):
    
    def __init__(self, path):
        self.paths = PathResolver(path)
        self.last_modified = 0
        
    def was_modified(self):
        modified = 0
        for root, dirs, files in os.walk(self.paths.base):
            for f in files:
                stat = os.stat(os.path.join(root, f))
                modified = max(self.last_modified, stat.st_mtime)
        was_modified = self.last_modified < modified
        self.last_modified = modified
        return was_modified
        
    def copy(self, target_path, overwrite=True):
        if overwrite and os.path.exists(target_path):
            shutil.rmtree(target_path)
        shutil.copytree(self.paths.base, target_path)
        return Project(target_path)
        
    def walk(self):
        for base, dirs, files in os.walk(self.paths.base):
            for f in files:
                yield create_file(os.path.join(base, f))
                
    def create_file(self, path):
        return create_file(self.paths.full(path))