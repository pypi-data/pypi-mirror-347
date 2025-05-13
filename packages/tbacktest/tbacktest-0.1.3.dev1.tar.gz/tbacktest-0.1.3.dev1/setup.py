# -*- coding: utf-8 -*-
"""
Created on Mon May 12 00:40:53 2025

@author: tts74
"""

from setuptools import setup, find_packages

setup(
    name='tbacktest',
    version='0.1.3.dev1',
    author='SteveTsai',
    author_email='tsunghsun0127@gmail.com',
    description='事件驅動式的 Python 金融投資工具回測套件',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TsungHsunTsai/T_BackTest',  # 可選
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)