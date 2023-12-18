# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

# source: https://github.com/Cornelius-Figgle/youtusic/

'''
Entry point for execution as a module
'''

'''
THIS FILE IS PART OF THE `youtusic` REPO, MAINTAINED AND 
PRODUCED BY MAX HARRISON, AS OF 2023

It may work separately and independently of the main repo, it may not

 - Code (c) Max Harrison 2023
'''

__version__ = '2.0.0'  
__author__ = 'Cornelius-Figgle'
__email__ = 'max@fullimage.net'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2023 Max Harrison'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['Max Harrison', 'edsq']


from curses import wrapper

from youtusic.tui import main


if __name__ == '__main__': 
    wrapper(main)  # start curses application
