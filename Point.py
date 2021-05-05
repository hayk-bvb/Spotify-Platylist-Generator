"""
CSC111 Final Project: Playlist Generator

Module Description
==================

This a file dedicated for a class Point which represents a song vertex.

We have separated this class because it is central for the computation,
used very often and we wanted to avoid an Import Error, from circular importing!


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
from __future__ import annotations
from typing import Any, List

class Point:
    """
    A song in Graph.

    Instance Attributes:
        - pos: List of floats representing normalized position of point in Graph
        - id: String representing Song id registered with Spotify
        - neighbours: Dictionary mapping distance to neighbour
    """

    pos: List[float]
    id: str
    neighbours: dict

    def __init__(self, pos: ..., point_id='NA') -> None:
        """
        Initialize with normalized position, id, and no neighbours
        """
        self.pos = pos
        self.id = point_id
        self.neighbours = dict()  # distance to Point

    def __repr__(self) -> str:
        """
        Return self.id when converting to string
        """
        return str(self.id)

    def become_neighbour(self, point: Point) -> None:
        """
        Add self to point.neighbours
        Add point to self.neighbours
        """
        distance = self.distance_from(point)
        while distance in self.neighbours:
            distance += 0.0000000001
        self.neighbours[distance] = point
        point.neighbours[distance] = self

    def is_neighbour_with(self, point: Point) -> bool:
        """
        Return whether a point is neighbours with given point
        """
        return point in self.neighbours.values()

    def get_neighbour(self, distance: float) -> Point:
        """
        Return neighbour given distance (which represents self's distance from neighbour)
        """
        return self.neighbours[distance]

    def distance_from(self, point: Point) -> float:
        """
        Returns the distance from a given point
        """
        dimension = len(self.pos)
        accumulator = 0
        for i in range(dimension):
            delta = self.pos[i] - point.pos[i]
            accumulator += delta ** 2
        return accumulator ** 0.5


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pickle', 'tkinter', 'PIL', 'urllib', 'webbrowser',
                          'Recommendation', 'Spotify.Spotify_client', 'Spotify.song_features',
                          'k_means', 'spotipy', 'argparse', 'song_tkinter', 'preprocess',
                          'post_cluster', 'typing'],
        'allowed-io': [],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
