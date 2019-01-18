# Utility Functions

from typing import List, Tuple, Dict
import re


def read_txtfile(filepath: str, verbose=False) -> List[Tuple[str]]:
    '''
    Takes a tab delimited text file of an iTunes playlist and creates a list of
    tuples in the format: (songname, artist)
    '''
    songs = []

    if verbose:
        print(f'> Reading songs from: {filepath}')

    with open(filepath, 'rb') as f:
        contents = f.read()
    contents = contents.decode("utf-16").split("\r")
    for line in contents:
        try:
            song = line.split('\t')[0].replace("\n", "")
            artist = line.split('\t')[1].replace("\n", "")
            if song != 'Name':
                songs.append((song, artist))
        except IndexError:
            if line.strip() and verbose:
                print(f'Corrupt line: {line}')
            else:
                pass  # ignore blank line

    if songs:
        if verbose:
            print(f'\n> Number of songs in itunes text file: {len(songs)}')
        return songs
    else:
        raise Exception("Empty song list after parsing file.")


def get_info(songs_results: Dict) -> Tuple[str]:
    '''
    Takes a dictionary result from a spotify API call and extracts info
    about a song.
    '''
    url = songs_results['external_urls']['spotify']
    uri = songs_results['external_urls']['spotify'].split('/')[-1]
    name = songs_results['name']
    spotify_artist = songs_results['artists'][0]['name']  # TODO: all artists
    return (url, uri, name, spotify_artist)


def alpha_num_lower(s: str) -> str:
    '''
    Returns a string with everything stripped except the
    lowercase alphanumeric characters
    '''
    # EXAMPLE:
    # alpha_num_lower('\n  asdfa^%LKAJL1231___daf.cas,   asdf \tasdfa  ')
    return re.sub(r'\W+', '', s).lower()
