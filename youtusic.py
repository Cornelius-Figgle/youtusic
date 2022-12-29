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


import csv
import curses
import os
from re import findall
from string import Template
from urllib import parse
from urllib.request import Request, urlopen

import yt_dlp
from moviepy.editor import VideoFileClip
from pytube import YouTube
from requests.exceptions import ConnectionError
from spotipy import Spotify as Spotipy_
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError
from tqdm import tqdm

from CursesIO import _CursesIO


class Youtusic_:
    '''
    Main class for `youtusic` module
    '''

    def __init__(
        self, API_USER: str=None, API_PASS: str=None, 
        use_curses: bool=True, stdscr: curses.window=None) -> None:

        self.title = [
            ' __     __         _             _      \n',
            ' \ \   / /        | |           (_)     \n',
            '  \ \_/ /__  _   _| |_ _   _ ___ _  ___ \n',
            '   \   / _ \| | | | __| | | / __| |/ __|\n',
            '    | | (_) | |_| | |_| |_| \__ \ | (__ \n',
            '    |_|\___/ \__,_|\__|\__,_|___/_|\___|\n',
            '========================================\n'
        ]

        self.illegal_chars = [
            '/', '\\', ':', 
            '*', '?', '"', 
            '<', '>', '|'
        ]

        if API_USER is not None and API_PASS is not None:
            # note: if provided
            client_auth = {
                'client_id': API_USER, 
                'client_secret': API_PASS
            }
        else:
            client_auth = {}
            # note: `spotipy` will handle env vars 
            # future: add a prompt?

        try:
            self.sp = Spotipy_(
            client_credentials_manager=SpotifyClientCredentials(
                **client_auth
                )
            )

            self.sp_available = True
        except SpotifyOauthError:
            self.sp_available = False

        self.use_curses = use_curses
        self.stdscr = stdscr

    def sp_get_tracks(self, playlist_link: str) -> list:
        '''
        Uses [spotipy](https://pypi.org/project/spotipy/) to retrieve
        a list of songs in the playlist provided. Returns a list to be
        used with `grab_yt_links`
        '''

        playlist_uri = playlist_link.split('/')[-1].split('?')[0]
        song_titles = []

        if self.use_curses:
            self.height, self.width = self.stdscr.getmaxyx()
            y_, _ = self.stdscr.getyx() ; del _
            self.curses_file = _CursesIO(stdscr=self.stdscr, y0=y_+1, x0=0)

            tqdm_args = {
                'desc': 'Listing songs...',
                'file': self.curses_file, 
                'ascii': False, 
                'ncols': self.width
            }
        else:
            tqdm_args = {
                'desc': 'Listing songs...'
            }

        api_response = self.sp.playlist_items(playlist_uri)['items']
        # future: `requests.exceptions.ConnectionError`

        for song in tqdm(api_response, **tqdm_args):
            track_name: str = song['track']['name']
            artist_name: str = song['track']['artists'][0]['name']
            
            song_titles.append(
                {
                    'artist': artist_name,
                    'title': track_name
                }
            )

        return song_titles
    
    def csv_get_tracks(self, file_path: str) -> list:
        '''
        Uses `csv` to retrieve a list of songs from `file_path` 
        provided. Returns a list to be used with `grab_yt_links`
        '''

        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            csv_content = list(reader)

        song_titles = []

        if self.use_curses:
            self.height, self.width = self.stdscr.getmaxyx()
            y_, _ = self.stdscr.getyx() ; del _
            self.curses_file = _CursesIO(stdscr=self.stdscr, y0=y_+1, x0=0)

            tqdm_args = {
                'desc': 'Listing songs...',
                'file': self.curses_file, 
                'ascii': False, 
                'ncols': self.width
            }
        else:
            tqdm_args = {
                'desc': 'Listing songs...'
            }

        for song in tqdm(csv_content, **tqdm_args):
            track_name: str = song[1]
            artist_name: str = song[0]
            
            song_titles.append(
                {
                    'artist': artist_name,
                    'title': track_name
                }
            )

        return song_titles

    def grab_yt_links(self, song_titles: list) -> list:
        '''
        Parses the list returned by `sp_get_tracks` and returns a 
        list of YouTube URLs to use for `dwld_playlists`
        '''

        yt_links = []

        if self.use_curses:
            self.height, self.width = self.stdscr.getmaxyx()
            y_, _ = self.stdscr.getyx() ; del _
            self.curses_file = _CursesIO(stdscr=self.stdscr, y0=y_+1, x0=0)

            tqdm_args = {
                'desc': 'Listing URLs...',
                'file': self.curses_file, 
                'ascii': False, 
                'ncols': self.width
            }
        else:
            tqdm_args = {
                'desc': 'Listing URLs...'
            }

        for song in tqdm(song_titles, **tqdm_args):
            song_artist = song['artist'].replace(' ', '+')
            song_title = song['title'].replace(' ', '+')
            song_name = f'{song_artist}+-+{song_title}'
            # note: constructs search phrase

            html_parsed_song_title = parse.quote(str(song_name), safe='')
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

    def dwld_playlists(self, yt_links: list, dwld_path: str) -> dict:
        '''
        Wrapper for `yt_dlp.YoutubeDL`. Passes URLs `yt_links` one at a
        time (just to make my own progress bar). Returns a dictionary
        of any videos that raised an error, with the title of the video
        as the key
        '''

        ydl_opts = {
            'paths': {'home': dwld_path},
            'quiet': True,
            'noprogress': False,
            'format': 'mp4/bestaudio/best',
            'outtmpl': {'default': '%(id)s.%(ext)s'},
            # note: See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            #'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a',}]   # note: Extract audio using ffmpeg
        }

        if self.use_curses:
            self.height, self.width = self.stdscr.getmaxyx()
            y_, _ = self.stdscr.getyx()
            self.curses_file = _CursesIO(stdscr=self.stdscr, y0=y_+1, x0=0)

            tqdm_args = {
                'desc': 'Downloading Videos...',
                'file': self.curses_file, 
                'ascii': False, 
                'ncols': self.width
            }
        else:
            tqdm_args = {
                'desc': 'Downloading Videos...'
            }

        error_codes = {}

        for video_url in tqdm(yt_links, **tqdm_args):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download([video_url])
            if error_code != 0:
                video_title = YouTube(video_url).title
                error_codes[video_title] = error_code
        
        return error_codes

    def process_files(
        self, yt_links: list, song_titles: list, dwld_path: str,
        rename_pattern: Template=Template('${artist} - ${title}')) -> None:
        '''
        Loops over all matching files in `dwld_path` and converts to 
        MP3. Will rename to match `rename_pattern` (a `string.Template`
        object) from `spotipy` info if `self.sp_available` is True, 
        will use `YouTube` video titles if there is no Spotify
        '''

        if self.use_curses:
            self.height, self.width = self.stdscr.getmaxyx()
            y_, _ = self.stdscr.getyx() ; del _
            self.curses_file = _CursesIO(stdscr=self.stdscr, y0=y_+1, x0=0)

            tqdm_args = {
                'desc': 'Converting Files...',
                'file': self.curses_file, 
                'ascii': False, 
                'ncols': self.width
            }
        else:
            tqdm_args = {
                'desc': 'Converting Files...'
            }

        for video_url in tqdm(yt_links, **tqdm_args):
            yt = YouTube(video_url)
            video_title = yt.title
            video_id = str(yt)[-12:-1]

            video_title_path = os.path.join(
                dwld_path,
                f'{video_id}.mp4'
            )

            if self.sp_available:
                song_info = song_titles[yt_links.index(video_url)]
                track_name = rename_pattern.substitute(
                    artist=song_info['artist'], 
                    title=song_info['title']
                )
            else:
                track_name = video_title

            for char in track_name:
                if char in self.illegal_chars:
                    track_name = track_name.replace(char, '_')
            track_name_path = os.path.join(
                dwld_path,
                f'{track_name}.mp3'
            )
                
            video_clip = VideoFileClip(video_title_path)            
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(track_name_path)
                
            audio_clip.close()
            video_clip.close()

            os.remove(video_title_path)

        return None