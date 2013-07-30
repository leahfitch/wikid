import unittest
import os
from wikid import files


class FilesTests(unittest.TestCase):
    
    def tearDown(self):
        try:
            os.remove('foo.txt')
        except OSError:
            pass
    
    def test_types(self):
        f = files.create('foo.txt')
        self.assert_(not f.exists())
        self.assertEquals(f.mimetype(), 'text/plain')
        self.assertEquals(f.contents(), '')
        
        f = files.create('foo.js')
        self.assertEquals(f.mimetype(), 'application/javascript')
        self.assertIsInstance(f, files.JavaScriptFile)
        
        f = files.create('foo.css')
        self.assertEquals(f.mimetype(), 'text/css')
        self.assertIsInstance(f, files.CSSFile)
        
        f = files.create('foo.md')
        self.assertEquals(f.mimetype(), 'text/x-markdown')
        self.assertIsInstance(f, files.MarkdownFile)
        
        
    def test_read_write(self):
        f = files.create('foo.txt')
        self.assert_(not f.exists())
        self.assertEquals(f.contents(), '')
        
        f.contents('foo bar baz')
        self.assert_(f.exists())
        g = files.create('foo.txt')
        self.assertEquals(g.contents(), 'foo bar baz')
        
        f.remove()
        self.assert_(not g.exists())
        self.assert_(not f.exists())