#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name="icbing",
    version="0.0.0",
    description="I Can't Believe It's Not Gmail - A tagging IMAP server",
    author="Evan Broder",
    author_email="broder@mit.edu",
    license="MIT",
    packages=find_packages(),
    #install_requires=['Twisted_Mail']
)
