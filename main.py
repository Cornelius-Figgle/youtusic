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


import curses
import os
from typing import NoReturn

from decouple import UndefinedValueError, config
from num2words import num2words
from pick import pick  # note: `pip install git+https://github.com/Cornelius-Figgle/pick.git@master` until PR is merged

from youtusic import Youtusic_


def get_response(question: str, answers: list=None) -> int | str:
    '''
    Function for repeatedly asking the same question until a valid
    answer is found (only to be used when not in `curses`, use 
    `pick.pick()` instead when running with `curses`)

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

def main(screen: curses.window) -> NoReturn:
    '''
    The main function that handles passing or args and return values.
    Also handles the application loop and errors from functions
    '''

    try:
        curses.echo()
        curses.curs_set(0)

        try:
            youtusic_args = {
                'API_USER': config('SPOTIPY_CLIENT_ID'),
                'API_PASS': config('SPOTIPY_CLIENT_SECRET'),
                'use_curses': True,
                'stdscr': screen
            }
        except UndefinedValueError:
            youtusic_args = {
                'use_curses': True,
                'stdscr': screen
            }

        obj = Youtusic_(**youtusic_args)

        for line in obj.title:
            screen.addstr(line)
        
        y_, _ = screen.getyx()
        playlist_provider_name, _ = pick(
            ['Spotify', 'Youtube'], 
            '\nPlaylist type?',
            screen=screen,
            position={'y0': y_, 'x0': 0},
            indicator='>'
        )

        screen.addstr('\nPlaylist URL? \n> ') ; screen.refresh()
        playlist_uri = str(screen.getstr())

        if playlist_provider_name == 'Spotify':
            # note: for Spotify playlist
            track_list = obj.sp_get_tracks(playlist_uri)
            url_list = obj.grab_yt_links(track_list)

        elif playlist_provider_name == 'Youtube':
            ...
        
        def check_path() -> tuple[False, None] | tuple[True, str]:
            screen.addstr('\nDownload Folder? \n> ') ; screen.refresh()
            dwld_path = os.path.abspath(screen.getstr().decode('utf-8'))

            def _confirm_correct(dwld_path: str) -> tuple[True, str] | tuple[False, None]:
                y_, _ = screen.getyx()
                confirm, _ = pick(
                    ['Yes', 'No'], 
                    f'\nIs This Path Correct? \t{dwld_path}',
                    screen=screen,
                    position={'y0': y_, 'x0': 0},
                    indicator='>'
                )
                        
                if confirm == 'Yes':
                    return True, dwld_path
                else:
                    return False, None

            if not os.access(dwld_path, os.X_OK | os.W_OK):
                if not os.access(os.path.dirname(dwld_path), os.X_OK | os.W_OK):
                    screen.addstr('\nSorry, invalid path. If path is relative, please prefix with "./" or ".\\"')
                    return False, None
                else:
                    y_, _ = screen.getyx()
                    confirm, _ = pick(
                        ['Yes', 'No'], 
                        f'\nDo You Wish To Create Child Folder "{os.path.basename(os.path.normpath(dwld_path))}" In Parent "{os.path.dirname(dwld_path)}"?',
                        screen=screen,
                        position={'y0': y_, 'x0': 0},
                        indicator='>'
                    )

                    if confirm != 'Yes':
                        return False, None

            return _confirm_correct(dwld_path)    

        while True:
            valid, dwld_path = check_path()
            if not valid:
                continue
            if valid:
                break
        
        ret_code = obj.dwld_playlists(url_list, dwld_path)
        obj.process_files(url_list, track_list, dwld_path)

        screen.addstr(f'Complete! Files can be found at "{dwld_path}"')
        screen.get_wch()
        
    except KeyboardInterrupt:
        pass

if __name__ == '__main__': 
    curses.wrapper(main)