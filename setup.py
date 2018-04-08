#!/usr/bin/python
# -*- coding: utf-8 -*-


from setuptools import find_packages
from setuptools import setup

author = 'liying'
email = 'liruoer2008@yeah.net'
version = '0.0.2'
url = 'https://github.com/liying2008/document-template'

setup(
    name='document-template',
    version=version,
    description="Generate documents according to the template.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],
    keywords='Template document',
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
    project_urls={
        'Source': url,
        'Tracker': url + '/issues',
    },
    entry_points={},
)
