#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Convierte un archivo markdown o varios en pdf según el estilo de la DNDIP

    Convierte un archivo .md en .pdf
    `python md2pdf.py index.md docs/portal-andino-docs.pdf`

    Convierte varios archivos .md en un solo .pdf
    `python md2pdf.py index.md,sect1.md,sect2.md docs/portal-andino-docs.pdf`

    Convierte todas las secciones de un mkdocs.yml en un solo .pdf
    `python md2pdf.py mkdocs.yml docs/portal-andino-docs.pdf`

La documentación debe organizarse dentro de un repo en una carpeta "docs" que
contenga todos los markdowns.
"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os
import sys
import re
from pprint import pprint

import markdown
from unidecode import unidecode
import yaml
import pdfkit
import shutil
from bs4 import BeautifulSoup


def title_to_name(title, decode=True, max_len=None, use_complete_words=True):
    """Convierte un título en un nombre normalizado para generar urls."""
    # decodifica y pasa a minúsculas
    if decode:
        title = unidecode(title)
    title = title.lower()

    # remueve caracteres no permitidos
    filtered_title = re.sub(r'[^a-z0-9- ]+', '', title)

    # remueve stop words y espacios y une palabras sólo con un "-"
    normalized_title = '-'.join([word for word in filtered_title.split()])

    # recorto el titulo normalizado si excede la longitud máxima
    if max_len and len(normalized_title) > max_len:

        # busco la última palabra completa
        if use_complete_words:
            last_word_index = normalized_title.rindex("-", 0, max_len)
            normalized_title = normalized_title[:last_word_index]

        # corto en el último caracter
        else:
            normalized_title = normalized_title[:max_len]

    return normalized_title


def _parse_section_paths_from_nav(nav, docs_dir="docs"):
    """Genera una lista de los paths a los md de las secciones de un mkdocs.

    Nav de ejemplo en mkdocs.yml:

        nav:
          - Inicio: 'index.md'
          - Usuarios:
            - Comienzo rápido: 'quickstart.md'
          - Desarrolladores:
            - Instalación: 'developers/install.md'
            - Actualización: 'developers/update.md'

    Lista generada por este método:
        [
            'index.md'
            'quickstart.md'
            'developers/install.md'
            'developers/update.md'
        ]
    """
    section_paths = []
    for section in nav:
        for value in section.values():
            if isinstance(value, list):
                section_paths.extend(
                    _parse_section_paths_from_nav(value, docs_dir))
            else:
                section_paths.append(
                    os.path.join(docs_dir, value)
                )
    return section_paths


def _fix_images(html, abs_docs_path="./"):
    """Crea los links internos entre las secciones del mkdocs."""
    soup = BeautifulSoup(html, features="html.parser")

    for img in soup.find_all("img"):
        img["src"] = abs_docs_path + img["src"]

    return soup.prettify()


def _fix_section_anchor_links(html, markdown_paths):
    """Crea los links internos entre las secciones del mkdocs."""
    soup = BeautifulSoup(html, features="html.parser")

    # agrega ids a todos los headers del documento
    for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']):
        h["id"] = title_to_name(h.text)

    # cambia URL para los markdowns listados
    for a in soup.find_all("a"):
        if "docs/" + a["href"] in markdown_paths:
            a["href"] = "#" + title_to_name(a.text)

    return soup.prettify()


def main(input_paths_str, output_path):
    MKDOCS_DATOSGOBAR_ABS_PATH = os.path.abspath(os.path.dirname(__file__))
    ABS_DOCS_PATH = os.path.dirname(os.path.abspath(output_path)) + "/"
    PDF_CSS_PATH = os.path.join(
        MKDOCS_DATOSGOBAR_ABS_PATH, "datosgobar_docs/css/pdf.css")

    # chequea si se ha pasado un mkdocs.yml con las secciones para convertir
    if input_paths_str == "mkdocs.yml":
        with open(input_paths_str, "rb") as f:
            docs_options = yaml.load(f.read())
        input_paths = _parse_section_paths_from_nav(
            docs_options["nav"], docs_options.get("docs_dir", "docs"))
    # asume que se pasa una lista de paths separados por comas
    else:
        input_paths = input_paths_str.split(",")

    # lee los htmls a convertir en PDF
    htmls = []
    for input_path in input_paths:
        # sólo se procesa si es un markdown
        if input_path.split(".")[-1] == "md":
            with open(input_path) as input_file:
                htmls.append(markdown.markdown(
                    input_file.read(),
                    extensions=["fenced_code", "codehilite", "admonition"]))
    print("Hay {} documentos a convertir en un solo PDF.".format(len(htmls)))

    # guarda html
    with open(output_path.replace(".pdf", ".html"), "wb") as output_html:

        # aplica el estilo al principio
        html = "\n".join(htmls)
        html = _fix_section_anchor_links(html, input_paths)
        html_with_style = """
        <link rel="stylesheet" href="pdf.css" type="text/css"/>
        """ + html

        # escribe el html
        output_html.write(html_with_style.encode("utf-8"))
        shutil.copyfile(
            PDF_CSS_PATH,
            os.path.join(os.path.dirname(output_path), "pdf.css")
        )

    # corrige el html para el pdf
    html = _fix_images(html, ABS_DOCS_PATH)

    # guarda pdf
    pdfkit.from_string(html, output_path, options={"encoding": "utf8"},
                       css=PDF_CSS_PATH)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
