"""
CSC111 Final Project: Playlist Generator

Module Description
==================

This file is responsible of storing the recommendation class which we use to recommend new
songs!


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

import pickle
from typing import Any
from spotify_client import Spotify_Client
from Point import Point
from post_cluster import Graph_Save


class Recommendation:
    """A class to represent a recommendation

    Instance Attributes:
        - playlist_link: this is the link of the given playlist from the user
        - adventure: this is an integer which represents the size of adventure they want for their
        recommendation
        - data: a data object to normalize new song values
        - sp: Spotify API
        - centroid_to_graph: This is a mapping of centroid point to graph object

    """

    playlist_link: str
    adventure: int
    data: Any
    sp: Any
    centroid_to_graph: Any

    def __init__(self, playlist_link: str, adventure: int, data: Any, sp: Any,
                 centroid_to_graph: Any) -> None:
        """
        Initialize the Recommendation class
        """
        self.playlist_link = playlist_link
        self.adventure = adventure
        self.data = data
        self.sp = sp
        self.centroid_to_graph = centroid_to_graph

    def action(self) -> Any:
        """
        Performs the recommendations as described by the comments

        """
        # Get song ids from input playlist link
        # Get normalized features for each song id
        print('Getting song ids, features; and normalizing features...', end='\r')
        # song_ids = get_song_ids(self.playlist_link, self.sp)
        spotify_instance = Spotify_Client()
        song_ids = spotify_instance.get_song_ids(self.playlist_link)
        song_id_to_features = []
        for song_id in song_ids:
            # features = get_features(song_id, self.sp)
            features = spotify_instance.get_song_features(song_id)
            normalized_features = self.data.normalize_value(features)
            song_id_to_features.append([song_id, normalized_features])
        print('Done getting song ids, features; and normalizing features!\n', end='\r')

        # Match each song with a graph
        # - If the song can be found in Graph_Final.pickle / Graph_Final_Evolve.pickle:
        #       Match song with graph
        # - If the song cannot be found:
        #       Match song with closest graph (by checking distance to graph centroid)
        #       And mutate Graph (to be saved)
        print('Matching songs with graphs...', end='\r')
        song_to_centroid = dict()
        graph_mutate = False
        for song in song_id_to_features:
            cur_song_id, cur_song_features = song
            is_in_dataset = False
            corresponding_centroid = None
            for centroid in self.centroid_to_graph:
                if not is_in_dataset:
                    cur_graph = self.centroid_to_graph[centroid]
                    cur_graph_point_ids = [point.id for point in cur_graph.points]
                    if cur_song_id in cur_graph_point_ids:
                        is_in_dataset = True
                        corresponding_centroid = centroid
            if is_in_dataset:
                # If song in dataset:
                song_to_centroid[cur_song_id] = corresponding_centroid
            else:
                # If song not in dataset, find closest centroid
                graph_mutate = True     # Here graph_mutate means: Graph will mutate
                closest_centroid = None
                closest_centroid_distance = None
                cur_point = Point(pos=cur_song_features, point_id=cur_song_id)
                for centroid in self.centroid_to_graph:
                    distance_to_centroid = cur_point.distance_from(centroid)
                    if closest_centroid_distance is None or \
                            distance_to_centroid < closest_centroid_distance:
                        closest_centroid = centroid
                        closest_centroid_distance = distance_to_centroid
                song_to_centroid[cur_song_id] = closest_centroid
        # Before making recommendations:
        # Convert song_to_centroid => centroid_to_songs
        # to avoid duplicate recommendations
        centroid_to_songs = dict()
        for song in song_to_centroid:
            corresponding_centroid = song_to_centroid[song]
            if corresponding_centroid in centroid_to_songs:
                centroid_to_songs[corresponding_centroid].extend([song])
            else:
                centroid_to_songs[corresponding_centroid] = [song]
        print('Done matching songs with graphs!\n', end='\r')

        # For each centroid in centroid_to_songs:
        # - g = self.centroid_to_graph[centroid]
        # - songs = centroid_to_songs[centroid]
        # - Use songs as input to g to make recommendations
        # Combine all recommendations
        print('Making recommendations...', end='\r')
        all_recommendations = []
        for centroid in centroid_to_songs:
            cur_input_songs = centroid_to_songs[centroid]
            cur_graph = self.centroid_to_graph[centroid]
            recommendations, fails = cur_graph.recommend(
                input_song_ids=cur_input_songs, adventure=self.adventure)
            all_recommendations.extend(recommendations)
        print('Done making recommendations!\n', end='\r')

        # If graph(s) mutated: Save to Graph_Final_Evolve.pickle
        # Unlike before, here graph_mutate means: Graph mutated
        if graph_mutate:
            print('Graph(s) were mutated during the recommendation process,', end=' ')
            print('because the input playlist included song(s) that were not '
                  'found in the graph file.\n', end='\r')
            print('Saving mutated Graphs to Graph_Final_Evolve.pickle...')
            centroid_to_graph_save = dict()
            for centroid in self.centroid_to_graph:
                cur_graph = self.centroid_to_graph[centroid]
                cur_graph_save = Graph_Save()
                cur_graph_save.save(cur_graph)
                centroid_to_graph_save[centroid] = cur_graph_save
            save_file = open('Graph_Final_Evolve.pickle', 'wb')
            pickle.dump(obj=centroid_to_graph_save, file=save_file,
                        protocol=pickle.HIGHEST_PROTOCOL)
            save_file.close()
            print('Done saving mutated Graphs to Graph_Final_Evolve.pickle!')
        else:
            print('Graph(s) were not mutated during the recommendation process,', end=' ')
            print('because all songs in the input playlist were found in the graph file.\n',
                  end='\r')

        return all_recommendations


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pickle', 'tkinter', 'PIL', 'urllib', 'webbrowser',
                          'Recommendation', 'k_means', 'spotipy', 'argparse',
                          'song_tkinter', 'preprocess', 'post_cluster', 'Point',
                          'spotify_client'],
        'allowed-io': ['action'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
