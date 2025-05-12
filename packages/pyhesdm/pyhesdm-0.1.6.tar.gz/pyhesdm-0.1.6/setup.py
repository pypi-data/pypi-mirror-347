from setuptools import setup, find_packages
from setuptools.command.install import install
import urllib.request
import os

setup(
    name='pyhesdm',
    version='0.1.6',
    description='Local Universe Dispersion Measure Model Computed from HESTIA Simulation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yuxin Huang, Khee-Gan Lee, Noam Libeskind, Sunil Simha, Aurélien Valade and J. X. Prochaska',
    author_email='mochafhxy@gmail.com',
    url='https://github.com/yuxinhuang1229/pyhesdm',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'pyhesdm': ['*.csv']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        'ne2001==0.0.1',
        'dust_extinction==1.5',
        'linetools==0.3.2',
        'mwprop==1.0.10',
        'importlib_resources',
        'healpy==1.17.3'
    ]
)