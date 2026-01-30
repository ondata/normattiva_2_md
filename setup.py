#!/usr/bin/env python3
"""
Setup script per normattiva2md - Convertitore Akoma Ntoso to Markdown
"""

from setuptools import setup, find_packages
import os


# Leggi il contenuto del README se esiste
def read_readme():
    # Per il pacchetto akoma2md deprecato, usa il README specifico
    readme_path = os.path.join(os.path.dirname(__file__), "README_AKOMA2MD.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "⚠️ DEPRECATED: Use normattiva2md instead. | Convertitore da XML Akoma Ntoso a Markdown"


setup(
    name="normattiva2md",
    version="2.1.10",
    description="Convertitore da XML Akoma Ntoso a formato Markdown con download automatico delle leggi citate e cross-references inline (CLI: normattiva2md)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Andrea Borruso",
    author_email="aborruso@gmail.com",
    url="https://github.com/ondata/normattiva_2_md",
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
        "rich>=13.0.0,<14.0.0",
    ],
    # Pacchetti
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # Script da riga di comando
    entry_points={
        "console_scripts": [
            "normattiva2md=normattiva2md.cli:main",
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
