# -*- coding: utf-8 -*-
import codecs
import os
import sys

from setuptools import find_packages
from setuptools import setup

import document_template

url = 'https://github.com/liying2008/document-template'

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

with codecs.open("README.rst", "r", "utf-8") as fh:
    long_description = fh.read()

setup(
    name='document-template',
    version=document_template.__version__,
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
    project_urls={
        'Documentation': url,
        'Source': url,
    },
    keywords='template document parser',
    author=document_template.__author__,
    author_email=document_template.__email__,
    maintainer=document_template.__author__,
    maintainer_email=document_template.__email__,
    url=url,
    license=document_template.__license__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={},
)
