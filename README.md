# Spotify-Platylist-Generator
A program that streamlines the generation of a new Spotify playlist full of recommended songs, based on the input of a user's existing playlist.

IMPORTANT:
Go to https://drive.google.com/drive/folders/1R0JYqXIXED6c4WoM72kluoV-G-6Khqn7, to download the zipped files, datasets, pngs, etc. necessary for the program, and then copy/paste them into the main project folder.


To run the program, open command prompt or terminal, change directory into the project folder and enter:
python main.py --graphs-file-name=Graph_Final.pickle

This will take 3-10 minutes to load.
After when using the UI, please be aware that you might have to wait an additional several minutes sometimes and thus do not close the window too early!

On your first usage, you will be redirected to a custom made website. Please copy and paste the URL of that website into the terminal and press enter, it is the Spotify API Authentication Code, this action will not be necessary in future runs.


TROUBLESHOOT SECTION:

* Do not include a playlist with a song that is not definined in Spotify, such as a song file used in Spotify from your local directory.
* If you encounter a pickling error, this is probably due to the impror unzipping of the provided files from the link above. Re-unzip all the files properly and try again!
