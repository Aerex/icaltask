import os
from setuptools import setup, find_packages
f = open('README.rst')

#long_description = f.read().strip()
#long_description = long_description.split('split here', 1)[1]
f.close()



setup(
    name='icaltask',
    version='0.0.1',
    author='Aerex',
    author_email='aerex@aerex.me',
    description=('Synchronize between Taskwarrior and iCalendar TODO events'),
    long_description=open('README.rst').read(),
    keywords='taskwarrior, ical, task-management',
    url='https://github.com/Aerex/icaltask',
    data_files=[('', ['icaltaskrc'])],
    packages=find_packages(include=['icaltask']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['vobject', 'requests', 'tzlocal', 'requests_toolbelt'],
    tests_require=[
        "pytest_mock",
        "pytest",
        "mock"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
        ],
    entry_points='''
    [console_scripts]
    icaltask=icaltask.cli:main
    '''
    )
