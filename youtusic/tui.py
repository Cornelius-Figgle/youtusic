# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

# source: https://github.com/Cornelius-Figgle/youtusic/

'''
    
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


import curses
import os
import sys
from typing import NoReturn

from pick import pick  # install from my fork

from youtusic.config import generate_final_config
from youtusic.main import Youtusic_


def main(stdscr: curses.window) -> NoReturn:
    '''
    The main function that controls the TUI for Youtusic. Called by __main__        
    '''

    # load our configuration, from arg line & TOML file
    user_config = generate_final_config(sys.argv)

    # sets up curses stdscr
    curses.echo()
    curses.curs_set(0)
    curses.use_default_colors()

    # for debugging
    stdscr.addstr(f'Using config:\n{str(user_config)}\n')
    stdscr.addstr('\nPress any key if this is correct, or Ctrl-C to abort')
    stdscr.get_wch()

    # initialise the main class
    obj = Youtusic_(user_config=user_config)
