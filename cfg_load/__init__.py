#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Core functions of the cfg_load."""

# core modules
import configparser
import io
import json
import os

# 3rd party modules
import yaml

# internal modules
import cfg_load.paths


def load(filepath, load_raw=False):
    """
    Load a configuration file.

    Parameters
    ----------
    filepath : str
        Path to the configuration file.
    load_raw : bool, optional (default: False)
        Load only the raw configuration file as a dict,
        without applying any logic to it.

    Returns
    -------
    config : dict
    """
    if filepath.lower().endswith('.yaml') or filepath.lower().endswith('.yml'):
        config = load_yaml(filepath)
    elif filepath.lower().endswith('.json'):
        config = load_json(filepath)
    elif filepath.lower().endswith('.ini'):
        config = load_ini(filepath)
    else:
        raise NotImplementedError('Extension of the file \'{}\' was not '
                                  'recognized.'
                                  .format(filepath))
    if not load_raw:
        reference_dir = os.path.dirname(filepath)
        config = cfg_load.paths.make_paths_absolute(reference_dir, config)
    return config


def load_yaml(yaml_filepath):
    """
    Load a YAML file.

    Parameters
    ----------
    yaml_filepath : str

    Returns
    -------
    config : dict
    """
    with open(yaml_filepath, 'r') as stream:
        config = yaml.load(stream)
    return config


def load_json(json_filepath):
    """
    Load a JSON file.

    Parameters
    ----------
    json_filepath : str

    Returns
    -------
    config : dict
    """
    with open(json_filepath, 'r') as stream:
        config = json.load(stream)
    return config


def load_ini(ini_filepath):
    """
    Load a ini file.

    Parameters
    ----------
    ini_filepath : str

    Returns
    -------
    config : OrderedDict
    """
    config = configparser.ConfigParser()
    config.read(ini_filepath)
    return config._sections
