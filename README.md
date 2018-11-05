# mkdocs-datosgobar
Repositorio de temas de documentación de datosgobar para mkdocs.

## Desarrollo

Para ver la documentación y hacer cambios en vivo: `mkdocs serve`

Para buildear la documentación y pusherar a Github: `mkdocs build`

## Instalación

`pip install mkdocs-datosgobar`

## Uso

1. Crear directorio `docs` donde poner las secciones de la documentación escritas en archivos `.md` (markdown)
2. Crear archivo `mkdocs.yml` en el directorio raíz (seguir el [ejemplo de este repo](mkdocs.yml))

### Generar PDFs

Si se desea generar la versión en PDF de un archivo markdown, se puede usar el módulo `md2pdf.py`.

1. Crear archivo `docs/css/pdf.css` donde se establecerán los estilos.
2. Crear directorio `docs/pdf` donde se pondrán las versiones en PDF.
3. Correr `python md2pdf.py docs/guia_metadatos.md docs/pdf/guia_metadatos.pdf` desde la línea de comandos.
