# youtusic

A [yt-dlp](https://github.com/yt-dlp/yt-dlp) wrapper that downloads songs from Spotify and YouTube playlists! (csv coming soon)

## Installation

### Source

[Python 3](https://www.python.org/downloads/) will need to be installed if it isn't already

You can then either clone the repo or download the zip from GitHub

```shell
git clone https://github.com/Cornelius-Figgle/youtusic.git
```

And the dependencies can be installed via [pip](https://pip.pypa.io/en/stable/) (which is normally installed with Python) when inside your virtual environment. It is recommended that these are installed inside a [virtual environment](https://docs.python.org/3/library/venv.html) in your project repo

*The `pick` module should be installed via my [GitHub fork](https://github.com/Cornelius-Figgle/pick) until my [pull request](https://github.com/wong2/pick/pull/95) is merged into the `master` branch of [pick](https://github.com/wong2/pick/)*

```shell
pip install spotipy yt-dlp pytube python-decouple moviepy tqdm 
pip install git+https://github.com/Cornelius-Figgle/pick.git@master
```

or alternatively, (when inside repository root)

```shell
pip install -r ./docs/requirements.txt
```

### Binaries / Releases

If you wish to install the binaries (executables) instead of the source files, [see here](https://github.com/cornelius-figgle/youtusic/releases)

## Usage

If using `spotipy`, please make sure that the `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` environment variables are set. This can be done by placing a file named `.env` (that should be the full name, no words before the dot) in the root of the project dir. Values for these can be generated by creating a project under your Spotify account [here](https://developer.spotify.com/dashboard/applications)

```shell
python ./main.py
```

- This will run a user-interface for the `youtusic.py` module
- Please make sure all paths are public and valid
- If loading from csv, please follow the structure defined in the [`example`](./tests/example_csv.csv)
