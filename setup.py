#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 13:21
# @File    : setup.py
# @Author  : donghaixing
# Do have a faith in what you're doing.
# Make your life a story worth telling.

# Always prefer setuptools over distutils
from codecs import open
from os import path

from setuptools import setup

# To use a consistent encoding
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(here, 'VERSION'), encoding='utf-8') as f:
    version = f.read()
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip()
                    for line in f if
                    line.strip() and not line.strip().startswith('--') and not line.strip().startswith('#')]

data_files = []

cmdclass = {}
ext_modules = []

setup(
    name='pmeter',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,

    description='A Jmeter auto test tool.',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://github.com/ddong8/pmeter',

    # Author details
    author='donghaixing',
    author_email='donghaixing8@gmail.com',

    # Choose your license
    license='Apache License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable ',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License ',

        'Topic :: Software Development :: Libraries',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Operating System :: OS Independent'
    ],

    # What does your project relate to?
    keywords='Jmeter Auto_test Distributed',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['pmeter', 'pmeter.common', 'pmeter.core', 'pmeter.etc', 'pmeter.result'],

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requirements,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[testing]
    extras_require={'testing': ['pytest', 'pytest-runner', 'pytest-html', 'pytest-cov', 'pytest-mock']},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        '': ['*']
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=data_files,

    zip_safe=False,
    cmdclass=cmdclass,
    ext_modules=ext_modules,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'pmeter_admin=pmeter.common.command:execute_from_command_line',
        ],
    },
)
