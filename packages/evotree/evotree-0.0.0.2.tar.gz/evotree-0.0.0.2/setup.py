#!/usr/bin/python3.8
# contact: heche@psb.vib-ugent.be

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='evotree',
    version='0.0.0.2',
    packages=['evotree'],
    url='http://github.com/heche-psb/evotree',
    license='GPL',
    author='Hengchi Chen',
    author_email='heche@psb.vib-ugent.be',
    description='Python package and CLI for processing phylogenetic tree',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['command'],
    include_package_data=True,
    install_requires=[
       'biopython>=1.76',
       'click>=7.1.2',
       'pandas>=1.4.4',
       'numpy>=1.19.0',
       'rich>=12.5.1',
       'matplotlib>=3.2.2',
       'scipy>=1.10.1',
       'statsmodels>=0.14.1',
       'tqdm>=4.64.1',
       'pymc>=5.6.1',
       'arviz>=0.15.1',
       'pytensor>=2.12.3'
    ],
    entry_points='''
        [console_scripts]
        evotree=command:cli
    ''',
)
