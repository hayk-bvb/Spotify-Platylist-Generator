"""
CSC111 Final Project: Playlist Generator

Module Description
==================
This module contains the classes needed to perform the k-means clustering algorithm.
The KMeansAlgo object stores a state of the clsuters at a particular iteration of the k-means
clustering algorithm. It contains functions to update the state of that clusters to what
it should look like at the next iteration.

For our project, a KMeansAlgo object should be initialized with the
path 'Data/normalized_data_final.csv' and k of 100. we ran the clustering algorithm
15 times to refine the clusters. This object was then stored as a pickle file to reduce
runtime.

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
from typing import List
import random
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Point import Point

ATTRIBUTE_TO_INDEX = {'acousticness': 0, 'danceability': 1, 'energy': 2, 'duration(ms)': 3,
                      'instrumentalness': 4, 'valence': 5, 'tempo': 6, 'liveness': 7,
                      'loudness': 8, 'speechiness': 10, 'key': 11}
COLOR_CHOICES = list(plt.cm.colors.cnames)


class KMeansAlgo:
    """Object to store data and methods for executing k-means algorithm. Specifically,
    the object stores the state of a dataset during a single iteration of k-means. The class
    contains methods to execute the algorithm on the data that is stored.

    Attributes:
        - data: A list of Point objects that are used in the algorithm to form clusters
        - centroids: A list of Point objects that describe the centers of the cluster
        - cluster: A dictionary mapping a centroid to a list of Points in that cluster

    Representation Invariants:
        - self.k > 0
        - len(self.centroids) > 0
    """

    data: list
    centroids: list
    clusters: dict

    def __init__(self, path: str, k: int) -> None:
        """Initializes the k_means object with k number of centroids that are picked randomly
        from the data points. The initialization also does the first round of clustering based
        on those centroids.

        Preconditions:
            - k > 0
            - path contains a file that is formatted correctly for the load_path function
        """
        self.data = initialize_data(load_path(path))
        self.centroids = [random.choice(self.data) for _ in range(k)]
        self.clusters = self.update_clusters()

    def run_n_times(self, n: int) -> None:
        """Run the k_means algorithm n times. Function will not run if n <= 0.
        """
        for _ in range(n):
            self.run_once()

    def run_once(self) -> None:
        """Runs the k-means algorithm once. The algorithm first finds the new centers of the
        clusters and then updates the clusters themselves. The function stores the new clusters
        in it's attributes."""
        self.centroids = self.find_new_centroids()
        self.clusters = self.update_clusters()

    def update_clusters(self) -> dict:
        """Sorts every point in self.data into a cluster based on the centroid that the point
        is closest to. Returns a dictionary mapping each centroid to a list of points which
        represents the clusters."""
        # initialize a dictionary mapping each current centroid to a empty list
        clusters = dict((key, []) for key in self.centroids)

        # Iterate through every data point and sort into a centroid based on distance
        for i in range(len(self.data)):
            point = self.data[i]
            closest_center = self.centroids[0]
            min_distances = point.distance_from(closest_center)

            # Iterate through each centroid and check distance between centroid and point
            # Closest centroid is saved in closest_center
            for centroid in self.centroids:
                curr_distance = point.distance_from(centroid)
                if curr_distance < min_distances:
                    min_distances = curr_distance
                    closest_center = centroid

            # Append current point to the cluster of the associated center
            clusters[closest_center].append(point)

        return clusters

    def find_new_centroids(self) -> List[Point]:
        """Returns the new centroids for each cluster based on the average of the attributes of the
        points in each cluster. The new centroids are returned as a list of Point objects"""
        new_centroids = []

        # Iterate through the clusters and update each center
        for centroid in self.clusters:

            # Helper function finds the new center for each individual cluster
            new = _update_centroid(centroid, self.clusters[centroid])
            new_centroids.append(new)

        # returns a list of the new centroids which will be used to update the clusters
        return new_centroids

    def print_cluster_len(self) -> None:
        """Print the lengths of each cluster in self.cluster"""
        for cluster in self.clusters:
            print(len(self.clusters[cluster]))

    # def get_clusters(self) -> List[List[Point]]:
    #     """Returns the clusters stored in the object as a list of lists where each inner
    #     list is a cluster."""
    #     accumulator = []
    #     for cluster in self.clusters:
    #         accumulator.append(self.clusters[cluster])
    #     return accumulator
    def get_clusters(self) -> dict:
        """Returns the clusters stored in the object as a list of lists where each inner
        list is a cluster."""
        return self.clusters

    def graph_3d(self, x: str, y: str, z: str, n: int) -> None:
        """
        Graph the furthest n clusters in 3 dimensions based on the attributes given
        for x, y, and z.

        Preconditions:
            - x in {acousticness, danceability, energy, duration(ms), instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - y in {acousticness, danceability, energy, duration(ms), instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - z in {acousticness, danceability, energy, duration(ms), instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - n <= len(self.cluster)
            - x != y != z
        """
        x, y, z = list(map(str.lower, [x, y, z]))
        # If matplotlib is displaying a graph, clear the graph
        if plt.get_fignums():
            plt.clf()

        # Get index that will be graphed
        x_index = ATTRIBUTE_TO_INDEX[x]
        y_index = ATTRIBUTE_TO_INDEX[y]
        z_index = ATTRIBUTE_TO_INDEX[z]
        points = []

        # Find n centroids that are the furthest from each other
        clusters_to_graph = self.find_furthest_n_clusters(n)

        for cluster in clusters_to_graph:
            points.extend(self.clusters[cluster])

        # Generate the x, y, z values to plot
        x = [p.pos[x_index] for p in points]
        y = [p.pos[y_index] for p in points]
        z = [p.pos[z_index] for p in points]

        for p in self.centroids:
            x.append(p.pos[x_index])
            y.append(p.pos[y_index])
            z.append(p.pos[z_index])

        colors = []

        # Generate color map for graph
        c_i = 10
        for cluster in clusters_to_graph:
            for _ in self.clusters[cluster]:
                colors.append(COLOR_CHOICES[c_i])
            c_i += 1
            if c_i >= len(COLOR_CHOICES):
                c_i = 0
        for _ in range(len(self.centroids)):
            colors.append('black')

        # Plot graph
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(xs=x, ys=y, zs=z, color=colors)
        plt.show()

    def graph_2d(self, x: str, y: str, n: int) -> None:
        """
        Graph the clusters in 2 dimensions based on the attributes given for x and y

        Preconditions:
            - x in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - y in {acousticness, danceability, energy, duration_ms, instrumentalness, valence,
            tempo, liveness, loudness, speechiness, key}
            - n <= len(self.clusters)
            - x != y
        """
        # If matplotlib is displaying a graph, clear the graph
        if plt.get_fignums():
            plt.clf()

        # Get index that should be graphed
        x_index = ATTRIBUTE_TO_INDEX[x]
        y_index = ATTRIBUTE_TO_INDEX[y]

        points = []

        # Find n centroids that are the furthest from each other
        clusters_to_graph = self.find_furthest_n_clusters(n)

        for cluster in clusters_to_graph:
            points.extend(self.clusters[cluster])

        # Generate the x, y values to plot
        x = [point.pos[x_index] for point in points]
        y = [point.pos[y_index] for point in points]

        for point in self.centroids:
            x.append(point.pos[x_index])
            y.append(point.pos[y_index])

        colors = []

        # Generate color map for graph
        c_i = 10
        for cluster in clusters_to_graph:
            for _ in self.clusters[cluster]:
                colors.append(COLOR_CHOICES[c_i])
            c_i += 1
            if c_i >= len(COLOR_CHOICES):
                c_i = 0

        for _ in range(len(self.centroids)):
            colors.append('black')

        # Plot graph
        plt.scatter(x, y, c=colors)
        plt.show()

    def find_furthest_n_clusters(self, n: int) -> list:
        """Returns a list of clusters that are far away from each other"""
        centroids = list(self.clusters)

        # Find the distances of every unique pair of centroids and store in list as tuple
        # with values as distance, centroid1, centroid2
        distances = [(centroids[i].distance_from(centroids[j]), centroids[i], centroids[j])
                     for i in range(len(centroids))
                     for j in range(i, len(centroids))
                     if centroids[i] != centroids[j]]

        # Sorted distances so that the furthest 2 distances are closest
        distances.sort(reverse=True)

        result = set()

        i = 0

        # Take the first n values and put the centroids in a list
        while len(result) < n:
            result.add(distances[i][1])
            result.add(distances[i][2])
            i += 1

        # Return the result as a list of centroids
        return list(result)


