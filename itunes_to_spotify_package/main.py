#!/usr/bin/env python

import click
from itunes_to_spotify_package.search import get_uri_list
from itunes_to_spotify_package.util import read_txtfile
from itunes_to_spotify_package.spotify_conn import (get_spotify_connection,
                                                    overwrite_playlist)
from itunes_to_spotify_package.spotify_conn import create_playlist


@click.command()
@click.option('--playlist_uri', prompt=True,
              help='playlist uri, should look like: '
                   'spotify:user:#####:playlist:********')
@click.option('--filepath', prompt=True, help='path to .txt file')
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
def main_overwrite(playlist_uri, filepath, verbose):
    search_and_write_playlist(filepath, verbose, playlist_uri=playlist_uri)


@click.command()
@click.option('--playlist_name', prompt=True,
              help='name of the playlist to create')
@click.option('--playlist_desc', prompt=True,
              help='description of the playlist to create')
@click.option('--filepath', prompt=True, help='path to .txt file')
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
def main_new_playlist(playlist_name, playlist_desc, filepath, verbose):
    search_and_write_playlist(filepath, verbose, 
                              playlist_name=playlist_name, playlist_desc=playlist_desc)
    
def search_and_write_playlist(filepath:str, 
                              verbose:bool, 
                              spotify=None,
                              playlist_uri:str=None,
                              playlist_name:str=None,
                              playlist_desc:str=None,
                              creds=None):
    if creds==None:
        from itunes_to_spotify_package.creds import creds as default_creds
        creds = default_creds
    
    if spotify==None:
        spotify = get_spotify_connection(creds['SPOTIPY_USERNAME_URI'],
                                        client_id=creds['SPOTIPY_CLIENT_ID'],
                                        client_secret=creds['SPOTIPY_CLIENT_SECRET'],
                                        redirect_uri=creds['SPOTIPY_REDIRECT_URI'])

    itunes_song_list = read_txtfile(filepath=filepath, verbose=verbose)
    uri_list = get_uri_list(itunes_song_list, spotify=spotify, verbose=verbose)

    if playlist_name and playlist_desc:
        playlist_uri = create_playlist(spotify=spotify,
                            playlist_name=playlist_name,
                            description=playlist_desc)

    overwrite_playlist(uri_list,
                       spotify=spotify,
                       playlist_uri=playlist_uri,
                       username=creds['SPOTIPY_USERNAME_URI'])


if __name__ == "__main__":
    main()
