#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test the cfg_load.paths module."""

# core modules
import os
import unittest

# 3rd party modules
from moto import mock_s3
import boto3
import pytest

# internal modules
import cfg_load.remote


class RemoteTest(unittest.TestCase):
    """Tests for the cfg_load.paths module."""

    def test_load_http(self):
        source = "https://martin-thoma.com/images/2017/02/Martin_Thoma_web_thumb.jpg"
        sink = "ignore_image-random.jpg"
        cfg_load.remote.load(source, sink)
        os.remove(sink)

    @pytest.mark.xfail(reason="bug 110")
    def test_load_ftp(self):
        source = "ftp://speedtest.tele2.net/1KB.zip"
        sink = "ignore_zip-random.zip"
        cfg_load.remote.load(source, sink)
        os.remove(sink)

    @mock_s3
    def test_load_aws_s3(self):
        # Set up bucket
        conn = boto3.resource("s3", region_name="us-east-1")
        conn.create_bucket(Bucket="ryft-public-sample-data")
        obj = conn.Object("ryft-public-sample-data", "ryft-server-0.13.0-rc3_amd64.deb")
        obj.put(Body=b"foo")

        # Run Test
        source = "s3://ryft-public-sample-data/" "ryft-server-0.13.0-rc3_amd64.deb"
        sink = "ignore.deb"
        cfg_load.remote.load(source, sink)
        os.remove(sink)

    def test_load_aws_s3_error(self):
        source = "s3://ryft-public-sample-data/"
        sink = "ignore.deb"
        with self.assertRaises(ValueError):
            cfg_load.remote.load(source, sink)

    def test_load_unknown_protocol(self):
        source = "bt://sample.com/example.zip"
        sink = "ignore_zip-random.zip"
        with self.assertRaises(RuntimeError):
            cfg_load.remote.load(source, sink)
