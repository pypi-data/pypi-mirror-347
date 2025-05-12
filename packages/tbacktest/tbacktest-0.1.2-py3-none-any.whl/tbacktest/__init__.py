# -*- coding: utf-8 -*-
"""
Created on Fri May  9 23:04:45 2025

@author: tts74
"""
'''
1. __init__.py

 __init__.py 是 Python 中用來標示某個資料夾是「package」的檔案
 使資料夾變成 Python 模組套件
 沒有 __init__.py，Python 不會把這個資料夾當成一個可導入（import）的 package。
 
 舉例說明： 
    mypackage/
    ├── __init__.py   ← 這個檔案的存在，讓 mypackage 可以被 import
    └── module.py
    
    使用方式 (如果__init__.py裡面空空如也)：
    from mypackage import module
    
    如果有寫  from .module import class(如本範例的例子，如下面code，則寫了之後會變成:
    from mypackage import class


2. 當你使用 import mypackage 時，__init__.py 裡面的程式碼會自動執行。
'''

