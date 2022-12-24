# 
# -*- coding: UTF-8 -*-

# https://github.com/Cornelius-Figgle/youtusic/

'''
This file was authored by [edsq](https://github.com/edsq) on GitHub -
for more info please see the [corresponding discussion](https://github.com/tqdm/tqdm/discussions/1314#discussion-3994546)
THIS FILE IS PART OF THE `youtusic` REPO, MAINTAINED AND 
PRODUCED BY MAX HARRISON, AS OF 2022

It may work separately and independently of the main repo, it may not

 - Original Code (c) edsq 2022
 - Adaptation (c) Max Harrison 2022

'''

# note: view associated GitHub info as well
__version__ = 'Pre-release'  
__author__ = 'edsq'
__email__ = 'https://github.com/tqdm/tqdm/discussions/1314#discussion-3994546'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2022 edsq'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['edsq']


import curses


class _CursesIO:
    '''
    Class faking io.StringIO so we can print `tqdm.tqdm` output to a
    curses screen. `stdscr` is the `curses.window` object to write to

    ### Example

    ```python
    from CursesIO import _CursesIO

    height, width = stdscr.getmaxyx()
    curses_file = _CursesIO(stdscr=stdscr, y0=1, x0=0)

    for i in tqdm(range(100), file=curses_file, ascii=False, ncols=width):
        curses.napms(100)  # note: sleep for 100 ms
    ```
    '''

    def __init__(self, stdscr: curses.window, x0: int, y0: int) -> None:
        self.stdscr = stdscr
        self.x0 = x0
        self.y0 = y0

        self.buffer = ''  # The string to write

    def write(self, s: str) -> int:
        '''
        Replace `self.buffer` with `s` and return number of characters 'written'
        '''

        self.buffer = s
        return len(s)

    def flush(self) -> None:
        '''
        Print `self.buffer` to `self.stdscr` and clear buffer contents
        '''

        self.stdscr.addstr(self.y0, self.x0, self.buffer)
        self.stdscr.refresh()
        self.buffer = ''
