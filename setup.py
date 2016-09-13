# pylint: disable=I0011,C0301
from __future__ import absolute_import, unicode_literals

import os
from setuptools import find_packages, setup

from namespaced_session import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-namespaced-session',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=1.7,<1.10',
    ],
    # tests_require=['tox'],
    test_suite="runtests.main",
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
