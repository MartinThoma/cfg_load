"""Test the cfg_load.paths module."""

# core modules
import unittest
from copy import deepcopy
from unittest.mock import patch

# internal modules
import cfg_load.paths


class PathsTest(unittest.TestCase):
    """Tests for the cfg_load.paths module."""

    def test_make_paths_absolute_empty(self):
        cfg_load.paths.make_paths_absolute('/', {})

    def test_make_paths_absolute_trivial(self):
        cfg = {'foo': 'bar'}
        loaded_cfg = cfg_load.paths.make_paths_absolute('/', deepcopy(cfg))
        self.assertDictEqual(cfg, loaded_cfg)

    def test_make_paths_absolute_begin_underscore(self):
        cfg = {'_': 'don\'t touch me'}
        loaded_cfg = cfg_load.paths.make_paths_absolute('/', deepcopy(cfg))
        self.assertDictEqual(cfg, loaded_cfg)

        cfg = {'_path': 'don\'t touch me'}
        loaded_cfg = cfg_load.paths.make_paths_absolute('/', deepcopy(cfg))
        self.assertDictEqual(cfg, loaded_cfg)

        cfg = {'_path': {'a_path': 'don\'t touch me'}}
        loaded_cfg = cfg_load.paths.make_paths_absolute('/', deepcopy(cfg))
        self.assertDictEqual(cfg, loaded_cfg)

    def test_make_paths_absolute_begin_underscore_path(self):
        cfg = {'a_path': 'change.me'}
        loaded_cfg = cfg_load.paths.make_paths_absolute('/home/user',
                                                        deepcopy(cfg))
        exp = {'a_path': '/home/user/change.me'}
        self.assertDictEqual(exp, loaded_cfg)

        cfg = {'inner': {'a_path': 'change.me'}}
        loaded_cfg = cfg_load.paths.make_paths_absolute('/home/user',
                                                        deepcopy(cfg))
        exp = {'inner': {'a_path': '/home/user/change.me'}}
        self.assertDictEqual(exp, loaded_cfg)

    def simple_expanduser(input_):
        return input_.replace('~', '/home/user')

    @patch('os.path.expanduser', side_effect=simple_expanduser)
    def test_make_paths_absolute_homedir(self, mock_expanduser):
        cfg = {'a_path': '~/change.me'}
        loaded_cfg = cfg_load.paths.make_paths_absolute('/home/user',
                                                        deepcopy(cfg))
        exp = {'a_path': '/home/user/change.me'}
        self.assertDictEqual(exp, loaded_cfg)
