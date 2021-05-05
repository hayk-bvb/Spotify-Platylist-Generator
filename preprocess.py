"""
CSC111 Final Project: Playlist Generator

Module Description
==================
Script for preprocessing the input data from kaggle.
The raw data can be found at:
https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks?select=data.csv

This file is meant to normalize the raw dataset to be usable for later computations.
Most of the script in this file is run before the main program with the exception of the Data
class. The Data class is used across modules to normalize any attributes for songs that were not
originally in the dataset.

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
import pandas as pd


class Data:
    """
    A class to store the the un-normalized music data for normalization purposes.
     This class is used to normalize new song data in the post_cluster module
     """
    data: pd.DataFrame

    def __init__(self) -> None:
        """
        Initializes a object that stores the music data as a pandas dataframe. Contains
        function to normalize any new data based on data in our dataset.
        """
        self.data = pd.read_csv('Data/music_data.csv')

    def normalize_value(self, pos: list) -> list:
        """
        Normalizes a list of values based on the data in our dataset. Return a new list of
        normalized values, doesn't not mutate the original

        Preconditions:
            - pos is a list of floats that is ordered so that each element represents the following:
                [acousticness, danceability, energy, duration_ms, instrumentalness, valence, tempo,
                liveness, loudness, speechiness, key]

        >>> data = Data()
        >>> input = [0.991, 0.598, 0.224, 168333, 0.000522, 0.634, 149.976, 0.379, -12.628, 0.0936, 5]
        >>> normalized = data.normalize_value(input)
        >>> normalized == [0.991, 0.598, 0.224, 0.030636568095376935, 0.000522, 0.634, 0.6159001589276694, 0.379, 0.7418682953566674, 0.0936, 0.45454545454545453]
        True
        """
        duration = pos[3]
        tempo = pos[6]
        loudness = pos[8]
        key = pos[10]

        normalized_duration = (duration - self.data['duration_ms'].min()) / \
                              (self.data['duration_ms'].max() - self.data['duration_ms'].min())
        normalized_tempo = (tempo - self.data['tempo'].min()) / \
                           (self.data['tempo'].max() - self.data['tempo'].min())
        normalized_loudness = (loudness - self.data['loudness'].min()) / \
                              (self.data['loudness'].max() - self.data['loudness'].min())
        normalized_key = (key - self.data['key'].min()) / \
                         (self.data['key'].max() - self.data['key'].min())

        return pos[:3] + [normalized_duration] + pos[4:6] + \
            [normalized_tempo] + [pos[7]] + [normalized_loudness] + [pos[9]] + [normalized_key]


def normalize_df(df: pd.DataFrame, column_name: str) -> None:
    """
    Normalizes every value in the specified column in the dataframe.

    The normalization is done by finding the min and max value in the column and
    then subtracting every value in by min and dividing by max-min.

    Preconditions:
        - column_name in df.keys()
        - columns only have numerical values stored in them
    """
    min_val = df[column_name].min()
    max_val = df[column_name].max() - min_val

    df[column_name] -= min_val
    df[column_name] /= max_val


def preprocess_data(file_name: str, columns_to_reorder: list, columns_to_normalize: list,
                    processed_name: str, new_file: bool = False) -> pd.DataFrame:
    """
    Reads the .csv file stored a Data/file_name and then reorders and normalizes the
    columns. A new .csv file is generated named 'normalized_{file_name}.csv in the Data folder.
    This file will also reorganize the columns of the data so that it is easier to access
    the required data and remove the release_date column.
    Specifically, from left to right, the columns will be organized as follows:
        1. id
        2. acousticness (Ranges from 0 to 1)
        3. danceability (Ranges from 0 to 1)
        4. energy (Ranges from 0 to 1)
        5. duration_ms (Integer typically ranging from 200k to 300k)
        6. instrumentalness (Ranges from 0 to 1)
        7. valence (Ranges from 0 to 1)
        8. tempo (Float typically ranging from 50 to 150)
        9. liveness (Ranges from 0 to 1)
        10. loudness (Float typically ranging from -60 to 0)
        11. speechiness (Ranges from 0 to 1)
        12. key

    Preconditions:
        - file_name is a .csv file in the Data folder
        - file_name is formatted as specified on the database website at top of file
    """
    file_path = 'Data/' + file_name
    music_df = pd.read_csv(file_path)
    df_reorder = music_df.reindex(columns=columns_to_reorder)
    for column in columns_to_normalize:
        normalize_df(df_reorder, column)
    if new_file:
        df_reorder.to_csv('Data/normalized_' + processed_name, index=False)
    return df_reorder


if __name__ == "__main__":
    file = "music_data.csv"
    columns_titles = ["id", "name", "artists", "year", "explicit", "mode", "acousticness",
                      "danceability", "energy", "duration_ms", "instrumentalness", "valence",
                      "popularity", "tempo", "liveness", "loudness", "speechiness", "key"]
    columns_dropped_titles = ["year", "acousticness",
                              "danceability",
                              "energy", "duration_ms", "instrumentalness", "valence", "popularity",
                              "tempo", "liveness", "loudness", "speechiness", "key"]

    columns_more_dropped_titles = ['id', "acousticness", "danceability", "energy", "duration_ms",
                                   "instrumentalness", "valence", "tempo", "liveness", "loudness",
                                   "speechiness", "key"]

    columns_to_normalize = ['duration_ms', 'tempo', 'loudness', 'key']
    # The following function was the one we called to normalize and format our raw data:
    # preprocess_data(file, columns_more_dropped_titles, columns_to_normalize,
    # 'music_data.csv', True)

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pandas'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that
        # call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
