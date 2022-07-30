# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 11:40:15 2022

@author: Jule
"""

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth



def playlist_generation(filepath1,filepath2,username,redirect,c_id,c_secret,playlist_max_length = 20):
    df1 = pd.read_csv(filepath1)
    df2 = pd.read_csv(filepath2)
    
    #find identical values in both datasets
    identical = df1.merge(df2, how = 'inner' ,indicator=False)
    
    #remove identical values in both dataframes
    df1  = pd.merge(df1, identical, how='left', indicator='Exist')
    df1  = df1.loc[df1 ['Exist'] != 'both']
    df1.drop(columns=['Exist'], inplace=True) 
    
    df2  = pd.merge(df2, identical, how='left', indicator='Exist')
    df2  = df2 .loc[df2 ['Exist'] != 'both']
    df2.drop(columns=['Exist'], inplace=True) 
    
    #find same artists in both playlist
    dfa = df1.merge(df2, how = 'inner' ,indicator=False, on = ["artist"])
    dfa.columns = dfa.columns.str.rstrip("_x")
    dfa = dfa.drop_duplicates(subset= ["track_name"])
    dfa = dfa.drop(dfa.columns[18:],axis=1)
    
    #remove those values from the dataframes
    
    df1  = pd.merge(df1, dfa, how='left', indicator='Exist')
    df1  = df1 .loc[df1 ['Exist'] != 'both']
    df1.drop(columns=['Exist'], inplace=True) 
    
    df2  = pd.merge(df2, dfa, how='left', indicator='Exist')
    df2  = df2.loc[df2 ['Exist'] != 'both']
    df2.drop(columns=['Exist'], inplace=True) 
    
    #merge identical and artist dataframe
    
    df = pd.concat([identical, dfa], axis=0)
    
    while len(df) < playlist_max_length and len(identical) > 0 and len(dfa) > 0:
        df = pd.concat([df, dfa.head(1)], axis=0)
        df = pd.concat([df, identical.head(1)], axis=0)
        dfa.drop(index=dfa.index[0], axis=0, inplace=True)
        df.drop(index=df.index[0], axis=0, inplace=True)
        
    

    scope = 'playlist-modify-public'
    
    token = SpotifyOAuth(scope=scope, username=username,client_id=c_id,client_secret=c_secret,redirect_uri=redirect)
    sp = spotipy.Spotify(auth_manager = token)
    
    playlist_name = "Spotipy Merge"
    playlist_description = "merged"
    
    newPlaylist = sp.user_playlist_create(user=username,name=playlist_name,public = True, description = playlist_description)
    identification = newPlaylist["id"]
    songList = list(df.id)
    sp.user_playlist_add_tracks(user=username,playlist_id=identification,tracks = songList)


import os
myfile=".cache-goody931"

## If file exists, delete it ##
if os.path.isfile(myfile):
    os.remove(myfile)
    
c_id =  "70542e66da8543619ed08f275dd12f57"
c_secret =  "9e9eb08d496643cfbb20d3e52295eb42"
redirect = "http://localhost:8888/callback/"
playlist_generation('top_song_genres_Jule.csv', 'top_song_genres_Lisa.csv', 'goody931', redirect, c_id, c_secret )