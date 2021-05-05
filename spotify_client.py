"""
CSC111 Final Project: Playlist Generator

Module Description
==================

This file is made for creating a new playlist for the user,
getting audio features of a given song id and for
getting a list of song ids from the user's given playlist.
Furthermore, this file relies on the usage of the Spotify API!


Copyright and Usage Information
===============================

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

This file is Copyright (c) 2021 Si Yuan Zhao, Hayk Nazaryan, Cliff Zhang, Joanne Pan.
"""
from typing import List, Any
import spotipy


class Spotify_Client:
    """
    Using the spotipy library to create a playlist, get song features and get song ids
    """
    # Private Instance Attributes:
    #     - _public_id:
    #         The unique identifier for our application.
    #     - _secret_id:
    #         The key that we pass in to secure calls to the Spotify API.
    #     - _redirect_uri:
    #         The uri enables the Spotify authentication service to
    #         automatically relaunch our program when a user runs the application.

    _public_id: Any
    _secret_id: Any
    _redirect_uri: Any

    def __init__(self) -> None:
        """
        Initializes the public_id, secret_id and the redirect_uri so
        that init_user can be called anytime
        """
        self._public_id = 'daf1fbca87e94c9db377c98570e32ece'
        self._secret_id = '1a674398d1bb44859ccaa4488df1aaa9'
        self._redirect_uri = 'https://pass-post.netlify.app'

    def init_user(self) -> Any:
        """
        Initializes an instance of spotipy.Spotify that is logged in
        """
        return \
            spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(scope="playlist-modify-public",
                            client_id=self._public_id, client_secret=self._secret_id,
                            redirect_uri=self._redirect_uri))

    def create_playlist(self, playlist_name: str, song_ids: List[str]) -> str:
        """
        Create a new playlist and return the playlist link
        """
        user = self.init_user()
        user_id = user.me()['id']
        playlist_data = user.user_playlist_create(
            user=user_id, name=playlist_name, public=True)
        user.playlist_add_items(playlist_data['id'], song_ids)
        playlist_link = playlist_data['external_urls']['spotify']
        return playlist_link

    def get_song_features(self, song_id: str) -> List[float]:
        """
        Return the audio features of a song
        Not all the features are returned, only the ones we are considering for clustering:
        acousticness, danceability, energy, duration_ms, instrumentalness, valence, tempo, liveness,
        loudness, speechiness and key.

        Preconditions:
            - song_id is not None
        """
        user = self.init_user()
        user.trace = True
        features = user.audio_features(song_id)[0]
        return [features['acousticness'], features['danceability'],
                features['energy'], features['duration_ms'],
                features['instrumentalness'], features['valence'],
                features['tempo'], features['liveness'],
                features['loudness'], features['speechiness'],
                features['key']]

    def get_song_ids(self, playlist_link: str) -> List[str]:
        """
        Given the user's playlist URL, return a list of track ids included in the playlist.
        """
        user = self.init_user()
        playlist_id = self.parse_link_to_id(playlist_link)
        res = user.playlist_items(playlist_id,
                                  offset=0,
                                  fields='items.track.id',
                                  additional_types=['track'])['items']
        return [item['track']['id'] for item in res]

    def parse_link_to_id(self, playlist_link: str) -> str:
        """
        Given the playlist link, return the playlist id.
        """
        split_1 = playlist_link.split('/')[4]
        split_2 = split_1.split('?')
        return split_2[0]


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pickle', 'tkinter', 'PIL', 'urllib', 'webbrowser',
                          'Recommendation', 'Spotify.Spotify_client', 'Spotify.song_features',
                          'k_means', 'spotipy', 'argparse', 'song_tkinter', 'preprocess',
                          'post_cluster', 'pprint'],
        'allowed-io': [],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })

    # For testing purposes!
    # from pprint import pprint
    # song_ids_block = ['5eI3fMgQoYfYh9NykE78Sn', '70jb2bIurVzYfxhhsRd4ew']
    # playlist_name_block = 'your recommended songs :)'
    #
    # instance = Spotify_Client()
    # print(instance.create_playlist(playlist_name_block, song_ids_block))
    # pprint(instance.get_song_features('5eI3fMgQoYfYh9NykE78Sn'))
    # pprint(instance.get_song_ids(
    #     'https://open.spotify.com/playlist/1fKVI2pKH5EGS0fX2ncoN6'))
