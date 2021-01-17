#!/usr/bin/python3.6
# coding: utf8


# setup the aya package to directly call functions, e.g. src_telegram.core_bot
from setuptools import setup, find_packages

setup(
   name='aya',
   version='1.0',
   description='A package to work with aya',
   author='s0288',
   author_email='alex.gansmann@gmail.com',
   packages=find_packages()
)