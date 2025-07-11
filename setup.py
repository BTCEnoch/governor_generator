"""
Setup script for the governor_generator package.
"""

from setuptools import setup, find_packages

setup(
    name="governor_generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tqdm",
        "pytest",
        "pytest-cov"
    ],
    python_requires=">=3.9",
) 