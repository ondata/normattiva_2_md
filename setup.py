#!/usr/bin/env python3
"""
Setup script per normattiva2md - Convertitore Akoma Ntoso to Markdown
"""

from setuptools import setup, find_packages
import os

# Leggi il contenuto del README se esiste
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Convertitore da XML Akoma Ntoso a Markdown"

setup(
    name="akoma2md",
    version="2.0.14",
    description="Convertitore da XML Akoma Ntoso a formato Markdown con download automatico delle leggi citate e cross-references inline (CLI: normattiva2md)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Andrea Borruso",
    author_email="aborruso@gmail.com",
    url="https://github.com/aborruso/normattiva_2_md",

    # Classificatori per PyPI
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: Markup",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    # Dipendenze
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],

    # Moduli Python
    py_modules=["convert_akomantoso"],

    # Script da riga di comando
    entry_points={
        "console_scripts": [
            "akoma2md=convert_akomantoso:main",
            "normattiva2md=convert_akomantoso:main",
        ],
    },

    # Parole chiave per la ricerca
    keywords="akoma ntoso xml markdown converter legal documents",

    # Licenza
    license="MIT",

    # Include file aggiuntivi
    include_package_data=True,
    zip_safe=False,
)
