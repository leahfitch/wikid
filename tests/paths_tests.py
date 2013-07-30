import unittest
from wikid import paths

class TestPaths(unittest.TestCase):
    
    def test_full(self):
        resolver = paths.PathResolver('/foo/bar')
        self.assertEqual(
            resolver.full('baz/qux.html'),
            '/foo/bar/baz/qux.html'
        )
        self.assertEqual(
            resolver.full('baz', 'qux.html'),
            '/foo/bar/baz/qux.html'
        )
        self.assertEqual(
            resolver.full('/baz/qux.html'),
            '/foo/bar/baz/qux.html'
        )
        self.assertEqual(
            resolver.full('baz/qux.html'),
            '/foo/bar/baz/qux.html'
        )
        self.assertEqual(
            resolver.full('../goo'),
            '/foo/goo'
        )
        
    def test_debase(self):
        resolver = paths.PathResolver('/foo/bar')
        self.assertEqual(
            resolver.debase('/foo/bar/baz/bing'),
            'baz/bing'
        )
        self.assertEqual(
            resolver.debase('/foo/bar', '/baz', 'bing'),
            'baz/bing'
        )
        self.assertRaises(ValueError, resolver.debase, '/baz/bing/foo.html')
        self.assertRaises(ValueError, resolver.debase, 'baz/bing/foo.html')
        self.assertRaises(ValueError, resolver.debase, '/foo/barbaz/bing')
        
        resolver = paths.PathResolver('foo/bar')
        self.assertEqual(
            resolver.debase('foo/bar/baz/bing'),
            'baz/bing'
        )
        self.assertRaises(ValueError, resolver.debase, '/foo/bar/baz/bing/foo.html')
        
        
    def test_rebase(self):
        resolver = paths.PathResolver('/foo/bar')
        self.assertEqual(
            resolver.rebase('/ron/perlman', '/foo/bar/baz/bing'),
            '/ron/perlman/baz/bing'
        )
        self.assertEqual(
            resolver.rebase('/ron/perlman', '/foo/', 'bar', '/baz/bing'),
            '/ron/perlman/baz/bing'
        )
        self.assertRaises(ValueError, resolver.rebase, '/ron/perlman', '/baz/bing/foo.html')
        
        
    def test_relative(self):
        resolver = paths.PathResolver('/foo/bar')
        base = 'baz'
        path = 'bing/boo'
        relpath = resolver.relative(base, path)
        self.assertEquals(relpath, '../bing/boo')
        
        base = '/baz/bonk'
        path = '/flub/floob'
        relpath = resolver.relative(base, path)
        self.assertEquals(relpath, '../../flub/floob')