"""Test the cfg_load module."""

# core modules
import unittest
import pkg_resources

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
