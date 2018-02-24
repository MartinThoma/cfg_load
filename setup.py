from setuptools import find_packages
from setuptools import setup

config = {
    'name': 'cfg_load',
    'version': '0.1.0',
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
    'long_description': ("A tookit for language identification."),
    'install_requires': [
        'PyYAML>=3.12',
    ],
    'tests_require': [
        'pytest>=3.3.2',
        'pytest-cov>=2.5.1',
        'pytest-pep8>=1.0.6',
    ],
    'keywords': ['Machine Learning', 'Data Science'],
    'download_url': 'https://github.com/MartinThoma/cfg_load',
    'classifiers': ['Development Status :: 1 - Planning',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 3.5',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': True,
}

setup(**config)
