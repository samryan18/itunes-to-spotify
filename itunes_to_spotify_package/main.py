#!/usr/bin/env python

import click
from itunes_to_spotify_package.creds import (SPOTIPY_CLIENT_ID,
                                             SPOTIPY_CLIENT_SECRET,
                                             SPOTIPY_REDIRECT_URI,
                                             SPOTIPY_USERNAME_URI)
from itunes_to_spotify_package.search import get_uri_list
from itunes_to_spotify_package.util import read_txtfile
from itunes_to_spotify_package.spotify_conn import (get_spotify_connection,
                                                    overwrite_playlist)


@click.command()
@click.option('--playlist_uri', prompt=True,
              help='playlist uri, should look like: '
                   'spotify:user:#####:playlist:********')
@click.option('--filepath', prompt=True, help='path to .txt file')
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
def main(playlist_uri, filepath, verbose):
    spotify = get_spotify_connection(SPOTIPY_USERNAME_URI,
                                     client_id=SPOTIPY_CLIENT_ID,
                                     client_secret=SPOTIPY_CLIENT_SECRET,
                                     redirect_uri=SPOTIPY_REDIRECT_URI)
    itunes_song_list = read_txtfile(filepath=filepath, verbose=verbose)
    uri_list = get_uri_list(itunes_song_list, spotify=spotify, verbose=verbose)
    overwrite_playlist(uri_list,
                       spotify=spotify,
                       playlist_uri=playlist_uri,
                       username=SPOTIPY_USERNAME_URI)


if __name__ == "__main__":
    main()
