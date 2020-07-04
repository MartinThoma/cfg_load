# Core Library
import logging
from typing import Dict


def pytest_configure(config: Dict) -> None:
    """Flake8 is to verbose. Mute it."""
    logging.getLogger("flake8").setLevel(logging.WARN)
