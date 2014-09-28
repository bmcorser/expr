import re
import os
import sys
import subprocess

from setuptools import setup
from setuptools.command.test import test
from setuptools.command.sdist import sdist

import pandoc
pandoc.core.PANDOC_PATH = subprocess.check_output(['which', 'pandoc']).strip()


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


class pandoc_sdist(sdist):

    def run(self):
        sdist.run(self)  # note this isn't `super` :(


def dunder(name):
    path_components = os.path.dirname(__file__), 'expr_graph', '__init__.py'
    with open(os.path.join(*path_components)) as initpy:
        return (re.compile(r".*{0} = '(.*?)'".format(name), re.S)
                  .match(initpy.read()).group(1))

doc = pandoc.Document()
with open('README.md') as README_md:
    doc.markdown = README_md.read()
with open('README.rst', 'w+') as README_rst:
    README_rst.write(doc.rst)
print('Created README.rst')
setup_kwargs = {
    'author': 'bmcorser',
    'author_email': 'bmcorser@gmail.com',
    'url': 'https://github.com/bmcorser/expr-graph',
    'name': 'expr-graph',
    'packages': ['expr_graph'],
    'install_requires': ['pydot'],
    'version': dunder('__version__'),
    'tests_require': ['pytest'],
    'long_description': open('README.rst', 'r').read(),
    'cmdclass': {
        'test': pytest_,
        'sdist': pandoc_sdist,
    },
}
setup(**setup_kwargs)
os.unlink(README_rst.name)
print('Deleted README.rst')
