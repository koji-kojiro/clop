#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from clop import __version__

config = {
    'name': 'clop',
    'author': 'TANI Kojiro',
    'author_email': 'kojiro0531@gmail.com',
    'url': 'https://github.com/koji-kojiro/clop',
    'description': 's-expressions to c transpiler',
    'long_description': open('README.md', 'r').read(),
    'long_description_content_type': 'text/markdown',
    'license': 'MIT',
    'version': __version__,
    'install_requires': [],
    'classifiers': [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
    ],
    'packages': find_packages(),
    'entry_points': {
        'console_scripts':[
            'clop = clop.cmd:main',
        ],
     }
}

if __name__ == '__main__':
    setup(**config)
