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
    module = __import__(name)
    return module
