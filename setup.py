import os
import shutil
import sys
import setuptools
from setuptools.command.test import test as TestCommand


PACKAGE_NAME = 'virtuallinks'


if 'reset' in sys.argv[1:]:
    shutil.rmtree('env', ignore_errors=True)
    sys.argv = [('clean' if a == 'reset' else a) for a in sys.argv]


if 'clean' in sys.argv[1:]:
    shutil.rmtree('%s.egg-info' % PACKAGE_NAME, ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('.tox', ignore_errors=True)
    shutil.rmtree('.cache', ignore_errors=True)
    shutil.rmtree('.eggs', ignore_errors=True)
    for root, drs, fns in os.walk('.'):
        pycache = os.path.join(root, '__pycache__')
        shutil.rmtree(pycache, ignore_errors=True)
        filtered_fns = filter(lambda f: f.endswith('.pyc'), fns)
        for fn in filtered_fns:
            _fn = os.path.join(root, fn)
            os.remove(_fn)
    sys.exit()


class PyTest(TestCommand):

    def run_tests(self):
        import pytest
        errno = pytest.main('-v tests')
        sys.exit(errno)


def get_long_description(fname='README.rst'):
    try:
        with open(fname) as f:
            content = f.read()
    except:
        content = ''
    else:
        ini = content.find('    Why')
        content = content[ini:]
    return content


package = __import__(PACKAGE_NAME)


setuptools.setup(
    name=package.__name__,
    version=package.__version__,
    author=package.__author__,
    license=package.__license__,
    description=package.__description__,
    long_description=get_long_description(),
    author_email='fmafunenga@gmail.com',
    url='https://github.com/ffunenga/%s' % package.__name__,
    packages=[package.__name__],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
)
