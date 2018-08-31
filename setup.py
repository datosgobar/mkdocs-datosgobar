from setuptools import setup, find_packages
from distutils.core import Command
import os

VERSION = '1.0'


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
    install_requires=['mkdocs>=1.0'],
    python_requires='>=2.7.9,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    entry_points={
        'mkdocs.themes': [
            'datosgobar_docs=mkdocs_datosgobar.datosgobar_docs'
        ]
    },
    zip_safe=False
)
