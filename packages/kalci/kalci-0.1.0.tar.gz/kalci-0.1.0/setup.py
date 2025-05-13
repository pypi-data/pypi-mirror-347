from setuptools import setup, find_packages
import codecs
import os

from pathlib import Path
this_directory = Path(__file__).parent

VERSION = '0.1.0'
DESCRIPTION = 'A CLI Calculator made in Python'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="kalci",
    version=VERSION,
    author="HussuBro010 (Hussain Vohra)",
    author_email="<hussainv2807@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['tabulate', 'sympy', 'typer', 'pryttier'],
    keywords=['python', 'calculator', 'science', 'algebra', 'calculus'],
)
