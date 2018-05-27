#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the cfg_load module."""

from __future__ import unicode_literals

# core modules
try:
    from unittest.mock import patch
except ImportError:  # Python 2.7
    from mock import patch
import os
import pkg_resources
import unittest

# 3rd party modules
from moto import mock_s3
import boto3

# internal modules
import cfg_load


class MainTest(unittest.TestCase):
    """Tests for the cfg_load module."""

    @mock_s3
    def test_load_yaml(self):
        # Set up bucket
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='ryft-public-sample-data')
        obj = conn.Object('ryft-public-sample-data',
                          'ryft-server-0.13.0-rc3_amd64.deb')
        obj.put(Body=b'foo')

        # Run Test
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

    @mock_s3
    def test_configuration_class(self):
        # Set up bucket
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='ryft-public-sample-data')
        obj = conn.Object('ryft-public-sample-data',
                          'ryft-server-0.13.0-rc3_amd64.deb')
        obj.put(Body=b'foo')

        # Run Test
        path = '../examples/test.json'  # always use slash
        filepath = pkg_resources.resource_filename('cfg_load', path)
        cfg2 = cfg_load.load(filepath)

        path = '../examples/cifar10_baseline.yaml'  # always use slash
        filepath = pkg_resources.resource_filename('cfg_load', path)
        cfg = cfg_load.load(filepath)
        self.assertEqual(cfg['umlautüößhere'], 'wörks')
        self.assertEqual(len(cfg), 11)
        # test cfg.__iter__
        for key in cfg:
            continue
        self.assertNotEqual(cfg, cfg2)
        self.assertTrue(isinstance(repr(cfg), str))
        self.assertTrue(isinstance(str(cfg), str))
        self.assertTrue(isinstance(cfg.pformat(), str))
        cfg.set('foo', 'bar')
