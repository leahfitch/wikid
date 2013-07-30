import unittest
import os.path
import shutil
from wikid.project import Project
from wikid import build, buildmd


class FooStage(build.Stage):
    
    def __init__(self, project, name):
        super(FooStage, self).__init__(name)
        self.project = project
        self.ran = False
    
    def run(self, builder):
        assert self.project == builder.project
        self.ran = True
        builder.data[self.name] = 1
        

class TestBuilder(unittest.TestCase):
    
    def setUp(self):
        self.project = Project(
            os.path.join( os.path.abspath( os.path.dirname(__file__) ), 'example' + os.sep )
        )
        self.dist_dir = os.path.join( os.path.abspath( os.path.dirname(__file__) ), 'example-dist' + os.sep )
        
    def tearDown(self):
        self.project = None
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)
              
    def test_abstract_build(self):
        stages = [FooStage(self.project, 'a'), FooStage(self.project, 'b')]
        self.assert_(not stages[0].ran)
        builder = build.Builder(self.project)
        builder.set_stages(stages)
        builder.run()
        self.assert_(stages[0].ran)
        self.assert_(stages[1].ran)
        self.assertEquals(builder.data['a'], 1)
        self.assertEquals(builder.data['b'], 1)
        
    def test_cached_build(self):
        stage = FooStage(self.project, 'foo')
        self.assert_(not stage.ran)
        builder = build.Builder(self.project)
        builder.set_stages([stage])
        builder.run()
        self.assert_(stage.ran)
        stage.ran = False
        builder.run()
        self.assert_(not stage.ran)
        
    def test_copy_stage(self):
        self.assert_(not os.path.exists(self.dist_dir))
        copy_stage = build.CopyAndSwitchStage('copy', self.dist_dir)
        builder = build.Builder(self.project)
        builder.set_stages([copy_stage])
        builder.run()
        self.assert_(os.path.exists(self.dist_dir))
        self.assertListEqual(os.listdir(self.dist_dir), ['index.md', 'inner'])
        self.assertEquals(builder.project.paths.base, self.dist_dir)
        
    def test_copy_data_stage(self):
        builder = build.Builder(self.project)
        builder.set_stages([
            build.CopyAndSwitchStage('copy source', self.dist_dir),
            build.CopyDefaultDataStage('copy data')
        ])
        builder.run()
        self.assert_(os.path.exists(self.dist_dir))
        self.assert_(os.path.exists(os.path.join(self.dist_dir, 'js')))
        self.assert_(os.path.exists(os.path.join(self.dist_dir, 'js/jquery.js')))
        self.assert_(os.path.exists(os.path.join(self.dist_dir, 'js/main.js')))
        self.assert_(os.path.exists(os.path.join(self.dist_dir, 'js')))
        self.assert_(os.path.exists(os.path.join(self.dist_dir, 'css')))
        self.assert_(os.path.exists(os.path.join(self.dist_dir, 'css/styles.css')))
        self.assertEquals(builder.project.paths.base, self.dist_dir)
        
    def test_remove_stage(self):
        self.assert_(os.path.exists(self.project.paths.full('index.md')))
        builder = build.Builder(self.project)
        builder.set_stages([
            build.CopyAndSwitchStage('copy', self.dist_dir),
            build.RemoveStage('remove_index_file', ['index.md'])
        ])
        builder.run()
        self.assert_(os.path.exists(self.dist_dir))
        self.assert_(not os.path.exists(
            os.path.join(self.dist_dir, 'index.md')
        ))
        
    def test_recursive_remove_stage(self):
        self.assert_(os.path.exists(self.project.paths.full('index.md')))
        self.assert_(os.path.exists(self.project.paths.full('inner')))
        self.assert_(os.path.exists(self.project.paths.full('inner/foo.md')))
        
        builder = build.Builder(self.project)
        builder.set_stages([
            build.CopyAndSwitchStage('copy', self.dist_dir),
            build.RecursiveRemoveStage('remove_markdown', ['*.md'])
        ])
        builder.run()
        self.assert_(os.path.exists(self.dist_dir))
        self.assert_(not os.path.exists(
            os.path.join(self.dist_dir, 'index.md')
        ))
        self.assert_(not os.path.exists(
            os.path.join(self.dist_dir, 'inner/foo.md')
        ))
      
    def test_markdown_builder(self):
        builder = buildmd.MarkdownBuilder(self.project, self.dist_dir)
        builder.run()
        self.assert_(os.path.exists( os.path.join(self.dist_dir, 'index.html') ))
        self.assert_(os.path.exists( os.path.join(self.dist_dir, 'inner/foo.html') ))
        self.assert_(not os.path.exists( os.path.join(self.dist_dir, 'index.md') ))
        self.assert_(not os.path.exists( os.path.join(self.dist_dir, 'inner/foo.md') ))
        self.assert_(os.path.exists( os.path.join(self.dist_dir, 'js/toc.js') ))
        self.assert_(os.path.exists( os.path.join(self.dist_dir, 'js/index.js') ))
        