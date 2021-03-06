""" Test the cpp-lib Cookiecutter template.

A template project is created in a temporary directory, the library and its
test suite are built, and the test suite is executed.

"""
from contextlib import contextmanager
from json import load
from os import chdir
from os import getcwd
from os.path import abspath
from os.path import dirname
from os.path import join
from shlex import split
from shutil import rmtree
from subprocess import check_call
from tempfile import mkdtemp

from cookiecutter.main import cookiecutter

from glob import glob

def main():
    """ Execute the test.
    
    """
    @contextmanager
    def tmpdir():
        """ Enter a self-deleting temporary directory. """
        cwd = getcwd()
        tmp = mkdtemp()
        try:
            chdir(tmp)
            yield tmp
        finally:
            rmtree(tmp)
            chdir(cwd)
        return

    template = dirname(dirname(abspath(__file__)))
    defaults = load(open(join(template, "cookiecutter.json")))
    with tmpdir():
        cookiecutter(template, no_input=True)
        chdir(defaults["project_name"])
        check_call(split("cmake -DCMAKE_BUILD_TYPE=Debug"))
        check_call(split("cmake --build ."))
        check_call(split(join("test", "test_hello")))
    return 0
    
    
# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
