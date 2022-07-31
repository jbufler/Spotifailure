import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.io import show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from math import pi
from Setup_file import *


def popularity(df):

    """
    measure the average popularity of entered songs, calculates how obscure the playlist is and prints it
    gives back top 5 most popular and unpopular songs
  
  
    Parameters:
    df (DataFrame): Dataframe of songs containing column measuring the popularity
  
    Returns:
    print
    obscure score
    top 5 most popular songs in Playlist
    top 5 most unpopular songs
  
    """
    #get popularity of songs, calculate mean popularity
    popular = list(df['popularity'])
    mean = round(np.mean(popular))
    #obscurity is the opposite of popularity, to calculate the obsurity percentage calculate 100-popularity
    obscure = 100 - mean
    print("your playlist is ",obscure,"% obscure")

    #get inidces of rows for most and least popular songs
    number = 5
    highindices = sorted(range(len(popular)), key = lambda sub: popular[sub])[-number:]
    lowindices = sorted(range(len(popular)), key = lambda sub: popular[sub])[:number]

    #initialize the two strings
    highString = ""
    lowString = ""
    for i in range(number):
        #append the top songs to string, starting with most popular which is last in the idices
        highindex = highindices[number-1-i]
        highObj = df.iloc[highindex]
        highString = highString + "\n" + highObj["track_name"] + " by " + highObj["artist"][0]
        
        #append the least popular songs to string, starting with most unpopular which is first in the idices
        lowindex = lowindices[i]
        lowObj = df.iloc[lowindex]
        lowString = lowString + "\n" + lowObj["track_name"] + " by " + lowObj["artist"][0]
    
        
    print("your most popular tracks are: ", highString,"\n", "your least popular tracks are: ", lowString)
 


def matplotlib(df): 
    
    """
    Gives out a visualization of audio features, one spider web chard and bar grapgh 
  
    Parameters:
    df (DataFrame): Dataframe containing the extracted audio features
  
    Returns:
    prints a spider web chart and bar graph showing audio features mapped
  
    """
    
    #get audio features from dataFrame by removing all other columns
    df = df.drop(df.loc[:, 'id':'popularity'].columns, axis=1)
    #scale tempo down
    df['tempo'] = df['tempo']/100
    #get labels and mean values from dataFrame
    labels = list(df)[:]
    features = df.mean().tolist()

    #create the spiderweb graph
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    fig = plt.figure(figsize = (15,15))

    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, features, '*', linewidth=2, color= 'green')
    ax.fill(angles, features, alpha=0.3, color='green')
    ax.set_thetagrids(angles * 180/np.pi, labels , fontsize = 12)

    #create the barplot
    fig, ax=plt.subplots(dpi=100)
    plt.bar(labels, features,color='green',alpha=0.3)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    ax.set_xticklabels(labels=labels,rotation=90);
    barplot = plt.show()


def seaborn_heatmap(df):
    
    """
    A seaborn heatmap showing correlating audio features
  
    Parameters:
    df (DataFrame): Dataframe containing the extracted audio features
  
    Returns:
    prints a heatmap
  
    """
    # heatmap of audio features 
    sns.set()
    corr = df.corr()
    sns.heatmap(corr, annot=True).set_title('Pearson correlation matrix')
    plt.show()


