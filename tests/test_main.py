"""Test the cfg_load module."""

# core modules
from unittest.mock import patch
import os
import pkg_resources
import unittest

# internal modules
import cfg_load


class MainTest(unittest.TestCase):
    """Tests for the cfg_load module."""

    def test_load_yaml(self):
        path = '../examples/cifar10_baseline.yaml'  # always use slash
        filepath = pkg_resources.resource_filename('cfg_load', path)
        cfg_load.load(filepath)

    def test_load_ini(self):
        path = '../examples/db_cfg.ini'  # always use slash
        filepath = pkg_resources.resource_filename('cfg_load', path)
        cfg_load.load(filepath)

    def test_load_json(self):
        path = '../examples/test.json'  # always use slash
        filepath = pkg_resources.resource_filename('cfg_load', path)
        cfg_load.load(filepath)

    def test_load_unknown(self):
        path = '../README.md'  # always use slash
        filepath = pkg_resources.resource_filename('cfg_load', path)
        with self.assertRaises(NotImplementedError):
            cfg_load.load(filepath)

    @patch.dict(os.environ, {'foo': 'foo',
                             'nb_foo': '1337',
                             '_ignore': 'me',
                             'interesting': 'simple'})
    def test_environ(self):
        config = {'foo': 'bar',
                  'answer': 42,
                  'nb_foo': 42,
                  '_ignore': 'bar',
                  'interesting': (1, 2)}
        expected = {'foo': 'foo',
                    'answer': 42,
                    'nb_foo': 1337,
                    '_ignore': 'bar',
                    'interesting': 'simple'}
        loaded_cfg = cfg_load.load_env(config)
        self.assertDictEqual(expected, loaded_cfg)
