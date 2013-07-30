import os
import os.path

__all__ = ['PathResolver']

class PathResolver(object):
    """Various path transformations based around a single base path."""
    
    def __init__(self, base):
        if len(base) == 0:
            raise ValueError, "The base path must be a string with a length greater than 0."
        if base[-1] != os.path.sep:
            base += os.path.sep
        self.base = base
        
    def full(self, *parts):
        """Create a "full" path by prepending the base path (which may not be absolute)."""
        parts = self._deabsolute(parts)
        return os.path.normpath(
            os.path.join(self.base, *parts)
        )
        
    def debase(self, *parts):
        """Remove the base path from the begining of the given path. 
        Raises `ValueError` if the path doesn't start with the base path."""
        if len(parts) > 0:
            parts = [parts[0]] + self._deabsolute(parts[1:])
        path = os.path.normpath(os.path.join(*parts))
        
        if not path.startswith(self.base):
            if self.base.startswith(path):
                return ''
            raise ValueError, "can't remove '%s' from '%s'" % (self.base, path)
        return path[len(self.base):]
            
            
    def rebase(self, new_base, *parts):
        """Replace the base portion of the path with a new base."""
        return os.path.normpath(
            os.path.join(
                new_base, 
                self._deabsolute(
                    [self.debase(*parts)]
                )[0]
            )
        )
        
    def relative(self, base, path):
        """Figures out a relative path to `path` from `base`. 
        Both arguments are assumed to be relative to the resolver's base."""
        _base = self.full(base)
        _path = self.full(path)
        return os.path.relpath(_path, _base)
        
    def _deabsolute(self, path_parts):
        return [p[1:] if p[0] == os.path.sep else p for p in path_parts if len(p) > 0]