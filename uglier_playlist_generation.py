# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 12:32:20 2022

@author: Jule
"""

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

df1 = pd.read_csv('C:/Users/Jule/University/4. Semester/Python/Spotifailure/data/song_genres.csv')
df2 = pd.read_csv('C:/Users/Jule/University/4. Semester/Python/Spotifailure/data/top_song_genres.csv')
    
df = df1.merge(df2, how = 'inner' ,indicator=False)

df1new  = pd.merge(df1, df, how='left', indicator='Exist')
df1new  = df1new .loc[df1new ['Exist'] != 'both']
df1new.drop(columns=['Exist'], inplace=True) 

df2new  = pd.merge(df2, df, how='left', indicator='Exist')
df2new  = df2new .loc[df2new ['Exist'] != 'both']
df2new.drop(columns=['Exist'], inplace=True) 

dfa = df1new.merge(df2new, how = 'inner' ,indicator=False, on = ["artist"])
dfa.columns = dfa.columns.str.rstrip("_x")
dfa = dfa.drop_duplicates(subset= ["track_name"])
dfa = dfa.drop(dfa.columns[18:],axis=1)

df1new  = pd.merge(df1new, dfa, how='left', indicator='Exist')
df1new  = df1new .loc[df1new ['Exist'] != 'both']
df1new.drop(columns=['Exist'], inplace=True) 

df2new  = pd.merge(df2new, dfa, how='left', indicator='Exist')
df2new  = df2new .loc[df2new ['Exist'] != 'both']
df2new.drop(columns=['Exist'], inplace=True) 

dfb = vertical_concat = pd.concat([df, dfa], axis=0)

while len(dfb) < 15 and len(df) > 0 and len(dfa) > 0:
    dfb = vertical_concat = pd.concat([dfb, dfa.head(1)], axis=0)
    dfb = vertical_concat = pd.concat([dfb, df.head(1)], axis=0)
    dfa.drop(index=dfa.index[0], axis=0, inplace=True)
    df.drop(index=df.index[0], axis=0, inplace=True)
    
    

scope = 'playlist-modify-public'
username = "bv7dt6v5tgogie1if0rjxlpt2"
redirect = "https://127.0.0.1:8080"
c_id =  "a8f23dd95faa48f489232cd9b03d1474"
c_secret =  "b38f603ff7d745de85fc79f5c19bac04"

token = SpotifyOAuth(scope=scope, username=username,client_id=c_id,client_secret=c_secret,redirect_uri=redirect)
spotObject = spotipy.Spotify(auth_manager = token)

playlist_name = "Spotipy Merge"
playlist_description = "This is a with python generated merge of my top songs and recently played ones"

newPlaylist = spotObject.user_playlist_create(user=username,name=playlist_name,public = True, description = playlist_description)
identification = newPlaylist["id"]

songList = list(dfb.id)

spotObject.user_playlist_add_tracks(user=username,playlist_id=identification,tracks = songList)