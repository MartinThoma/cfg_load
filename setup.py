"""cfg_load is a library for handling configuration."""

# Third party
from setuptools import setup

tests_require = [
    "boto3",
    "google-compute-engine",
    "pytest-black",
    "pytest-cov>=2.5.1",
    "flake8==3.7.9",  # https://github.com/tholo/pytest-flake8/issues/66
    "pytest-flake8==1.0.4",
    "pytest>=3.3.2",
    "requests_mock",
]
aws_require = ["boto3"]


setup(
    install_requires=[
        "mpu[io]>=0.15.0",
        "pytz>=2018.4",
        "PyYAML>=4.2b1",
        "requests>=2.18.4",
        "six>=1.11.0",
    ],
    tests_require=tests_require,
    extras_require={"all": tests_require + aws_require},
)
