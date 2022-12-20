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

from decouple import config
from num2words import num2words

from youtusic import Youtusic_, dnf


if hasattr(sys, '_MEIPASS'):
    # source: https://stackoverflow.com/a/66581062/19860022
    file_base_path = sys._MEIPASS
    # source: https://stackoverflow.com/a/36343459/19860022
else:
    file_base_path = os.path.dirname(__file__)


def get_response(question: str, answers: list=None) -> int | str:
    '''
    Function for repeatedly asking the same question until a valid
    answer is found

    - `question` is the full question to be asked (including any escape
    characters for nice input)
    - `answers` is an optional `2D` list with each outcome in the first
    dimension, and variations on the input of this in the second
    - `answers` should be in all lowercase
    - In addition to the passed `answers`, numbers (starting index `1`)
    and their cardinal forms will be considered as valid responses
    - Returns the option number of the chosen answer (starting 
    index `0`)
    - If `answers` is not provided, `responses` will be returned if it
    is not `None`

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
        elif answers:
            for i in range(len(answers)):
                if (response in answers[i]) or (response in [str(i+1), num2words(i+1)]):
                    return i
            print('Error in answer - please try again')
            continue
        else:
            return response

def main() -> NoReturn:
    '''
    The main function that handles passing or args and return values.
    Also handles the application loop and errors from functions
    '''
    print('start')

    try:
        

        playlist_provider = get_response(
            'Playlist type? 1: Spotify, 2: YouTube \n> ', 
            [
                ['spotify', 'sp'], 
                ['youtube', 'yt']
            ]
        )

        playlist_uri = get_response(
            'Playlist URL? \n> '
        )
        
        if playlist_provider == 0:  # note: If using a Spotify playlist
            obj = Youtusic_(
                API_USER=config('API_USER'),
                API_PASS=config('API_PASS')
            )

            track_list = obj.sp_get_tracks(playlist_uri)
            url_list = obj.grab_yt_links(track_list)

            dwld_args = [url_list]

        elif playlist_provider == 1:  # note: If using a YouTube playlist
            obj = Youtusic_()  # note: no keys
            url_list = [playlist_uri, True]  # note: use yt playlist instead
        
        obj.dwld_playlists(*dwld_args)
        
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__': 
    main()