[![PyPI version](https://badge.fury.io/py/cfg-load.svg)](https://badge.fury.io/py/cfg-load)
[![Python Support](https://img.shields.io/pypi/pyversions/cfg_load.svg)](https://pypi.org/project/cfg_load/)
[![Documentation Status](https://readthedocs.org/projects/cfg_load/badge/?version=latest)](http://cfg-load.readthedocs.io/en/latest/)
[![Build Status](https://travis-ci.org/MartinThoma/cfg_load.svg?branch=master)](https://travis-ci.org/MartinThoma/cfg_load)
[![Coverage Status](https://coveralls.io/repos/github/MartinThoma/cfg_load/badge.svg?branch=master)](https://coveralls.io/github/MartinThoma/cfg_load?branch=master)

# cfg_load

Loading configuration files is a common task in many projects. This package
does the job.


## Installation

The recommended way to install cfg_load is:

```
$ pip install cfg_load[all] --user
```

Note: You might have to escape `[` and `]` in some shells like ZSH.

If you want the latest version:

```
$ git clone https://github.com/MartinThoma/cfg_load.git; cd cfg_load
$ pip instell -e .[all] --user
```


## Usage

`cfg_load` is intended to be used as a library. In your code, it will mostly
be used like this:

```
import cfg_load

config = cfg_load.load('some/path.yaml')
```

In order to check if it is doing what you expect, you can use it as a command
line tool:

```
$ cfg_load examples/cifar10_baseline.yaml

{   'dataset': {   'script_path': '/home/moose/GitHub/cfg_loader/datasets/cifar10_keras.py'},
    'evaluate': {   'augmentation_factor': 32,
                    'batch_size': 1000,
                    'data_augmentation': {   'channel_shift_range': 0,
                                             'featurewise_center': False,
                                             'height_shift_range': 0.15,
                                             'horizontal_flip': True,
                                             'rotation_range': 0,
                                             'samplewise_center': False,
                                             'samplewise_std_normalization': False,
                                             'shear_range': 0,
                                             'vertical_flip': False,
                                             'width_shift_range': 0.15,
                                             'zca_whitening': False,
                                             'zoom_range': 0}},
    'model': {   'script_path': '/home/moose/GitHub/cfg_loader/models/baseline.py'},
    'optimizer': {   'initial_lr': 0.0001,
                     'script_path': '/home/moose/GitHub/cfg_loader/optimizers/adam_keras.py'},
    'train': {   'artifacts_path': '/home/moose/GitHub/cfg_loader/artifacts/cifar10_baseline',
                 'batch_size': 64,
                 'data_augmentation': {   'channel_shift_range': 0,
                                          'featurewise_center': False,
                                          'height_shift_range': 0.1,
                                          'horizontal_flip': True,
                                          'rotation_range': 0,
                                          'samplewise_center': False,
                                          'samplewise_std_normalization': False,
                                          'shear_range': 0,
                                          'vertical_flip': False,
                                          'width_shift_range': 0.1,
                                          'zca_whitening': False,
                                          'zoom_range': 0},
                 'epochs': 1000,
                 'script_path': '/home/moose/GitHub/cfg_loader/train/train_keras.py'}}
```

You can see that it automatically detected that the file is a YAML file and
when you compare it to `cfg_load examples/cifar10_baseline.yaml --raw` you can
also see that it made the paths absolute.


## Good Application Practice

```
import cfg_load

# Load defaults
base_cfg = cfg_load.load('some/path.yaml')

# Overwrite defaults if user defined it
user_cfg = cfg_load.load('other/path.yaml')
user_cfg = base_cfg.update(user_cfg)

# Overwrite user default with environment variables
env_mapping = cfg_load.load('other/env_mapping.yaml')
cfg = user_cfg.apply_env(env_mapping)
```


## Features

* You load your config like this: `cfg = cfg_load.load('examples/test.json')`
* No key that starts with `_` will ever be touched.
* Keys ending in `_path` will be made absolute.
* Don't worry about Unicode.
* Every key `[something]_module_path` triggers `cfg_load` to load the
  file found at `[something]_module_path` as a Python module to
  `cfg.modules['something']`.
* If an environment variable with the same name as a config key exists, the
  take the value of the environment variable. *Please note*: If the type of
  the overwritten key is not str, then `cfg_load` applies `json.loads` to the
  environment variable.
* Every key ending with `_load_url` has to have `source_url` and `sink_path`.
  Files from `source_url` will be loaded automatically and stored in the
  `sink_path`. A `policy` parameter can specify if it should be `load_always`
  or `load_if_missing`.

Not there, but planned fo the future:

* Every key `[something]_cfg_path` will trigger `cfg_load` to search for
  another config file and append it at `[something]`. By this way you can
  define configuration files recursively.


## Development

Check tests with `tox`.
