#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 定义依赖，不包含火山引擎SDK
requirements = [
    'pyyaml>=6.0',
    'tqdm>=4.64.0',
    'colorama>=0.4.4'
]

setup(
    name='ecsbatchcli',
    version='0.1.0',
    description='A CLI tool for batch management of Volcano Engine ECS instances',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Volcano Engine Team',
    author_email='support@volcengine.com',
    url='https://github.com/volcengine/ecsbatchcli',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ecsbatchcli=ecsbatchcli.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Systems Administration',
    ],
    python_requires='>=3.6',
)
