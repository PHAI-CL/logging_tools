import setuptools
from setuptools import setup
import os

if __name__ == "__main__":
    setup_path = os.path.dirname(os.path.abspath(__file__))
    setup(
        name="logger",
        version="0.1",
        description="Logging Tools",
        packages=setuptools.find_packages(exclude=["*tests*"]),
    )
