# pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin\bin" --workpath ".\bin\build" --name youtusic --onefile --paths ".\spotify-env\Lib\site-packages" .\youtusic.py
# pyinstaller --noconfirm --log-level=WARN --clean --distpath "./bin/bin" --workpath "./bin/build" --name youtusic --onefile --paths "./spotify-env/Lib/site-packages" ./youtusic.py
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
from typing import NoReturn

from decouple import config

import youtusic


if hasattr(sys, '_MEIPASS'):
    # source: https://stackoverflow.com/a/66581062/19860022
    file_base_path = sys._MEIPASS
    # source: https://stackoverflow.com/a/36343459/19860022
else:
    file_base_path = os.path.dirname(__file__)


def main() -> NoReturn:
    '''
    The main function that handles passing or args and return values.
    Also handles the application loop and errors from functions
    '''

    try:
        API_USER = config('API_USER')
        API_PASS = config('API_PASS')
        
        try: 
            ...
        except youtusic.dnf:
            ...
    except KeyboardInterrupt:
        sys.exit(0)