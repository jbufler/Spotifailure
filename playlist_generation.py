from numpy import outer
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Setup_file import *

# vorerst drinlassen!!! 

# TODO: alle funktionen in evaluation in einer separaten main klasse antesten und ausführen. 
# von da aus den user input? 

def playlist_generation(df1, df2, username,sp, sp_2, playlist_max_length = 20):
    
    

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
    username = "31ta2dool2ticjyjjqe77gqxwkku"
    c_id = "14cf301b12844b78b644bb4a52db0423"
    c_secret = "71b96d7dae04418192c74ec273467b5a"
    redirect = "http://localhost:8888/callback/"

    n = Setup(c_id, c_secret, redirect, scope='playlist-modify-public')
    sp = n.getSpotifyInstance()


    # second user my data 
    c_id =  "70542e66da8543619ed08f275dd12f57"
    c_secret =  "9e9eb08d496643cfbb20d3e52295eb42"
    redirect = "http://localhost:8888/callback/"
    username_2 = "goody931"

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

# test data ####################################
username = "31ta2dool2ticjyjjqe77gqxwkku"
c_id = "14cf301b12844b78b644bb4a52db0423"
c_secret = "71b96d7dae04418192c74ec273467b5a"
redirect = "http://localhost:8888/callback/"
user = Setup(c_id, c_secret, redirect)
t_sp = user.getSpotifyInstance()
df1 = user.top_genre_extraction()
################################################

# my data ######################################
c_id =  "70542e66da8543619ed08f275dd12f57"
c_secret =  "9e9eb08d496643cfbb20d3e52295eb42"
redirect = "http://localhost:8888/callback/"
setup = Setup(c_id, c_secret, redirect)
df2 = setup.top_genre_extraction()
################################################


playlist_generation(df1, df2, username, user.getSpotifyInstance, setup.getSpotifyInstance, 20)

