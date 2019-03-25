#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os

from setuptools import setup, find_packages
from distutils.core import Command

VERSION = '1.0.11'

with open(os.path.abspath("requirements.txt")) as f:
    requirements = [req.strip() for req in f.readlines()]

setup(
    name="mkdocs-datosgobar",
    version=VERSION,
    url='http://www.mkdocs.org',
    license='BSD',
    description='Temas de datosgobar para documentación con MkDocs',
    author='Datos Argentina',
    author_email='datos@modernizacion.gob.ar',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=2.7.9,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    entry_points={
        'mkdocs.themes': [
            'datosgobar_docs=mkdocs_datosgobar.datosgobar_docs'
        ],
        'console_scripts': [
            'mkdocs_datosgobar=mkdocs_datosgobar.__main__:main'
        ]
    },
    zip_safe=False
)
