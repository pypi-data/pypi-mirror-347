#!/usr/bin/env python
"""This module contains setup instructions for pytube."""
import codecs
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# with open(os.path.join(here, "fly_dev_run", "version.py")) as fp:
#     exec(fp.read())

setup(
    name="fly_dev_run", 
    version="0.2.2", 
    author="FlyThinker Huang",
    author_email="flythinker@qq.com",
    packages=["fly_dev_run"],
    package_data={"": ["LICENSE"],},
    url="",
    license="The Unlicense (Unlicense)",
    entry_points={
        "console_scripts": [
            "dev_run = fly_dev_run.cli_main:main"],},  
    classifiers=[
        "Development Status :: 5 - Production/Stable", 
        "Environment :: Console",
        "Intended Audience :: Developers",                
        "Operating System :: OS Independent",        
        "Programming Language :: Python",                
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=long_description,
    zip_safe=True,
    python_requires=">=3.7",    
    keywords=["dev_tools", "python", "run"], 
)
