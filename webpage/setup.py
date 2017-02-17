"""
App for running Python apps on Bluemix
"""

# Always prefer setuptools over distutils
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

setup(
    name='co_occurrences',
    version='1.0.0',
    description='Hello World app for running Python apps on Bluemix',
    url='https://github.com/anshu92/co_occurrence_heroku/',
    license='Apache-2.0'
)
