"""
Module providing custom shapes for diagram generation.
"""

from os import path

from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja_environment = Environment(
    loader=FileSystemLoader(
        [path.join(path.dirname(__file__), "icons"), path.join(path.dirname(__file__), "shapes")]
    ),
    autoescape=select_autoescape(),
)
