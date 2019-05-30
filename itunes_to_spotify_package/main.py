#!/usr/bin/env python

import click
from itunes_to_spotify_package.search import get_uri_list
from itunes_to_spotify_package.util import read_txtfile
from itunes_to_spotify_package.spotify_conn import (get_spotify_connection,
                                                    overwrite_playlist)
from itunes_to_spotify_package.spotify_conn import create_playlist


# TEMP
from itunes_to_spotify_package.requests_util import make_http_request

@click.command()
@click.option('--playlist_uri', prompt=True,
              help='playlist uri, should look like: '
                   'spotify:user:#####:playlist:********')
@click.option('--filepath', prompt=True, help='path to .txt file')
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
def main(playlist_uri, filepath, verbose):
    search_and_write_playlist(playlist_uri, filepath, verbose)
    
def search_and_write_playlist(playlist_uri, filepath, verbose, creds=None):
    if creds == None:
        from itunes_to_spotify_package.creds import creds as default_creds
        creds = default_creds

    spotify = get_spotify_connection(creds['SPOTIPY_USERNAME_URI'],
                                    client_id=creds['SPOTIPY_CLIENT_ID'],
                                    client_secret=creds['SPOTIPY_CLIENT_SECRET'],
                                    redirect_uri=creds['SPOTIPY_REDIRECT_URI'])

    itunes_song_list = read_txtfile(filepath=filepath, verbose=verbose)
    uri_list = get_uri_list(itunes_song_list, spotify=spotify, verbose=verbose)
    overwrite_playlist(uri_list,
                       spotify=spotify,
                       playlist_uri=playlist_uri,
                       username=creds['SPOTIPY_USERNAME_URI'])

    # IN DEVELOPMENT (CREATES PLAYLIST)
    # create_playlist(spotify=spotify,
    #                 playlist_name="suh suh suh",
    #                 username=SPOTIPY_USERNAME_URI,
    #                 public=False,
    #                 description = "temp test playlist")
    
    
    # data = {'name': "TEST_1", 'public': True, 'description': "test description"}
    # make_http_request(url='https://api.spotify.com/v1/users/'
    #                       'spotify:user:12183238257/playlists',
    #                   data=data,
    #                   auth=spotify._auth)


if __name__ == "__main__":
    main()
