import os
from setuptools import setup, find_packages
f = open('README.rst')

long_description = f.read().strip()
long_description = long_description.split('readme', 1)[1]
f.close()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='icaltask',
    version='0.0.1',
    author='Aerex',
    author_email='aerex@aerex.me',
    description=('A taskwarrior hook to import tasks as vtodo calendar events'),
    keywords='taskwarrior, hooks, iCal',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['vobject', 'requests'],
    long_description=read('README.rst'),
    tests_require=[
        "pytest_mock",
        "pytest",
        "mock"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        ],
    )