def artist_chart(df): 
    """
    Creates a Pie chart of the most listened to artists of input dataframe
  
    Parameters:
    df (DataFrame): Dataframe containing the extracted artists
  
    Returns:
    print pie chart of artists most listened to
  
    """
    
    # Donut - 'Number of tracks by artist'
    print(df['artists'])
    artists_songs_df = df['artists'].value_counts()[:20]
    print(artists_songs_df)
    data = pd.Series(artists_songs_df).reset_index(name='value').rename(columns={'index':'artists'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(artists_songs_df)]
    z=110*(data['value']/data['value'].sum())
    data['value']=z


    p = figure(plot_height=350, title="", toolbar_location=None,
            tools="hover", tooltips="@artists: @value{0.2f} %", x_range=(-.5, .5))

    p.annular_wedge(x=0, y=1,  inner_radius=0.15, outer_radius=0.25, direction="anticlock",
                    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_label='Artists', source=data)

    show(p)


def playlist_generation(df1, df2, username1,username2,sp, sp_2, playlist_max_length = 20):
    """
    Create a Playlist directly in Spotify on two accountns merged from two input playlists
  
    Parameters:
    df1 (DataFrame): Dataframe of first users Playlist
    df2 (DataFrame): Dataframe of second users Playlist
    
    username1 (string): String containing Spotify Username of first user
    username2 (string): String containing Spotify Username of second user
    
    sp(spotipy Objects): spotipy object containing current authorization and scope of first user
    sp_2(spotipy Objects): spotipy object containing current authorization and scope of second user
    
    playlist_max_length (int): maximum length of playlist
  
    Returns:
    int: Description of return value
  
    """

    print("merging the data frames....")
    df = pd.read_csv("top_song_genres_Lisa.csv")
    df1 = df1.drop("popularity", axis=1)
    df2 = df2.drop("popularity", axis=1)
    df1["genre"] = df1['genre'].apply(lambda x: ','.join(map(str, x)))
    df1["artist"]= df1["artist"].apply(lambda x: ','.join(map(str, x)))
    df1["artist_uri"]= df1["artist_uri"].apply(lambda x: ','.join(map(str, x)))
    df2["genre"] = df2['genre'].apply(lambda x: ','.join(map(str, x)))
    df2["artist"]= df2["artist"].apply(lambda x: ','.join(map(str, x)))
    df2["artist_uri"]= df2["artist_uri"].apply(lambda x: ','.join(map(str, x)))
    #print(df1.columns)
    # find identical values in both datasets
    identical = df1.merge(df2, how= "inner" ,indicator=False)
    
    # remove identical values in both dataframes
    df1  = pd.merge(df1, identical, how='left', indicator='Exist')
    df1  = df1.loc[df1 ['Exist'] != 'both']
    df1.drop(columns=['Exist'], inplace=True) 
    
    df2  = pd.merge(df2, identical, how='left', indicator='Exist')
    df2  = df2 .loc[df2 ['Exist'] != 'both']
    df2.drop(columns=['Exist'], inplace=True) 
    
    # find same artists in both playlist
    dfa = df1.merge(df2, how = 'inner' ,indicator=False, on = ["artist"])
    dfa.columns = dfa.columns.str.rstrip("_x")
    dfa = dfa.drop_duplicates(subset= ["track_name"])
    dfa = dfa.drop(dfa.columns[18:],axis=1)
    
    # remove those values from the dataframes  
    df1  = pd.merge(df1, dfa, how='left', indicator='Exist')
    df1  = df1 .loc[df1 ['Exist'] != 'both']
    df1.drop(columns=['Exist'], inplace=True) 
    
    df2  = pd.merge(df2, dfa, how='left', indicator='Exist')
    df2  = df2.loc[df2 ['Exist'] != 'both']
    df2.drop(columns=['Exist'], inplace=True) 
    
    # merge identical and artist dataframe 
    df = pd.concat([identical, dfa], axis=0)
    
    while len(df) < playlist_max_length and len(identical) > 0 and len(dfa) > 0:
        df = pd.concat([df, dfa.head(1)], axis=0)
        df = pd.concat([df, identical.head(1)], axis=0)
        dfa.drop(index=dfa.index[0], axis=0, inplace=True)
        df.drop(index=df.index[0], axis=0, inplace=True)
        
    
    #scope = 'playlist-modify-public'
    
    #token = SpotifyOAuth(scope=scope, username=username,client_id=c_id,client_secret=c_secret,redirect_uri=redirect)
    #sp = spotipy.Spotify(auth_manager = token)

    print("Logging in of the user....")
    playlist_name = "Spotipy Merge"
    playlist_description = "merged"
    

    # first user - testdata 
    username1 = "31ta2dool2ticjyjjqe77gqxwkku"
    c_id = "14cf301b12844b78b644bb4a52db0423"
    c_secret = "71b96d7dae04418192c74ec273467b5a"
    redirect = "http://localhost:8888/callback/"

    n = Setup(c_id, c_secret, redirect, scope='playlist-modify-public')
    sp = n.getSpotifyInstance()


    # second user my data 
    c_id =  "70542e66da8543619ed08f275dd12f57"
    c_secret =  "9e9eb08d496643cfbb20d3e52295eb42"
    redirect = "http://localhost:8888/callback/"
    username2 = "goody931"

    n_2 = Setup(c_id, c_secret, redirect, scope='playlist-modify-public')
    sp_2 = n_2.getSpotifyInstance()

    # checking if there is already a playlist called "Spotipy Merge" in your profile
    def no_double_named(sp, username):
        playlists = sp.user_playlists(user=username,limit=50, offset=0) 
        for i in range(0,len(playlists["items"])):
            playlist_n = playlists["items"][i]["name"]
            # if yes just replace the tracks in the existing playlist 
            if playlist_n == playlist_name:
                sp.user_playlist_replace_tracks(user=username, playlist_id=playlists["items"][i]["id"], tracks= list(df.id))
                return 0
                
        # else create a new playlist and put in tracks  
        user = sp.current_user()
        displayName = user['display_name']
        print(displayName)
        newPlaylist = sp.user_playlist_create(user=username,name=playlist_name,public = True, description = playlist_description)
        identification = newPlaylist["id"]
        songList = list(df.id)
        sp.user_playlist_add_tracks(user=username,playlist_id=identification,tracks = songList)

    print("creating the playlists....")
    no_double_named(sp, username)
    no_double_named(sp_2, username_2)