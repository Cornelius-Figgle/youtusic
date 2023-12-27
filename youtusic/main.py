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


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Youtusic_:
    def __init__(self, user_config: dict) -> None:
        '''
            
        '''

        self.user_config = user_config

    def get_spotify_playlist() -> dict:
        '''
            
        '''

        # initialises Spotify object
        oauth = SpotifyClientCredentials(
            client_id=self.user_config['spotify']['id'],
            client_secret=self.user_config['spotify']['secret'],
        )
        sp = spotipy.Spotify(
            client_credentials_manager=oauth
        )
