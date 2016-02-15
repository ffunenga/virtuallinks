import sys
import os
import shutil


def import_package(name):
    _filepath = os.path.abspath(__file__)
    path = backup = os.path.dirname(_filepath)
    while os.path.basename(path) != name:
        path = os.path.join(path, '..')
        path = os.path.abspath(path)
    if path != backup:
        sys.path.insert(0, path)
    return __import__(name)


def generate_numbers():
    for i in range(10):
        yield i
