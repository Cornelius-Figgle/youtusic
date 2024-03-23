# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

# source: https://github.com/Cornelius-Figgle/youtusic/

'''
Parses the command-line arguements and the TOML config file as well as forming
a final dictionary based on these and preset defaults
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


import os
import tomllib
from argparse import ArgumentParser


def parse_arg_line(argv: list) -> dict:
    '''
    Create a config from the command-line arguements passed to the program
    '''

    # create main object
    parser = ArgumentParser(
        description='A curses-based TUI for managing music across platforms',
        epilog='For additional support and help, please visit ' \
            'https://github.com/Cornelius-Figgle/youtusic or drop an email to max@fullimage.net'
    )

    # version arg
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {__version__}')

    # create subparser object
    subparsers = parser.add_subparsers(help='sub-command help')

    # add subparsers
    parser_sync = subparsers.add_parser('sync', help='sync help')
    parser_group = subparsers.add_parser('group', help='group help')
    parser_auth = subparsers.add_parser('auth', help='auth help')

    # return config set by command line
    return parser.parse_args(argv)

def parse_user_config() -> dict:
    ''' 
    Create a config from the `config.toml` file
    '''

    # lists possible config file locations
    if os.name in ('dos', 'nt'):  # if Windows
        file_paths = [
            os.path.join(
                os.environ.get('APPDATA', str()),
                'youtusic',
                'config.toml'
            ),  # %APPDATA%\youtusic\config.toml
            os.path.join(
                os.path.expanduser('~'),
                'AppData',
                'Roaming',
                'youtusic',
                'config.toml'
            ),  # %USERPROFILE%\AppData\Roaming\youtusic\config.toml
            os.path.join(
                os.path.expanduser('~'),
                '.config',
                'youtusic',
                'config.toml'
            )  # %USERPROFILE%\.config\youtusic\config.toml
        ]
    else:  # if not Windows
        file_paths = [
            os.path.join(
                os.environ.get('XDG_CONFIG_HOME', str()),
                'youtusic', 
                'config.toml'
            ),  # $XDG_CONFIG_HOME/youtusic/config.toml
            os.path.join(
                os.path.expanduser('~'),
                '.config',
                'youtusic',
                'config.toml'
            )  # ~/.config/youtusic/config.toml
        ]

    # check each path and use the first one that exists
    for path in file_paths:
        if os.path.exists(path):
            # get path for authentication config
            # split to allow main configuration to be seperated from auth keys
            # this allows it to be stored more securely/outside the repo
            auth_path = os.path.join(
                os.path.dirname(path),
                'auth.toml'
            )
            
            # load files
            with open(path, 'rb') as file, open(auth_path, 'rb') as auth_file:
                loaded_file = tomllib.load(file)
                loaded_auth_file = tomllib.load(auth_file)
                
            # merge main and auth files
            merged_file_configs = dict()
            for header in loaded_file.keys():
                merged_file_configs[header] = {
                    **loaded_file[header],
                    **loaded_auth_file[header]
                }

            return merged_file_configs
        else:
            continue

        # if no file found, return blank dict
        return {}

def generate_final_config(argv: list) -> dict:
    '''
    Combines configuration from command-line arguements, the user config file
    and default options
    '''

    arg_cfg = {}  # parse_arg_line(argv)
    file_cfg = parse_user_config()
    default_cfg = {}

    # merge arg onto file, then the result onto the default
    return {**default_cfg, **{**file_cfg, **arg_cfg}}
