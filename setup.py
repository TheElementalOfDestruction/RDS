import os
import re

from setuptools import setup

# a handful of variables that are used a couple of times
github_url = 'https://github.com/TheElementalOfDestruction/rds'
main_module = 'rds'

# read in the description from README
with open('README.rst', 'rb') as stream:
    long_description = stream.read().decode('utf-8').replace('\r', '')

# Just to be safe, we want to avoid
version_re = re.compile("__version__ = '(?P<version>[0-9\\.]*)'")
with open('rds/__init__.py', 'r') as stream:
    contents = stream.read()
match = version_re.search(contents)
version = match.groupdict()['version']

setup(
    name=main_module,
    version=version,
    description="Python Redundant Data Storage Module",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url=github_url,
    download_url='%s/archives/master' % github_url,
    author='Destiny Peterson (The Elemental of Destruction)',
    author_email='arceusthe@gmail.com',
    license='GPL',
    packages=[main_module],
    py_modules=[main_module],
    include_package_data=True,
)
