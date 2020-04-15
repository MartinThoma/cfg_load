#!/usr/bin/env python

"""Test the cfg_load module."""


# Core Library
import os
from io import StringIO
from unittest.mock import patch
from urllib import request

# Third party
import boto3
import pkg_resources
import pytest
import requests
from moto import mock_s3

# First party
import cfg_load


class MockUrllibResponse:
    @staticmethod
    def read():
        return b"foo response"


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "http://someurl.com/test.json":
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == "http://someotherurl.com/anothertest.json":
        return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)


@pytest.fixture
def mocked_urlopen(monkeypatch):
    """
    monkeypatch the actual urlopen calls done by the internal plugin
    function that connects to bpaste service.
    """
    calls = []

    def mocked(url, data):
        calls.append((url, data))

        class MockFile(StringIO):
            """This is a work around for the fact that StringIO is a slotted class and
            doesn"t have a name attribute.
            """

            name = None

            def __init__(self, name="defaultname.txt", buffer_=None):
                super().__init__(buffer_)
                self.name = name
                self.i = 0

            def read(self, bs):
                # part of html of a normal response
                if self.i < 2:
                    self.i += 1
                    return b"foo"
                else:
                    return False

            def info(self):
                return {"Content-Length": 123}

        return MockFile()

    import urllib.request

    monkeypatch.setattr(urllib.request, "urlopen", mocked)
    return calls


@mock_s3
def test_load_yaml(monkeypatch, requests_mock, mocked_urlopen):
    def mock_urlretrieve(*args, **kwargs):
        return MockUrllibResponse()

    monkeypatch.setattr(request, "urlretrieve", mock_urlretrieve)
    requests_mock.get("http://foo-bar.de/something.JPG", text="data")
    requests_mock.get(
        "https://martin-thoma.com/images/2017/02/Martin_Thoma_web_thumb.jpg",
        text="data",
    )

    # Set up bucket
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="ryft-public-sample-data")
    obj = conn.Object("ryft-public-sample-data", "ryft-server-0.13.0-rc3_amd64.deb")
    obj.put(Body=b"foo")

    # Run Test
    path = "../examples/cifar10_baseline.yaml"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg_load.load(filepath)


def test_load_ini():
    path = "../examples/db_cfg.ini"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg_load.load(filepath)


def test_load_json():
    path = "../examples/test.json"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg_load.load(filepath)


def test_to_dict():
    path = "../examples/test.json"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg = cfg_load.load(filepath)
    dict_ = cfg.to_dict()
    assert isinstance(dict_, dict)


def test_load_unknown():
    path = "../README.md"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    with pytest.raises(NotImplementedError):
        cfg_load.load(filepath)


def test_update():
    path = "../examples/simple_base.yaml"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg_base = cfg_load.load(filepath)

    path = "../examples/simple_user.yaml"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg_update = cfg_load.load(filepath)

    cfg_result = cfg_base.update(cfg_update)
    cfg_expected = {
        "foo": 1,
        "only": "base",
        "nested": {"overwrite": True, "inner_only_base": 28},
    }
    assert cfg_expected == cfg_result._dict


def test_apply_env():
    path = "../examples/simple_base.yaml"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg_base = cfg_load.load(filepath)

    path = "../examples/env_mapping.yaml"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    env_mapping = cfg_load.load(filepath)

    os.environ["nested_overwrite"] = "no"
    cfg = cfg_base.apply_env(env_mapping)

    cfg_expected = {
        "foo": "bar",
        "only": "base",
        "nested": {"overwrite": False, "inner_only_base": 28},
    }

    assert cfg._dict == cfg_expected


@patch.dict(
    os.environ,
    {"foo": "foo", "nb_foo": "1337", "_ignore": "me", "interesting": "simple"},
)
def test_environ():
    config = {
        "foo": "bar",
        "answer": 42,
        "nb_foo": 42,
        "_ignore": "bar",
        "interesting": (1, 2),
    }
    expected = {
        "foo": "foo",
        "answer": 42,
        "nb_foo": 1337,
        "_ignore": "bar",
        "interesting": "simple",
    }
    loaded_cfg = cfg_load.load_env(config)
    assert expected == loaded_cfg


@mock_s3
def test_configuration_class(monkeypatch):
    monkeypatch.setattr(requests, "get", mocked_requests_get)

    # Set up bucket
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket="ryft-public-sample-data")
    obj = conn.Object("ryft-public-sample-data", "ryft-server-0.13.0-rc3_amd64.deb")
    obj.put(Body=b"foo")

    # Run Test
    path = "../examples/test.json"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg2 = cfg_load.load(filepath)

    path = "../examples/cifar10_baseline.yaml"  # always use slash
    filepath = pkg_resources.resource_filename("cfg_load", path)
    cfg = cfg_load.load(filepath)
    assert cfg["umlautüößhere"] == "wörks"
    assert len(cfg) == 11
    # test cfg.__iter__
    for key in cfg:
        continue
    assert cfg != cfg2
    assert isinstance(repr(cfg), str)
    assert isinstance(str(cfg), str)
    assert isinstance(cfg.pformat(), str)
    assert isinstance(cfg.pformat(meta=True), str)
    cfg.set("foo", "bar")
