import re
import os
from setuptools import setup
import sys
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def dunder(name):
    path_components = os.path.dirname(__file__), 'expr_graph', '__init__.py'
    with open(os.path.join(*path_components)) as initpy:
        return (re.compile(r".*{0} = '(.*?)'".format(name), re.S)
                  .match(initpy.read()).group(1))

setup_kwargs = {
    'author': dunder('__author__'),
    'name': 'expression graph',
    'packages': ['expr_graph'],
    'install_requires': ['pydot'],
    'version': dunder('__version__'),
    'tests_require': ['pytest'],
    'cmdclass': {'test': PyTest},
}
setup(**setup_kwargs)
