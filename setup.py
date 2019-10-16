"""cfg_load is a library for handling configuration."""

# Core Library
import io
import os

# Third party
from setuptools import find_packages, setup

tests_require = [
    "boto3",
    "google-compute-engine",
    "pytest-black",
    "pytest-cov>=2.5.1",
    "pytest-flake8==1.0.4",
    "pytest>=3.3.2",
]
aws_require = ["boto3"]


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(
        os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8"
    ) as f:
        return f.read()


config = {
    "name": "cfg_load",
    "version": "0.9.0",  # keep in sync with cfg_load/_version.py
    "author": "Martin Thoma",
    "author_email": "info@martin-thoma.de",
    "maintainer": "Martin Thoma",
    "maintainer_email": "info@martin-thoma.de",
    "packages": find_packages(),
    "entry_points": {"console_scripts": ["cfg_load=cfg_load.cli:entry_point"]},
    "platforms": ["Linux"],
    "url": "https://github.com/MartinThoma/cfg_load",
    "license": "MIT",
    "description": "Library for loading configuration files",
    "long_description_content_type": "text/markdown",
    "long_description": read("README.md"),
    "install_requires": [
        "mpu[io]>=0.15.0",
        "pytz>=2018.4",
        "PyYAML>=4.2b1",
        "requests>=2.18.4",
        "six>=1.11.0",
    ],
    "tests_require": tests_require,
    "extras_require": {"all": tests_require + aws_require},
    "keywords": ["Machine Learning", "Data Science"],
    "download_url": "https://github.com/MartinThoma/cfg_load",
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    "zip_safe": True,
}

setup(**config)
