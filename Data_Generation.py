"""
CSC111 Final Project: Playlist Generator

Module Description
==================
This module is to demonstrate our data generation algorithms as the main program works on datasets
that are too large to be run in a reasonable amount of time. This module only contains code to run
the k-means and graph generation algorithms. We did not feel like the preprocessing merited
demonstration as it only consisted of using pandas to manipulate dataframes.

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
from k_means import KMeansAlgo
from post_cluster import Graph


def k_means_next(k_means: KMeansAlgo) -> None:
    """Shows a visualization of k-means working on a 2-dimensional dataset.
    We chose to use 2 dimensional data as it is the easiest to graph and will best illustrate
    the k-means algorithm. The algorithm is the same regardless of the dimension of the dataset."""
    k_means.run_once()
    k_means.graph_2d('acousticness', 'danceability', 4)


def visualize_graphing(k_means: KMeansAlgo) -> None:
    """Shows what the graph looks like for a cluster in the k-means object after
    it has finished clustering"""
    k_means.run_n_times(4)
    cluster = k_means.clusters[list(k_means.clusters)[0]]
    graph = Graph(cluster, 0.1)
    graph.init_edges()
    graph.draw_with_matplotlib()


if __name__ == "__main__":
    k_means = KMeansAlgo('DataGeneration Data/normalized_data_sample.csv', 4)


