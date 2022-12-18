# 
# -*- coding: UTF-8 -*-

# https://github.com/Cornelius-Figgle/youtusic/

'''
THIS FILE IS PART OF THE `youtusic` REPO, MAINTAINED AND 
PRODUCED BY MAX HARRISON, AS OF 2022

It may work separately and independently of the main repo, it may not

 - Code (c) Max Harrison 2022

'''

# note: view associated GitHub info as well
__version__ = 'Pre-release'  
__author__ = 'Cornelius-Figgle'
__email__ = 'max@fullimage.net'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2022 Max Harrison'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['Max Harrison']


import os
import sys
from contextlib import contextmanager
from io import BytesIO


if hasattr(sys, '_MEIPASS'):
    # source: https://stackoverflow.com/a/66581062/19860022
    file_base_path = sys._MEIPASS
    # source: https://stackoverflow.com/a/36343459/19860022
else:
    file_base_path = os.path.dirname(__file__)

@contextmanager
def no_stdout() -> None:
    '''
    Silences the `sys.stdout` of a function call 
    
    [Credit here](https://stackoverflow.com/a/2829036/19860022)

    Example:
    ```
    with no_stdout():
        do_something_noisily()
    ```
    '''

    save_stdout = sys.stdout
    sys.stdout = BytesIO()
    yield
    sys.stdout = save_stdout

class dnf(Exception):
    '''
    Exception class for error handling

    did not complete but exited fine
    '''
    ...