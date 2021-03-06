import os
import unittest
import glob
import shutil
from packed_role import expand_role, CallbackModule


here = os.path.dirname(os.path.abspath(__file__))


class CreateRoleDirTests(unittest.TestCase):
    def setUp(self):
        self.target_dir = os.path.join(here, 'temp', 'CreateRoleDirTests')
        shutil.rmtree(self.target_dir, ignore_errors=True)
    
    def _callFUT(self, target):
        from packed_role import mkdir_if_not_exists
        mkdir_if_not_exists(target)
    
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
            if not os.path.isdir(item):
                continue
            shutil.rmtree(item) 
    
    def test_create_directory(self):
        test_simple_path = os.path.join(here, 'roles', 'simple.yml')
        test_simple_dir = os.path.join(here, 'roles', 'simple')

        expand_role(test_simple_path)

        self.assertTrue(os.path.exists(test_simple_dir))
        self.assertTrue(os.path.exists(os.path.join(test_simple_dir, 'tasks', 'main.yml')))
        self.assertTrue(os.path.exists(os.path.join(test_simple_dir, 'vars', 'main.yml')))

        try:
            expand_role(test_simple_path)
        except Exception as err:
            self.fail('error occurred' + err.message)

    def test_not_create_needless_directory(self):
        test_simple_path = os.path.join(here, 'roles', 'with_comment.yml')
        test_simple_dir = os.path.join(here, 'roles', 'with_comment')

        expand_role(test_simple_path)

        self.assertTrue(os.path.exists(test_simple_dir))
        self.assertFalse(os.path.exists(os.path.join(test_simple_dir, 'comments')))


class OutputFilesFromPackedRolesTests(unittest.TestCase):
    def setUp(self):
        # clean up dest folder
        for item in glob.iglob(os.path.join(here, 'roles', '*')):
            if not os.path.isdir(item):
                continue
            shutil.rmtree(item) 
    
    def test_create_directory(self):
        test_simple_path = os.path.join(here, 'roles', 'with_files.yml')
        test_simple_dir = os.path.join(here, 'roles', 'with_files/files')
        test_simple_file = os.path.join(here, 'roles', 'with_files/files/testfile.txt')

        expand_role(test_simple_path)

        self.assertTrue(os.path.exists(test_simple_dir))
        self.assertTrue(os.path.exists(test_simple_file))
        with open(test_simple_file) as fp:
            content = \
                'Hello world.\n' \
                'Test'
            self.assertEqual(fp.read(), content)

    def test_create_templates_directory_and_file(self):
        test_simple_path = os.path.join(here, 'roles', 'with_templates.yml')
        test_simple_dir = os.path.join(here, 'roles', 'with_templates/templates')
        test_simple_file = os.path.join(here, 'roles', 'with_templates/templates/testfile.txt.j2')

        expand_role(test_simple_path)

        self.assertTrue(os.path.exists(test_simple_dir))
        self.assertTrue(os.path.exists(test_simple_file))
        with open(test_simple_file) as fp:
            content = \
                'Hello world. {{ foo }}\n' \
                'Test\n'
            self.assertEqual(fp.read(), content)


def _cleanup_dest_dir():
    # clean up dest folder
    for item in glob.iglob(os.path.join(here, 'roles', '*')):
        if not os.path.isdir(item):
            continue
        shutil.rmtree(item) 

def _init_playbook(path):
    from ansible.playbook import PlayBook
    from ansible.inventory import Inventory
    from ansible import callbacks
    from ansible import utils

    inventory = Inventory(os.path.join(here, 'test_hosts'))
    
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
    
    playbook = PlayBook(
        playbook=os.path.join(path),
        inventory=inventory,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats)
    return playbook


def test_role_as_dict():
    """If not used role, plugin must be raised error.
    """
    _cleanup_dest_dir()
    playbook = _init_playbook(os.path.join(here, 'testrun_no_role.yml'))
    result = playbook.run()
    assert type(result) == dict


def test_role_as_str():
    """Case of use  string
    """
    _cleanup_dest_dir()
    playbook = _init_playbook(os.path.join(here, 'testrun_str_role.yml'))
    result = playbook.run()
    assert type(result) == dict

def test_role_as_dict():
    """Case of use dictionary instead  of string
    """
    _cleanup_dest_dir()
    playbook = _init_playbook(os.path.join(here, 'testrun_dict_role.yml'))
    result = playbook.run()
    assert type(result) == dict
