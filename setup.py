# -*- coding: utf-8 -*-
import codecs

from setuptools import find_packages
from setuptools import setup

author = 'liying'
email = 'liruoer2008@yeah.net'
version = '1.0.0'
url = 'https://github.com/liying2008/document-template'

with codecs.open("README.rst", "r", "utf-8") as fh:
    long_description = fh.read()

setup(
    name='document-template',
    version=version,
    description="Generate documents from templates.",
    long_description=long_description,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    keywords='template document parser',
    author=author,
    author_email=email,
    url=url,
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points={},
)
