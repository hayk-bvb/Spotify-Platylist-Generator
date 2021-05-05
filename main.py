"""
CSC111 Final Project: Playlist Generator

Module Description
==================

This is the main file to run the entire program!
Please use terminal/command prompt to run the file.
See our Proposal for more info on how to run.


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


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pickle', 'tkinter', 'PIL', 'urllib', 'webbrowser',
                          'Recommendation', 'k_means', 'spotipy', 'argparse', 'song_tkinter',
                          'preprocess', 'post_cluster'],
        'allowed-io': [],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })

    from argparse import ArgumentParser
    import tkinter as tk
    import pickle
    import spotipy

    from song_tkinter import UserPlaylistEntry, NewPlaylistOutput
    from preprocess import Data
    from post_cluster import Graph_Save

    print('Running main.py. Tkinter interface will appear', end=' ')
    print('when everything finishes loading.\n', end='\r')

    print('Parsing args...', end='\r')
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--graphs-file-name', type=str)
    args = arg_parser.parse_args()
    print('Done parsing args!\n', end='\r')

    # Preprocessed data
    print('Restoring preprocessed data...', end='\r')
    data_obj = Data()
    print('Done restoring preprocessed data!\n', end='\r')

    # Spotify
    print('Initializing Spotipy client...', end='\r')
    credentials_manager = spotipy.oauth2.SpotifyClientCredentials(
        'daf1fbca87e94c9db377c98570e32ece', '1a674398d1bb44859ccaa4488df1aaa9')
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)
    print('Done initializing Spotipy client!\n', end='\r')

    # Restore centroid_to_graph
    print('Restoring Graphs... This will take a while (3 - 10 min).', end='\r')
    graphs_file = open(args.graphs_file_name, 'rb')
    centroid_to_graph_save = pickle.load(file=graphs_file)
    centroid_to_graph = dict()
    for centroid in centroid_to_graph_save:
        cur_graph_save = centroid_to_graph_save[centroid]
        restored_graph = cur_graph_save.restore()
        centroid_to_graph[centroid] = restored_graph
    print('Done restoring Graphs!                                  \n', end='\r')

    # Show tkinter
    print('Starting Tkinter interface.\n', end='\r')
    input_window_root = tk.Tk()
    input_window = UserPlaylistEntry(root=input_window_root,
                                     core={'data_obj': data_obj,
                                           'sp': sp,
                                           'centroid_to_graph': centroid_to_graph})
    input_window.run_window()
    input_window_root.mainloop()
