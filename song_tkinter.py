"""
CSC111 Final Project: Playlist Generator

Module Description
==================

This file is made for the user interface of the entire program using Tkinter.
With the given user input, within this file, tasks are carried out such as returning
new_generated playlist and also visualizations for K-means and Individual Graph.

new_generated playlist will be returned with a separate window, where with a button named
"OPEN LINK!", it opens a new tab in the browser, which is the spotify playlist. This same window
also displays the attribute averages of the initial playlist inputted by the user.


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
from typing import Any, Dict
import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import ImageTk, Image
from Recommendation import Recommendation
from spotify_client import Spotify_Client
from k_means import KMeansAlgo


class UserPlaylistEntry:
    """
    This is a class responsible for creating a Tkinter window.

    It collects info from the user such as:
    * their desired playlist input's link
    * the scale of their adventurousness
    * the desired name for their new playlist that is to be generated

     When inputted with the button ENTER, after a few minutes another Tkinter window will pop up,
     from the class NewPlaylistOutput. If during these minutes the Tkinter window shows as
     "Not Responding", this is okay, just please wait as computations are being done!

    Instance Attributes:
        - root: This instance attribute is used for storing the root of the Tkinter window
        - data_obj: A Data object with all of the raw data
        - sp: Spotify API
        - centroid_to_graph: Mapping of centroid point to its associated graph object
        - ordered_centroids: list of ordered centroid points
        - playlist_entry: the inputted playlist by the user
        - scale_entry: the inputted value on scale/slider by the user
        - new_playlist_name: the desired name of the new playlist to be generated
        - visualization: the choice of which option to visualize
        - att_1: the first attribute selected by the user to visualize
        - att_2: the second attribute selected by the user to visualize
        - att_3: the third attribute selected by the user to visualize
        - graph_int: the index of which graph to visualize, selected by the user
    """

    root: Any
    data_obj: Any
    sp: Any
    centroid_to_graph: Any
    ordered_centroids: Any
    playlist_entry: str
    scale_entry: Any
    new_playlist_name: str
    visualization: str
    att_1: str
    att_2: str
    att_3: str
    graph_int: Any

    # Private:
    _image: Any
    _link_entry: tk.Entry
    _slider: tk.Scale
    _new_playlist_name_entry: tk.Entry
    _inner_string: tk.StringVar
    _dimension_menu: tk.OptionMenu
    _inner_string_att1: tk.StringVar
    _attribute1_menu: tk.OptionMenu
    _inner_string_att2: tk.StringVar
    _attribute2_menu: tk.OptionMenu
    _inner_string_att3: tk.StringVar
    _attribute3_menu: tk.OptionMenu
    _graph_int_entry: tk.Entry

    # We only need to initialize the root and core, the latter used for computation on user input
    def __init__(self, root: Any, core: dict) -> None:
        """
        Initialize UserPlaylistEntry class
        """
        # We first initialize the root of our tkinter window
        self.root = root

        # Initialize data needed to recommend
        self.data_obj = core['data_obj']
        self.sp = core['sp']
        self.centroid_to_graph = core['centroid_to_graph']
        self.ordered_centroids = list(self.centroid_to_graph.keys())

        # Here we initialize the rest of the class attributes that are user inputs to empty strings
        self.playlist_entry = ''
        self.scale_entry = ''
        self.new_playlist_name = ''
        self.visualization = ''
        self.att_1 = ''
        self.att_2 = ''
        self.att_3 = ''
        # This we need to initialize to 0
        self.graph_int = 0

        # Open the Spotify Logo to later display
        self._image = Image.open('Spotify-Logo.png').resize((140, 100))

        self._link_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

        self._slider = tk.Scale(self.root, from_=1, to=10, tickinterval=1, orient='horizontal',
                                bg="#1DB954",
                                fg="BLACK", sliderlength=20, length=200)

        self._new_playlist_name_entry = tk.Entry(self.root, borderwidth=10,
                                                 selectbackground='#1DB954')

        self._inner_string = tk.StringVar(self.root)
        self._inner_string.set('Choose Visualization')
        dimension_options = ["K-means", "Individual Graph"]
        self._dimension_menu = tk.OptionMenu(self.root, self._inner_string, *dimension_options)

        self._dimension_menu.config(bg='#1DB954')

        attribute_options = ['Acousticness', 'Danceability', 'Energy', 'Duration(ms)',
                             'Instrumentalness', 'Valence', 'Tempo', 'Liveness', 'Loudness',
                             'Speechiness', 'Key']
        self._inner_string_att1 = tk.StringVar(self.root)
        self._inner_string_att1.set('Attribute 1')
        self._attribute1_menu = tk.OptionMenu(self.root, self._inner_string_att1,
                                              *attribute_options)
        self._attribute1_menu.config(bg='#1DB954')

        self._inner_string_att2 = tk.StringVar(self.root)
        self._inner_string_att2.set('Attribute 2')
        self._attribute2_menu = tk.OptionMenu(self.root, self._inner_string_att2,
                                              *attribute_options)

        self._attribute2_menu.config(bg='#1DB954')

        self._inner_string_att3 = tk.StringVar(self.root)
        self._inner_string_att3.set('Attribute 3')
        self._attribute3_menu = tk.OptionMenu(
            self.root, self._inner_string_att3, *attribute_options)

        self._attribute3_menu.config(bg='#1DB954')

        self._graph_int_entry = tk.Entry(self.root, borderwidth=10, selectbackground='#1DB954')

    def run_window(self) -> None:
        """Runs the Tkinter window for this class
        """

        self.root.title('Spotify Recommender')

        sp_logo = ImageTk.PhotoImage(self._image)
        label = tk.Label(self.root, image=sp_logo)

        # We need to save the reference to the image
        label.image = sp_logo
        label.grid()

        tk.Label(self.root, text='Enter the link of your Spotify playlist below : ',
                 font=("Proxima nova", "9", "bold")).grid()

        self._link_entry.grid(ipadx=30)

        tk.Label(self.root, text="How adventurous are you feeling today?",
                 font=("Proxima nova", "9", "bold")).grid()

        self._slider.grid()

        tk.Label(self.root, text='What do you want to name your new playlist? ',
                 font=("Proxima nova", "9", "bold")).grid()

        self._new_playlist_name_entry.grid(ipadx=30)

        tk.Button(self.root, text='ENTER', command=self.get_user_input, padx=5,
                  pady=5, bg='#1DB954').grid()

        tk.Label(self.root, text='VISUALIZATION \n Please choose a visualization option.',
                 font=("Proxima nova", "9", "bold")).grid(pady=15)

        self._dimension_menu.grid()

        tk.Label(self.root, text='Please choose your first attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute1_menu.grid()

        tk.Label(self.root, text='Please choose your second different attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute2_menu.grid()

        tk.Label(self.root, text='Choose your third different attribute',
                 font=("Proxima nova", "9", "bold")).grid()
        self._attribute3_menu.grid()

        tk.Label(self.root, text='IF CHOSEN GRAPH: Enter an integer 1-100',
                 font=("Proxima nova", "9", "bold")).grid()
        self._graph_int_entry.grid()

        tk.Button(self.root, text='VISUALIZE', command=self.visualize, padx=5,
                  pady=5, bg='#1DB954').grid(pady=15)

    def get_user_input(self) -> None:
        """Designed to be the command for the button 'ENTER':

        Here it stores user input of ONLY the new playlist generation (link, scale, playlist name)

        Furthermore, it also executes recommendation and from that, also computes the link
        to the newly generated Spotify Playlist

        It then passes it on to NewPlaylistOutput, to create a Top Level window for user to
        access the newly generated Spotify Playlist

        Lastly, it also computes the normalized averages of the attributes of the old
        inputted playlist. Assigned as a dictionary, and passed on to NewPlaylistOutput
        to display with bar graphs.
        """

        # Here we update the playlist entry attribute
        self.playlist_entry = self._link_entry.get()

        # Here we update the scale entry attribute
        self.scale_entry = int(self._slider.get())

        # Update the desired new playlists name
        self.new_playlist_name = self._new_playlist_name_entry.get()

        # Need to check if user has inputted everything needed, and only then go into this branch
        if self.playlist_entry != '' and self.scale_entry != '' \
                and self.new_playlist_name != '':

            try:
                tk.Label(self.root, text='YOUR *PLAYLIST* INFORMATION HAS BEEN RECORDED.'
                                         ' \n THANK YOU!',
                         font=("Proxima nova", "9", "bold"), fg='white', bg='black').grid()

                # Recommendation computation from module
                recommended_song_ids = Recommendation(self.playlist_entry,
                                                      self.scale_entry,
                                                      self.data_obj,
                                                      self.sp,
                                                      self.centroid_to_graph).action()

                # Generating new link
                # new_playlist_link = SpotifyClient(recommended_song_ids,
                # self.new_playlist_name).url
                spotify_instance = Spotify_Client()
                new_playlist_link = spotify_instance.create_playlist(self.new_playlist_name,
                                                                     recommended_song_ids)

                # Calculating old playlist averages to display
                aves = [0] * 9      # 9 features
                num_songs = 0
                for song_id in recommended_song_ids:
                    num_songs += 1
                    # features = self.data_obj.normalize_value(get_features(song_id, self.sp))

                    features = self.data_obj.normalize_value(
                        spotify_instance.get_song_features(song_id))

                    # Removing duration(ms) and key
                    cols_removed_features = features[:3] + features[4:10]
                    for i in range(len(aves)):
                        aves[i] += cols_removed_features[i]

                aves = list(map(lambda ave: round(ave / num_songs * 100), aves))

                output_playlist_summary = {'Acousticness': aves[0],
                                           'Danceability': aves[1],
                                           'Energy': aves[2],
                                           'Instrumentalness': aves[3],
                                           'Valence': aves[4],
                                           'Tempo': aves[5],
                                           'Liveness': aves[6],
                                           'Loudness': aves[7],
                                           'Speechiness': aves[8]}

                # Running another Tkinter window (Top Level) to
                # display computations(aka new playlist)
                output_root = tk.Toplevel()
                output_window = NewPlaylistOutput(output_root,
                                                  new_playlist_link,
                                                  output_playlist_summary)
                output_window.run_window()
                output_root.mainloop()

            # Case where there may be in song in user playlist that is not recognized by API
            except TypeError:
                print('There is a song in this playlist that the Spotipy API cannot read. \n'
                      'This is because this song is not defined in Spotify but rather '
                      'it most likely is from a local file. \n Please input a new playlist! ')
        else:
            print('Invalid playlist entry inputs.\nPlease input all entries!.')

        print('Playlist generation over. If you want, input another playlist link, \n'
              'try to visualize, or close window!')

    def visualize(self) -> None:
        """A method that is designed to be used as a button command for the visualize button at the
        bottom of the Tkinter window

        This also stores the user inputs of for the visualization (visual-type, atts 1-3, graph-int)
        """
        # Record all the user input for visualization
        self.visualization = self._inner_string.get()
        self.att_1 = self._inner_string_att1.get()
        self.att_2 = self._inner_string_att2.get()
        self.att_3 = self._inner_string_att3.get()
        self.graph_int = self._graph_int_entry.get()

        # .get() returns a string thus there occurs this case below ->
        # This is the case where we did not select Graph Visualization, in this case I am doing this
        # in order not to receive type error when checking if self.graph > 100
        if self.graph_int == '':
            self.graph_int = 0
        elif int(self.graph_int) > 100:
            # If the input is higher than 100, automatically set to the highest (100)
            self.graph_int = 100
        else:
            # graph_int is valid
            self.graph_int = int(self.graph_int)

        first = self.visualization != 'Choose Visualization' and self.visualization != ''
        second = self.att_1 != '' and self.att_1 != 'Attribute 1'
        third = self.att_2 != '' and self.att_2 != 'Attribute 2'
        fourth = self.att_3 != '' and self.att_3 != 'Attribute 3'

        if first and second and third and fourth:

            tk.Label(self.root, text='YOUR *VISUALIZATION* INFORMATION HAS BEEN RECORDED.'
                                     ' \n THANK YOU!',
                     font=("Proxima nova", "9", "bold"), fg='yellow', bg='black').grid()

            if self.visualization == 'K-means':
                clusters_file = open('Cluster_Final.pickle', 'rb')
                centroid_to_clusters = pickle.load(file=clusters_file)
                k_means = KMeansAlgo(path="Data/normalized_data_final.csv", k=1)
                k_means.clusters = centroid_to_clusters
                k_means.centroids = list(k_means.clusters)
                k_means.graph_3d(self.att_1, self.att_2, self.att_3, n=5)

            else:   # self.visualization == 'Individual Graph'
                centroid = self.ordered_centroids[self.graph_int - 1]
                graph = self.centroid_to_graph[centroid]
                graph.draw_with_matplotlib_3d(self.att_1, self.att_2, self.att_3)
        else:
            print('Invalid visualization options input.\nPlease select all options.')

        print('Visualization over, you enter another playlist or quit the program.')


class NewPlaylistOutput:
    """
    This class is responsible for outputting the link to the final generated playlist, for the user
    to open and listen to.

    Within this window there is also a DID YOU KNOW?! section, where the normalized
    averages of the playlist's song attributes are being displayed with bars.

    Instance Attributes:
        - root: This instance attribute is used for storing the root of the Tkinter window

        - link: This is the link to the newly generated playlist

        - old_averages: This is a dictionary mapping attribute type to its average from all the
        songs in a playlist, this will be used to display the averages bars in the DID YOU KNOW?!
        section.
    """
    root: Any
    link: str
    old_averages: Dict[str, float]

    # Private:
    _image: Any
    _link_button: tk.Button
    _acoustic_progress_bar: ttk.Progressbar
    _dance_progress_bar: ttk.Progressbar
    _energy_progress_bar: ttk.Progressbar
    _instrument_progress_bar: ttk.Progressbar
    _valence_progress_bar: ttk.Progressbar
    _tempo_progress_bar: ttk.Progressbar
    _liveness_progress_bar: ttk.Progressbar
    _loud_progress_bar: ttk.Progressbar
    _speech_progress_bar: ttk.Progressbar

    def __init__(self, root: Any, link: str, old_average: Dict[str, float]) -> None:
        """Initialize the class and its attributes"""

        self.root = root
        self.link = link
        self.old_averages = old_average

        self._image = Image.open('Spotify-Logo.png').resize((140, 100))

        self._link_button = tk.Button(self.root, text='OPEN LINK!', command=self.open_link, padx=5,
                                      pady=5, bg='#1DB954')

        # Each bar needs to be initialized and to add colours to them we have to add it with a style
        # for each bar

        style_acoustic = ttk.Style()
        style_acoustic.theme_use('alt')
        style_acoustic.configure("orange.Horizontal.TProgressbar", foreground='orange',
                                 background='orange')

        self._acoustic_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                      style='orange.Horizontal.TProgressbar')

        style_dance = ttk.Style()
        style_dance.theme_use('alt')
        style_dance.configure("red.Horizontal.TProgressbar", foreground='red',
                              background='red')

        self._dance_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                   style='red.Horizontal.TProgressbar')

        style_energy = ttk.Style()
        style_energy.theme_use('alt')
        style_energy.configure("blue.Horizontal.TProgressbar", foreground='blue',
                               background='blue')

        self._energy_progress_bar = ttk.Progressbar(self.root, style='blue.Horizontal.TProgressbar',
                                                    length=300, orient='horizontal')

        style_instrument = ttk.Style()
        style_instrument.theme_use('alt')
        style_instrument.configure("yellow.Horizontal.TProgressbar", foreground='yellow',
                                   background='yellow')

        self._instrument_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                        style="yellow.Horizontal.TProgressbar")

        style_valence = ttk.Style()
        style_valence.theme_use('alt')
        style_valence.configure("violet.Horizontal.TProgressbar", foreground='violet',
                                background='violet')

        self._valence_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                     style="violet.Horizontal.TProgressbar")

        style_tempo = ttk.Style()
        style_tempo.theme_use('alt')
        style_tempo.configure("turquoise.Horizontal.TProgressbar", foreground='turquoise',
                              background='turquoise')

        self._tempo_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                   style="turquoise.Horizontal.TProgressbar")

        style_liveness = ttk.Style()
        style_liveness.theme_use('alt')
        style_liveness.configure("pink.Horizontal.TProgressbar", foreground='pink',
                                 background='pink')

        self._liveness_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                      style="pink.Horizontal.TProgressbar")

        style_loud = ttk.Style()
        style_loud.theme_use('alt')
        style_loud.configure("lavender.Horizontal.TProgressbar", foreground='lavender',
                             background='lavender')

        self._loud_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                  style="lavender.Horizontal.TProgressbar")

        style_loud = ttk.Style()
        style_loud.theme_use('alt')
        style_loud.configure("green.Horizontal.TProgressbar", foreground='green',
                             background='green')

        self._speech_progress_bar = ttk.Progressbar(self.root, orient='horizontal', length=300,
                                                    style="green.Horizontal.TProgressbar")

    def run_window(self) -> None:
        """
        Runs the tkinter window which displays the link to the generated playlist,

        has an 'OPEN LINK' button which opens the link of the newly generated playlist

        At the end, there is a DID YOU KNOW?! section where the normalized song attribute
        averages of the old inputted playlist are displayed with bars
        """

        self.root.title('Spotify Recommender')

        # Format the spotify logo that will be displayed
        sp_logo = ImageTk.PhotoImage(self._image)
        label = tk.Label(self.root, image=sp_logo)

        # We need to save the reference to the image!
        label.image = sp_logo
        label.grid()

        # Make all the labels and grid() all the corresponding bars
        tk.Label(self.root, text='Here is the link to your new playlist!',
                 font=("Proxima nova", "9", "bold")).grid()
        tk.Label(self.root, text=self.link, bd=20, font=("Proxima nova", "9", "bold")).grid()

        self._link_button.grid()

        tk.Label(self.root, text="DID YOU KNOW?! \n These are your old playlist's stats:",
                 font=("Proxima nova", "9", "bold")).grid(pady=5)

        tk.Label(self.root, text=f"Avr. Acousticness: {self.old_averages['Acousticness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._acoustic_progress_bar['value'] = self.old_averages['Acousticness']
        self._acoustic_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Danceability: {self.old_averages['Danceability']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._dance_progress_bar['value'] = self.old_averages['Danceability']
        self._dance_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Energy: {self.old_averages['Energy']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._energy_progress_bar['value'] = self.old_averages['Energy']
        self._energy_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Instrumentalness: {self.old_averages['Instrumentalness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._instrument_progress_bar['value'] = self.old_averages['Instrumentalness']
        self._instrument_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Valence: {self.old_averages['Valence']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._valence_progress_bar['value'] = self.old_averages['Valence']
        self._valence_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Tempo: {self.old_averages['Tempo']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._tempo_progress_bar['value'] = self.old_averages['Tempo']
        self._tempo_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Liveness: {self.old_averages['Liveness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._liveness_progress_bar['value'] = self.old_averages['Liveness']
        self._liveness_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Loudness: {self.old_averages['Loudness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._loud_progress_bar['value'] = self.old_averages['Loudness']
        self._loud_progress_bar.grid(pady=5)

        tk.Label(self.root, text=f"Avr. Speechiness: {self.old_averages['Speechiness']}",
                 font=("Proxima nova", "9", "bold")).grid(pady=0)
        self._speech_progress_bar['value'] = self.old_averages['Speechiness']
        self._speech_progress_bar.grid(pady=5)

    def open_link(self) -> None:
        """Function that is used to be the command for the button of the tkinter window to go
        to the link of the new playlist

        It uses the webbrowser module to open a new tab in your browser
        """

        webbrowser.open_new(self.link)


if __name__ == "__main__":

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pickle', 'tkinter', 'PIL', 'urllib', 'webbrowser',
                          'Recommendation', 'Spotify.Spotify_client', 'Spotify.song_features',
                          'k_means'],
        'allowed-io': ['get_user_input', 'visualize'],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
