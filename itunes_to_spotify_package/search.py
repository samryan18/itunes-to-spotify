'''
Search Functions

Not pretty but gets the job done
'''


from typing import List, Tuple, Dict
from itunes_to_spotify_package.util import get_info, alpha_num_lower


def get_uri_list(itunes_songs: List[Tuple[str]],
                 spotify,
                 verbose=False) -> List[Dict]:
    '''
    Takes a list of tuples in the format: (songname, artist) and searches
    spotify to create a list or spotify songs that match.
    '''
    full_results_list = []
    no_match_list = []
    for track, artist in itunes_songs:
        # search song on spotify
        results = spotify.search(q=track, type='track',  limit=50)

        # iterate through results
        if not results['tracks']['items']:
            # No search results at all
            results = spotify.search(q=track.split('(')[0], type='track',
                                     limit=50)
        if not results['tracks']['items']:
            results = spotify.search(q=track.split('[')[0], type='track',
                                        limit=50)
        if not results['tracks']['items']:
            # strip numbers on left (i.e. album number numbers sometimes in CD uploads)
            results = spotify.search(q=track.lstrip('0123456789.- '), type='track',
                                        limit=50)
        if not results['tracks']['items']:
            results = spotify.search(q=track.replace('.', ''),
                                        type='track',  limit=50)
        if not results['tracks']['items']:
            if verbose:
                print(f'No search results for {track}')
                continue

        # results exist!
        no_match = True
        # for songs_results in results['tracks']['items']:
        results = sort_results_by_popularity(results['tracks']['items'])
        for url, uri, name, spotify_artist, popularity in results:
            # compare alphanumeric lowercase artists
            if ((alpha_num_lower(spotify_artist) in alpha_num_lower(artist)
                    or alpha_num_lower(artist)
                    in alpha_num_lower(spotify_artist)
                    or alpha_num_lower(artist)
                    in alpha_num_lower(name)
                    ) and not 'karaoke' in alpha_num_lower(name)
                    and not 'kaoke' in alpha_num_lower(name)):
                # case match
                full_results_list.append({'name': name,
                                          'artist': artist,
                                          'url': url,
                                          'uri': uri,
                                          'found_by': 1})
                no_match = False
                break

        if no_match:
            # try again!
            # search song on spotify again with artist name
            results = spotify.search(q=f'{track} {artist}', type='track',
                                     limit=50)
            
            if not results['tracks']['items']:
                results = spotify.search(q=f'{track.split("(")[0]} {artist}', type='track',
                                     limit=50)
            if not results['tracks']['items']:
                results = spotify.search(q=f'{track.split("[")[0]} {artist}', type='track',
                                     limit=50)
            if not results['tracks']['items']:
                results = spotify.search(q=f'{track.split("[")[0]} {artist}', type='track',
                                     limit=50)
            if not results['tracks']['items']:
                results = spotify.search(q=f'{track.lstrip("0123456789.- ")} {artist}', type='track',
                                     limit=50)
            # iterate through results
            if not results['tracks']['items']:
                # No search results for song_name+song_artist
                if verbose:
                    print(f'No match within search results '
                          f'for {track} by {artist}')
                    no_match_list.append({'name': track, 'artist': artist})
            else:
                # results exist!
                no_match = True
                results = sort_results_by_popularity(results['tracks']['items'])
                for url, uri, name, spotify_artist, popularity in results:
                    # compare alphanumeric lowercase artists
                    if ((alpha_num_lower(spotify_artist)
                            in alpha_num_lower(artist)
                        or alpha_num_lower(artist)
                            in alpha_num_lower(spotify_artist)
                        or alpha_num_lower(artist)
                            in alpha_num_lower(name)
                        or alpha_num_lower(spotify_artist)
                            in alpha_num_lower(name)) 
                            and not 'kaoke' in alpha_num_lower(name)):
                        # case match
                        full_results_list.append({'name': name,
                                                  'artist': artist,
                                                  'url': url,
                                                  'uri': uri,
                                                  'found_by': 2})
                        no_match = False
                        break

                if no_match:
                    # if still no match, fuck it
                    if verbose:
                        print(f'No match within search results '
                              f'for {track} by {artist}')
                        no_match_list.append({'name': track, 'artist': artist})

    print(f'> Successfully found {len(full_results_list)}/{len(itunes_songs)} '
          f'songs on spotify search')
    info_dict = {
        'num_found': len(full_results_list),
        'num_in_original': len(itunes_songs),
        'full_results_list': full_results_list,
        'no_match_list': no_match_list
    }
    return full_results_list, info_dict

def sort_results_by_popularity(results: List[Dict]) -> List[Tuple[str]]:
    final_results = []
    for songs_results in results:
        url, uri, name, spotify_artist, popularity = get_info(songs_results)
        final_results.append((url, uri, name, spotify_artist, popularity))

    return sorted(final_results, key=lambda x: x[-1], reverse=True)