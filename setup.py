import os

from setuptools import setup

# A handful of variables that are used a couple of times.
github_url = 'https://github.com/TheElementalOfDestruction/rds'
main_module = 'rds'

# Read in the description from README.
with open('README.rst', 'rb') as stream:
    long_description = stream.read().decode('utf-8').replace('\r', '')

from rds import __version__

setup(
    name = main_module,
    version = __version__,
    description = "Python Redundant Data Storage Module",
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    url = github_url,
    download_url = '{}/archives/master'.format(github_url),
    author = 'Destiny Peterson (The Elemental of Destruction)',
    author_email = 'arceusthe@gmail.com',
    license = 'GPL',
    packages = setuptools.find_packages(),
    py_modules = [main_module],
    include_package_data = True,
)