def _update_centroid(centroid: Point, points: list) -> Point:
    """Helper function for KMeansAlgo.find_new_centroids.
    Returns the new center of the cluster associated with the given centroid. If the
    cluster is empty, then the original centroid is returned. Otherwise, a new Point object
    is created with the position of the new center is returned."""

    if len(points) == 0:
        # If the length of the associated cluster is 0, return original centroid
        return centroid
    else:
        # If length of associated cluster is > 0, find new centroid
        new_pos = []
        dimensions = len(centroid.pos)

        # Iterate through each attribute of the clusters and find the average
        for i in range(dimensions):
            accumulator = 0
            for point in points:
                accumulator += point.pos[i]
            # Append the average to the pos value of new centroid
            new_pos.append(accumulator / len(points))

        # Return point object with pos of new centroid
        return Point(new_pos)


def load_path(path: str) -> List[List]:
    """Loads the .csv file at path. This function assumes that the first column represents the id
    of the song and the rest of the columns represent the position values. The function
    returns a list of lists, where each inner list is a row in the .csv file.

    Preconditions:
        - The .csv file stored at path must be formatted such that the columns are ordered in the
        following way from left to right
            [acousticness, danceability, energy, duration_ms, instrumentalness, valence, tempo,
            loudness, speechiness, key]
    """
    file = csv.reader(open(path))
    next(file)
    accumulator = []

    for line in file:
        entry = list()
        entry.append(line[0])
        entry.extend([float(val) for val in line[1:]])
        accumulator.append(entry)

    return accumulator


def initialize_data(data: List[List]) -> List[Point]:
    """Given a list of lists in the appropriate format, returns a list of Point objects.

    Precondition:
        - all(type(line[0]) == str for line in data)
        - all([type(val) == Union[float, int] for val in line[1:]] for line in data)
    """
    return [Point(line[1:], line[0]) for line in data]


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['__future', 'typing', 'matplotlib.pyplot', 'mpl_toolkits.mplot3d',
                          'Point', 'random', 'csv'],  # the names (strs) of imported modules
        'allowed-io': ['print_cluster_len', 'load_path'],  # the names (strs) of functions that
        # call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
