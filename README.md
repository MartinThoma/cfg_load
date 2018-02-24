# cfg_load

Loading configuration files is a common task in many projects. This package
does the job.


## Installation

The recommended way to install cfg_load is:

```
$ pip install cfg_load --user
```

If you want the latest version:

```
$ git clone https://github.com/MartinThoma/cfg_load.git; cd cfg_load
$ pip instell -e . --user
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


## Features

* No key that starts with `_` will ever be touched.
* Keys ending in `_path` will be made absolute.
* Don't worry about Unicode.

Not there, but planned fo the future:

* Every key ending with `_load_path` has to have `source` and `sink`. Sources
  which are AWS S3 URLs and URLs starting with http(s) will be loaded
  automatically and stored in the sink. A `policy` parameter can specify if
  it should be `load_always` or `load_if_missing`.
* Every key `[something]_cfg_path` will trigger `cfg_load` to search for
  another config file and append it at `[something]`. By this way you can
  define configuration files recursively.
* Every key `[something]_module_path` will trigger `cfg_load` to load the
  file found at `[something]_module_path` as a Python module to `[something]`.


## Development

Check tests with `tox`.
