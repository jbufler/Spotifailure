## What we learned/struggled with 

Through the project, we have better understood how to handle data frames and work with virtual environments and Web APIs. 
We struggled a bit with getting to know the spotipy library since neither of us had experience working with this particular one. An issue, in the beginning, was also that at first, we struggled with authenticating to users at the same time, we were unable to delete the first authentication so any afterwards were overwritten. We spent a lot of time finding a solution, from setting up virtual environments with flask or extracting the playlists as CSV files. But of course, in the end, the solution is always the simplest answer, the problem lies in the browser automatically authenticating once you were logged in so all that was needed to solve this issue was to simply always display the authorisation page instead of automatic authorisation. We also then had to decide how to handle user input since we don't just accept a CSV file but rather want flexible login options so we had the opportunity to learn more about the kivy library and give our python code a visually pleasing way of interaction with the user. 
In general, we learned how to work with libraries we had no prior knowledge of and gained more experience with data frame handling.


## Libraries we worked with 
- NumPy 
- pandas
- matplotlib
- seaborn
- bokeh
- math 
- kivy

## Prerequisites:
- All libraries installed
- Python 3.10

Enter your information into the user_data file:

- Get Client Id and client secret:
Go to Spotify Applications and create an App
https://developer.spotify.com/dashboard/applications
There you find your Client Id and Client Secret
- Under Edit Settings, you need to enter a redirect, for example: https://127.0.0.1:8080/

- Find Spotify username
https://www.spotify.com/de/account/overview/

- Find Playlist URI:
Click on a spotify playlist, find the options symbol(three dots) and hover over share. There should be two options "Share Playlist" and "Embed Playlist". If you press Ctrl while overing over share, "Share Playlist" transforms into copy Spotify URI

## How to work with our code 

First make sure that all information has been correctly added in user_data.
Run the File user_input to see almost all implemented functions by pressing the corresponding buttons.
Run the File Test Main to see the additional feature of shared playlist creation and all previous features.

## What our code can - functionalities 

Our code can give you a nice display which asks you how you would like to analyse and compare your data. These functionalities include the following:
- Extract a DataFrame with features about the top songs of an account
- Checking how obscure your playlist is. Measures the mean of the popularity given by Spotify and tells you the name and artist of your five most popular and unpopular songs in order
- Give you a Visualization of your average audio features in a playlist via a spider web graph and a bar plot
- Give you a seaborn heatmap showing you which audio features of your playlist and another correlate
- Give you a visualization of your most listened to artists via a Donut graph
- Shared Playlist, creates a playlist with a user-chosen name and description on two accounts. This playlist is a merge between the top songs of both users. If any Songs or artists are the same they will be prioritised otherwise the top songs of each user will be added in an alternating fashion.

## Files:

Evaluation: All implemented functionalities
Setup: Funtions for authorizing access for spotify and extracting a playlist.
TestMain: Run all functionalities available
user_data: file for entering all necessary values to access the spotify account
user_input: Run most functionalities in a nice UI


