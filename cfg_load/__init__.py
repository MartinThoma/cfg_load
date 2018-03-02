#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Core functions of the cfg_load."""

# core modules
from datetime import datetime, timezone
import collections
import configparser
import imp
import json
import logging
import os
import pprint
import sys

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
    config : Configuration(collections.Mapping)
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
        config = load_modules(config)
        config = load_env(config)
        config = Configuration(config, cfg_filepath=filepath)
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


def load_modules(config):
    """
    Every key [SOMETHING]_module_path is loaded as a module.

    The module is accessible at config['SOMETHING'].

    Parameters
    ----------
    config : dict

    Returns
    -------
    config : dict
    """
    keyword = '_module_path'
    for key in list(config.keys()):
        if hasattr(key, 'endswith'):
            if key.startswith('_'):
                continue
            if key.endswith(keyword):
                sys.path.insert(1, os.path.dirname(config[key]))
                loaded_module = imp.load_source('foobar', config[key])
                target_key = key[:-len(keyword)]
                config[target_key] = loaded_module
        if type(config[key]) is dict:
            config[key] = load_modules(config[key])
    return config


def load_env(config):
    """
    Load environment variables in config.

    Parameters
    ----------
    config : dict

    Returns
    -------
    config : dict
    """
    logger = logging.getLogger(__name__)
    for env_name in os.environ:
        if env_name.startswith('_'):
            continue
        if env_name in config:
            if isinstance(config[env_name], str):
                config[env_name] = os.environ[env_name]
            elif isinstance(config[env_name], (list, dict, float, int, bool)):
                config[env_name] = json.loads(os.environ[env_name])
            else:
                logger.warning('Configuration value was {} of type {}, but '
                               'is overwritten with a string from the '
                               'environment')
                config[env_name] = os.environ[env_name]
    return config


class Configuration(collections.Mapping):
    """
    Configuration class.

    Essentially, this is an immutable dictionary.

    Parameters
    ----------
    cfg_dict : dict
    """

    def __init__(self, cfg_dict, cfg_filepath):
        self._dict = dict(cfg_dict)   # make a copy
        self._hash = None
        self._add_meta(cfg_filepath)

    def __getitem__(self, key):
        return self._dict[key]

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return iter(self._dict)

    def __eq__(self, other):
        return self._dict == other._dict

    def set(self, key, value):
        """
        Set a value in the configuration.

        Although it is discouraged to do so, it might be necessary in some
        cases.

        If you need to overwrite a dictionary, then you should do:

        >> inner_dict = cfg['key']
        >> inner_dict['inner_key'] = 'new_value'
        >> cfg.set('key', inner_dict)
        """
        self._dict[key] = value
        return self

    def __str__(self):
        return 'Configuration({})'.format(self.meta['cfg_filepath'])

    def __repr__(self):
        return str(self)

    def pformat(self, indent=4):
        """
        Pretty-format the configuration.

        Parameters
        ----------
        indent : int

        Returns
        -------
        pretty_format_cfg : str
        """
        pp = pprint.PrettyPrinter(indent=indent)
        return pp.pformat(self._dict)

    def _add_meta(self, cfg_filepath):
        """
        Add meta data to configuration.

        Parameters
        ----------
        config : dict
        cfg_filepath : str

        Returns
        -------
        config : dict
        """
        self.meta = {'cfg_filepath': os.path.abspath(cfg_filepath),
                     'parse_datetime': datetime.now(timezone.utc)}
        return self
