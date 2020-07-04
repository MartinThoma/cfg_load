"""cfg_load is a library for handling configuration."""

# Third party
from setuptools import setup

setup(
    install_requires=[
        "mpu[io]>=0.15.0",
        "pytz>=2018.4",
        "PyYAML>=4.2b1",
        "requests>=2.18.4",
        "six>=1.11.0",
    ],
    extras_require={"all": "boto3"},
)
