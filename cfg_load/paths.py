#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Path manipulation functions."""

# core modules
import os


def make_paths_absolute(dir_, cfg):
    """
    Make all values for keys ending with `_path` absolute to dir_.

    Parameters
    ----------
    dir_ : str
    cfg : dict

    Returns
    -------
    cfg : dict
    """
    for key in cfg.keys():
        if hasattr(key, 'endswith'):
            if key.startswith('_'):
                continue
            if key.endswith('_path'):
                if cfg[key].startswith('~'):
                    cfg[key] = os.path.expanduser(cfg[key])
                else:
                    cfg[key] = os.path.join(dir_, cfg[key])
                cfg[key] = os.path.abspath(cfg[key])
        if type(cfg[key]) is dict:
            cfg[key] = make_paths_absolute(dir_, cfg[key])
    return cfg
