#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Módulo de entrada para la interfaz de línea de comandos

Todos los módulos de mkdocs_datosgobar se pueden llamar por línea de comandos
siempre que tengan un método main() definido en el módulo, que recibe
argumentos y realiza acciones relacionadas con el core de su funcionalidad.

Example:
    mkdocs_datosgobar md2pdf mkdocs.yml docs/portal-andino-docs.pdf
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os
import sys
import importlib


def main():
    module_name = sys.argv[1]
    module = importlib.import_module("." + module_name, "mkdocs_datosgobar")
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    module.main(*args)


if __name__ == '__main__':
    main()
