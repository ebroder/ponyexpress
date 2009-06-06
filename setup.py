#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name="PonyExpress",
    version="0.0.0",
    description="The PonyExpress - A tagging IMAP server",
    author="Evan Broder",
    author_email="broder@mit.edu",
    license="MIT",
    packages=find_packages(),
    #install_requires=['Twisted_Mail', 'SQLAlchemy>=0.5.0,<0.6a']
)
