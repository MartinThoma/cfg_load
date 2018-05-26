#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the cfg_load.paths module."""

# core modules
import os
import unittest

# internal modules
import cfg_load.remote


class RemoteTest(unittest.TestCase):
    """Tests for the cfg_load.paths module."""

    def test_load_http(self):
        source = ('https://martin-thoma.com/images/2017/02/'
                  'Martin_Thoma_web_thumb.jpg')
        sink = 'ignore_image-random.jpg'
        cfg_load.remote.load(source, sink)
        os.remove(sink)

    def test_load_ftp(self):
        source = ('ftp://speedtest.tele2.net/1KB.zip')
        sink = 'ignore_zip-random.zip'
        cfg_load.remote.load(source, sink)
        os.remove(sink)

    def test_load_aws_s3(self):
        source = ('s3://ryft-public-sample-data/'
                  'ryft-server-0.13.0-rc3_amd64.deb')
        sink = 'ignore.deb'
        cfg_load.remote.load(source, sink)
        os.remove(sink)

    def test_load_aws_s3_error(self):
        source = 's3://ryft-public-sample-data/'
        sink = 'ignore.deb'
        with self.assertRaises(Exception):
            cfg_load.remote.load(source, sink)

    def test_load_unknown_protocol(self):
        source = ('bt://sample.com/example.zip')
        sink = 'ignore_zip-random.zip'
        with self.assertRaises(Exception):
            cfg_load.remote.load(source, sink)
