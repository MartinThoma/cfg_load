#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Load files from remote locations."""

# core modules
try:
    from urllib.request import urlretrieve, urlcleanup
except ImportError:  # Python 2
    from urllib import urlretrieve, urlcleanup
import os
import requests


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
    known_protocols = [('http://', load_requests),
                       ('https://', load_requests),
                       ('ftp://', load_urlretrieve),
                       ('s3://', load_aws_s3)]
    for protocol, handler in known_protocols:
        if source_url.startswith(protocol):
            handler(source_url, sink_path)
            break
    else:
        raise RuntimeError('Unknown protocol: source_url=\'{}\''
                           .format(source_url))


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
    urlcleanup()
    urlretrieve(source_url, sink_path)


def load_aws_s3(source_url, sink_path):
    """
    Load a file from AWS S3.

    Parameters
    ----------
    source_url : str
        Where to load the file from.
    sink_path : str
        Where the loaded file is stored.
    """
    # Import here to make this dependency optional
    import boto3

    # Parse parts
    url = source_url[len('s3://'):]
    bucket, key = url.split('/', 1)
    if len(key) == 0:
        raise ValueError('Key was empty for source_url=\'{}\''
                         .format(source_url))

    # Download file
    client = boto3.Session().client('s3')
    response = client.get_object(Bucket=bucket, Key=key)

    # Write file to local file
    body_string = response['Body'].read()
    with open(sink_path, 'wb') as f:
        f.write(body_string)
