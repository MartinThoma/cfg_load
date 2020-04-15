#!/usr/bin/env python

"""Test the cfg_load.paths module."""

# Core Library
import os

# Third party
import boto3
import pytest
from moto import mock_s3

# First party
import cfg_load.remote


def test_load_http(requests_mock):
    source = "https://martin-thoma.com/images/2017/02/Martin_Thoma_web_thumb.jpg"
    requests_mock.get(source, text="data")
    sink = "ignore_image-random.jpg"
    cfg_load.remote.load(source, sink)
    os.remove(sink)


@pytest.mark.xfail(reason="bug 110")
def test_load_ftp():
    source = "ftp://speedtest.tele2.net/1KB.zip"
    sink = "ignore_zip-random.zip"
    cfg_load.remote.load(source, sink)
    os.remove(sink)


@mock_s3
def test_load_aws_s3():
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


def test_load_aws_s3_error():
    source = "s3://ryft-public-sample-data/"
    sink = "ignore.deb"
    with pytest.raises(ValueError):
        cfg_load.remote.load(source, sink)


def test_load_unknown_protocol():
    source = "bt://sample.com/example.zip"
    sink = "ignore_zip-random.zip"
    with pytest.raises(RuntimeError):
        cfg_load.remote.load(source, sink)
