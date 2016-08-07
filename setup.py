# pylint: disable=I0011,C0301
from __future__ import absolute_import, unicode_literals

import os
from setuptools import find_packages, setup

__VERSION__ = '0.1.1'


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-namespaced-session',
    version=__VERSION__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django<1.9',
    ],
    license='MIT',
    description='Django app which makes it easier to work with dictionaries in sessions',
    long_description=README,
    url='https://github.com/ckot/django-namespaced-session/',
    author='Scott Silliman',
    author_email='scott.t.silliman@gmail.com',
    classifiers=[
        'Private :: Do Not Upload'
    ],
)
