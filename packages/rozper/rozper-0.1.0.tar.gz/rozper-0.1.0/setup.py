# setup.py

from setuptools import setup, find_packages

setup(
    name="rozper",
    version="0.1.0",
    author="Rohit Varma",
    author_email="info@rozper.com",
    description="A simple greeting package by Rozper",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://www.rozper.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
