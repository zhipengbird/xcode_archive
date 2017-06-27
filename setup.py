#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/23 下午2:47
# @Author  : 袁平华
# @Site    : 
# @File    : setup.py
# @Software: PyCharm Community Edition

import os
from setuptools import setup, find_packages


def fread(fname):
    filepath = os.path.join (os.path.dirname (__file__), fname)
    with open (filepath, 'r') as fp:
        return fp.read ( )


setup (
    name='xcodearchive',
    version='1.4.6',
    description='A  xcode build and archive tools',
    keywords='xcode, build, archive ',
    url='https://github.com/zhipengbird/xcode_archive',
    author='yuanpinghua',
    author_email='yuanpinghua@yeah.net',
    license='MIT',
    packages=find_packages ( ),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    entry_points={
        'console_scripts': [
            'xcodearchive = xcodearchive.xcodetool:main'
        ]
    },
    # long_description=fread("README.md")

    # install_requires =['shutil'],
)
