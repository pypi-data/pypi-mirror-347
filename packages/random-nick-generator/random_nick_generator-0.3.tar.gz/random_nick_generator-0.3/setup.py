from setuptools import setup, find_packages

import os

def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name='random-nick-generator',
    version='0.3',
    packages=find_packages(),
    description='A simple library to generate random nicknames.',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='vsenikzianyati',
    author_email='fmsg4341@gmail.com',
    url='https://github.com/dsadasdasdsaas/random-nick-generator',
)