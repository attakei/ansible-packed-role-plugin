import os
import unittest
import glob
import shutil
from packed_role import expand_role


here = os.path.dirname(os.path.abspath(__file__))


class CreateRoleDirTests(unittest.TestCase):
    def setUp(self):
        self.target_dir = os.path.join(here, 'temp', 'CreateRoleDirTests')
        shutil.rmtree(self.target_dir, ignore_errors=True)
    
    def _callFUT(self, target):
        from packed_role import create_role_dir
        create_role_dir(target)
    
    def test_it(self):
        self._callFUT(self.target_dir)
        self.assertTrue(os.path.exists(self.target_dir))
        try:
            self._callFUT(self.target_dir)
        except OSError:
            self.fail('Not raised OSError')


class ExpandRoleTests(unittest.TestCase):
    def setUp(self):
        # clean up dest folder
        for item in glob.iglob(os.path.join(here, 'roles', '*')):
            if os.path.isdir(item):
                shutil.rmtree(item) 
    
    def test_create_directory(self):
        test_simple_path = os.path.join(here, 'roles', 'test_simple.yml')
        test_simple_dir = os.path.join(here, 'roles', 'test_simple')

        expand_role(test_simple_path)

        self.assertTrue(os.path.exists(test_simple_dir))
