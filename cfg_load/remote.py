#!/usr/bin/env python

"""Load files from remote locations."""

# core modules
from urllib.request import urlretrieve
import os


def load(source_url, sink_path, policy='load_if_missing'):
    """
    Load remote files from source_url to sink_path.

    Parameters
    ----------
    source_url : str
    sink_path : str
    policy : {'load_always', 'load_if_missing'}
    """
    file_exists = os.path.isfile(sink_path)
    if file_exists and policy == 'load_if_missing':
        return
    for protocol in ['http://', 'https://']:
        if source_url.startswith(protocol):
            load_requests(source_url, sink_path)
    for protocol in ['ftp://']:
        if source_url.startswith(protocol):
            load_urlretrieve(source_url, sink_path)


def load_requests(source_url, sink_path):
    """
    Load a file from an URL (e.g. http).

    Parameters
    ----------
    source_url : str
        Where to load the file from.
    sink_path : str
        Where the loaded file is stored.
    """
    import requests
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(sink_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def load_urlretrieve(source_url, sink_path):
    """
    Load a file from an URL with urlretrieve.

    Parameters
    ----------
    source_url : str
        Where to load the file from.
    sink_path : str
        Where the loaded file is stored.
    """
    urlretrieve(source_url, sink_path)
