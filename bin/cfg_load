#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Show what cfg_load.load() returns."""

# core modules
import logging.config

# internal modules
import cfg_load


config = {
    "LOGGING": {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s-%(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "cfg_load.info.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            },
            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "cfg_load.errors.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "my_module": {
                "level": "ERROR",
                "handlers": [
                    "console"
                ],
                "propagate": False
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                "console",
                "info_file_handler",
                "error_file_handler"
            ]
        }
    }
}

logging.config.dictConfig(config['LOGGING'])


def get_parser():
    """Show what cfg_load.load() returns."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(dest='filename',
                        help='read this configuration file',
                        metavar='FILE')
    parser.add_argument('--raw',
                        action='store_true', dest='raw', default=False,
                        help='only get the raw file; do not execute anything '
                             'else')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    loaded = cfg_load.load(args.filename, args.raw)
    if hasattr(loaded, 'pformat'):
        print(loaded.pformat())
    else:
        print(loaded)
