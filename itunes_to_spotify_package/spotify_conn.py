# Spotify functions

import spotipy
import spotipy.util as util
from typing import List, Dict


def get_spotify_connection(username_uri,
                           client_id,
                           client_secret,
                           redirect_uri) -> spotipy.Spotify:
    SCOPE = ('playlist-modify-public, playlist-modify-private, '
             'user-library-modify')
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
                    username: str,
                    public: bool = True,
                    description: str = ''):
    # IN PROGRESS TODO
    # giving me error :(
    # for now, need to use existing playlist
    spotify.user_playlist_create(username,
                                 name=playlist_name,
                                 public=public)
    # calling it
    # create_playlist(spotify=spotify,
    #                 playlist_name="helloWorld",
    #                 username=SPOTIPY_USERNAME_URI,
    #                 description = "temp test playlist")


def overwrite_playlist(full_results_list: List[Dict],
                       spotify,
                       playlist_uri: str,
                       username):
    # Get list of uris from results
    uri_songlist = [uri for result in full_results_list
                    for k, uri in result.items() if k == 'uri']

    # replace all tracks in playlist with new tracks
    spotify.user_playlist_replace_tracks(user=username,
                                         playlist_id=playlist_uri,
                                         tracks=uri_songlist[0:100])
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
