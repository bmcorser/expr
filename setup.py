import re
import os
import sys

from setuptools import setup
from setuptools.command.test import test


class pytest_(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def dunder(name):
    path_components = os.path.dirname(__file__), 'expr', '__init__.py'
    with open(os.path.join(*path_components)) as initpy:
        return (re.compile(r".*{0} = '(.*?)'".format(name), re.S)
                  .match(initpy.read()).group(1))

setup_kwargs = {
    'author': 'bmcorser',
    'author_email': 'bmcorser@gmail.com',
    'url': 'https://github.com/bmcorser/expr',
    'name': 'expr',
    'packages': ['expr'],
    'install_requires': ['pydot'],
    'version': dunder('__version__'),
    'tests_require': ['pytest'],
    'long_description': open('README.rst', 'r').read(),
    'cmdclass': {
        'test': pytest_,
    },
}
setup(**setup_kwargs)
