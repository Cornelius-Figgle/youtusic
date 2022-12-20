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


import curses
import os
import sys
from contextlib import contextmanager
from io import BytesIO
from re import findall
from urllib import parse
from urllib.request import Request, urlopen

import yt_dlp
from spotipy import Spotify as Spotipy_
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

from CursesIO import _CursesIO


if hasattr(sys, '_MEIPASS'):
    # source: https://stackoverflow.com/a/66581062/19860022
    _file_base_path = sys._MEIPASS
    # source: https://stackoverflow.com/a/36343459/19860022
else:
    _file_base_path = os.path.dirname(__file__)

@contextmanager
def no_stdout() -> None:
    '''
    Silences the `sys.stdout` of a function call 
    
    [Credit here](https://stackoverflow.com/a/2829036/19860022)

    ### Example:
    
    ```python
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


class Youtusic_(object):
    '''
    Main class for `youtusic` module
    '''

    def __init__(self, *args: object, 
        API_USER: str=None, API_PASS: str=None,
        stdscr: curses.window) -> None:

        super().__init__(*args)

        self._illegalChars = [
            '/', '\\', ':', 
            '*', '?', '"', 
            '<', '>', '|'
        ]

        if API_USER is not None and API_PASS is not None:  # note: if provided
            self.sp = Spotipy_(
                client_credentials_manager=SpotifyClientCredentials(
                    client_id=API_USER, client_secret=API_PASS
                )
            )

        self.stdscr = stdscr

    def sp_get_tracks(self, playlist_link: str) -> list:
        '''
        Uses [spotipy](https://pypi.org/project/spotipy/) to retrieve
        a list of songs in the playlist provided. Returns a list to be
        used with `grab_yt_links`
        '''

        playlist_uri = playlist_link.split('/')[-1].split('?')[0]
        song_titles = []

        self.height, self.width = self.stdscr.getmaxyx()
        y_, x_ = self.stdscr.getyx()
        self.curses_file = _CursesIO(stdscr=self.stdscr, y0=y_+1, x0=0)

        for song in tqdm(
            self.sp.playlist_tracks(playlist_uri)['items'], 
            desc='Listing songs...',
            file=self.curses_file, ascii=False, ncols=self.width):

            track_name: str = song['track']['name']
            artist_name: str = song['track']['artists'][0]['name']

            track_name = track_name.replace(' ', '+')
            artist_name = artist_name.replace(' ', '+')
            
            song_titles.append(f'{artist_name}+{track_name}')

        return song_titles

    def grab_yt_links(self, song_titles: str) -> list:
        '''
        Parses the list returned by `sp_get_tracks` and returns a 
        list of YouTube URLs to use for `dwld_playlists`
        '''

        yt_links = []

        self.height, self.width = self.stdscr.getmaxyx()
        y_, x_ = self.stdscr.getyx()
        self.curses_file = _CursesIO(stdscr=self.stdscr, y0=y_+1, x0=0)

        for song in tqdm(
            song_titles, 
            desc='Listing URLs...',
            file=self.curses_file, ascii=False, ncols=self.width):

            html_parsed_song_title = parse.quote(str(song), safe='')
            url = Request(
                f'https://www.youtube.com/results?search_query={html_parsed_song_title}',
                headers = {'User-Agent': 'Mozilla/5.0'}
            )

            html_resp = urlopen(url)
            video_ids = findall(r'watch\?v=(\S{11})', html_resp.read().decode())

            yt_links.append(f'https://www.youtube.com/watch?v={video_ids[0]}')
            # note: uses first found link
            # future: might add preview window?
        
        return yt_links

    def dwld_playlists(self, yt_links: list, use_playlist: bool=False):
        ...

        # https://github.com/yt-dlp/yt-dlp#extract-audio