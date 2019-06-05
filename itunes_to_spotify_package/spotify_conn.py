# Spotify functions

import spotipy
import spotipy.util as util
from typing import List, Dict
import random


def get_spotify_connection(username_uri,
                           client_id,
                           client_secret,
                           redirect_uri) -> spotipy.Spotify:
                           
    SCOPE = ('playlist-modify-public, playlist-modify-private')
    # SCOPE = ('playlist-modify-public')
    SPOTIFY_API_TOKEN = util.prompt_for_user_token(username_uri,
                                                   scope=SCOPE,
                                                   client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri)

    if SPOTIFY_API_TOKEN:
        spotify = spotipy.Spotify(auth=SPOTIFY_API_TOKEN)
        spotify.trace = False
        print('Successfully connected to spotify API')
        return spotify
    else:
        raise Exception("Can't get token for ", username_uri)


def create_playlist(spotify,
                    playlist_name: str,
                    public: bool = True,
                    description: str = '') -> str:

    user = spotify.current_user()
    user_id = user['id']
    TEMP_NAME = f'itunes2spotify_TEMPORARY_NAME_NEW_PLAYLIST{random.randint(1,1000)}'
    spotify.user_playlist_create(user=user_id,
                                 name=TEMP_NAME,
                                 public=public,
                                 description=description)
    
    playlists = []
    for i in range(2000):
        # max is 100000
        new_playlists = spotify.user_playlists(user_id, limit=50, offset=(50*i))['items']
        playlists = playlists + new_playlists
        if not new_playlists:
            break
    
    playlist_uri = [p for p in playlists if p['name']==TEMP_NAME][0]['uri']
    playlist_id = [p for p in playlists if p['name']==TEMP_NAME][0]['id']
    spotify.user_playlist_change_details(user=user_id, playlist_id=playlist_id, name=playlist_name)

    return playlist_uri


def overwrite_playlist(full_results_list: List[Dict],
                       spotify,
                       playlist_uri: str,
                       username):
    # Get list of uris from results
    uri_songlist = [uri for result in full_results_list
                    for k, uri in result.items() if k == 'uri']

    # replace all tracks in playlist with new tracks
    try:
        spotify.user_playlist_replace_tracks(user=username,
                                             playlist_id=playlist_uri,
                                             tracks=uri_songlist[0:100])
    except Exception as e:
        print(f'\n\nThis playlist URI causing issue: {playlist_uri}')
        print(f'\nThis uri song list caused the error: {uri_songlist}')
        raise

    while len(uri_songlist) > 100:
        # only 100 songs allowed per request
        uri_songlist = uri_songlist[100:]
        spotify.user_playlist_add_tracks(user=username,
                                         playlist_id=playlist_uri,
                                         tracks=uri_songlist[0:100])
    playlist_info = spotify.user_playlist(user=username,
                                          playlist_id=playlist_uri,
                                          fields=['external_urls'])
    playlist_url = playlist_info['external_urls']['spotify']

    print(f'> Successfully overwrote playlist. \n> URL: {playlist_url}')
    return playlist_url
