# Standard library imports
import os

# Third party imports
import opengeode


# Local application imports


def sum(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    return a / b


def string_upper(string="Hello world"):
    string_upper = string.upper()
    print(string_upper, flush=True)
    return string_upper


def load_brep(path):
    return opengeode.load_brep(path)
