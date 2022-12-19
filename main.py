# pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin\bin" --workpath ".\bin\build" --name youtusic --onefile --paths ".\spotify-env\Lib\site-packages" .\main.py
# pyinstaller --noconfirm --log-level=WARN --clean --distpath "./bin/bin" --workpath "./bin/build" --name youtusic --onefile --paths "./spotify-env/Lib/site-packages" ./main.py
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

from decouple import UndefinedValueError, config
from num2words import num2words

from youtusic import Youtusic, dnf


if hasattr(sys, '_MEIPASS'):
    # source: https://stackoverflow.com/a/66581062/19860022
    file_base_path = sys._MEIPASS
    # source: https://stackoverflow.com/a/36343459/19860022
else:
    file_base_path = os.path.dirname(__file__)


def get_response(question: str, answers: list=None) -> int:
    '''
    Function for repeatedly asking the same question until a valid
    answer is found

    - `question` is the full question to be asked (including any escape
    characters for nice input)
    - `answers` is a `2D` list with each outcome in the first
    dimension, and variations on the input of this in the second
    - `answers` should be in all lowercase
    - In addition to the passed `answers`, numbers (starting index `1`)
    and their cardinal forms will be considered as valid responses
    - Returns the option number of the chosen answer (starting 
    index `0`)

    ### Example:

    ```python
    answer = get_response(
        'Which program? 1: Spotify, 2: YouTube \\n> ',
        [
            ['spotify', 'sp'],
            ['youtube', 'yt']
        ]
    )
    ```
    '''

    while True:
        response = input(question).lower()
        if response is None: 
            print('Error in answer - please try again')
            continue
        if answers:
            for i in range(len(answers)):
                if (response in answers[i]) or (response in [str(i), num2words(i)]):
                    return i
            print('Error in answer - please try again')
            continue

def main() -> NoReturn:
    '''
    The main function that handles passing or args and return values.
    Also handles the application loop and errors from functions
    '''

    try:
        try:
            obj = Youtusic(
                API_USER=config('API_USER'), 
                API_PASS=config('API_PASS')
            )
        except UndefinedValueError:
            obj = Youtusic()

        resp = get_response(
            'Playlist type? 1: Spotify, 2: YouTube \n> ', 
            [
                ['spotify', 'sp'],
                ['youtube', 'yt']
            ]
        )

        if resp is 0:
            playlist_uri = get_response(
                'Playlist URL? \n>'
            )
            obj.sp_get_tracks(playlist_uri)
        
    except KeyboardInterrupt:
        sys.exit(0)