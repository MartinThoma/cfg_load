"""Path manipulation functions."""

# Core Library
import os
from typing import Dict


def make_paths_absolute(dir_: str, cfg: Dict) -> Dict:
    """
    Make all values for keys ending with `_path` absolute to dir_.

    Parameters
    ----------
    dir_ : str
    cfg : Dict

    Returns
    -------
    cfg : Dict
    """
    if hasattr(cfg, "keys"):
        for key in cfg.keys():
            if hasattr(key, "endswith"):
                if key.startswith("_"):
                    continue
                if key.endswith("_path"):
                    if cfg[key].startswith("~"):
                        cfg[key] = os.path.expanduser(cfg[key])
                    else:
                        cfg[key] = os.path.join(dir_, cfg[key])
                    cfg[key] = os.path.abspath(cfg[key])
            if type(cfg[key]) is dict:
                cfg[key] = make_paths_absolute(dir_, cfg[key])
    elif type(cfg) is list:
        for i, el in enumerate(cfg):
            cfg[i] = make_paths_absolute(dir_, el)
    return cfg
