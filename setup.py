from setuptools import find_packages
from setuptools import setup
import io
import os

# internal modules
exec(open('cfg_load/_version.py').read())

tests_require = ['pytest>=3.3.2',
                 'pytest-cov>=2.5.1',
                 'pytest-pep8>=1.0.6',
                 'boto3',
                 ]
aws_require = ['boto3']


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()

config = {
    'name': 'cfg_load',
    'version': __version__,
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': find_packages(),
    'scripts': ['bin/cfg_load'],
    'platforms': ['Linux'],
    'url': 'https://github.com/MartinThoma/cfg_load',
    'license': 'MIT',
    'description': 'Library for loading configuration files',
    'long_description': read('README.md'),
    'install_requires': [
        'PyYAML>=3.12',
        'requests>=2.18.4',
        'pytz>=2018.4',
        'mpu>=0.2.0',
    ],
    'tests_require': tests_require,
    'extras_require': {'all': tests_require + aws_require, },
    'keywords': ['Machine Learning', 'Data Science'],
    'download_url': 'https://github.com/MartinThoma/cfg_load',
    'classifiers': ['Development Status :: 1 - Planning',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3.6',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': True,
}

setup(**config)
