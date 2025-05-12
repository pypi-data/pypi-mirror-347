from setuptools import setup, find_packages

import pathlib

this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cashcat',
    version='1004',
    py_modules=['cashcat'],
    url='https://github.com/bitrate16/cashcat',
    author='bitrate16',
    author_email='bitrate16@gmail.com',
    description='simple file integrity verification tool',
    license='AGPL-3',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
