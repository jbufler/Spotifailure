# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd



def top_genre_extraction(c_id,c_secret,redirect):
    
    scopes = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=c_id,
                                                   client_secret=c_secret,
                                                   redirect_uri=redirect,
                                                   scope=scopes))
    top = sp.current_user_top_tracks()
    
    
    track_info_cols = ['id', 'genre', 'track_name', 'artist', 'artist_uri', 'album', 'release_date', # Track info
                      'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'] # Audio features
    

    
    song_df = pd.DataFrame(columns=track_info_cols)
    for track in top['items']:
        artists = track['artists']
        album_name = track['album']['name']
        release_date = track['album']['release_date']
        track_name = track['name']
        audio_features = sp.audio_features(track['uri'])[0] 
        track_id = track['id']
        currentArtist = []
        currentArtistURI = []
    
        for artist in artists:
            artist_name = artist['name']
            artist_uri = artist['uri']
    
            genres = sp.artist(artist_uri)['genres']
            currentArtist.append(artist_name)
            currentArtistURI.append(artist_uri)
            currentGenre = []
    
            for genre in genres:
                    # Add info to dictionary
                    currentGenre.append(genre)
    
        row = {'id' : track_id,
               'genre' : currentGenre,
              'track_name' : track_name,
              'artist' : currentArtist,
              'artist_uri' : currentArtistURI,
              'album' : album_name,
              'release_date' : release_date 
              }
        # Need to create a dictionary for the audio features
        audio_feature_dict = {key: value for key, value in audio_features.items() if key in track_info_cols}
    
        # Combine the above row and audio_feature_dict into one
        row.update(audio_feature_dict)
    
        song_df = song_df.append(row,ignore_index=True)
    
    
    song_df.to_csv(f'./top_song_genres.csv', 
               mode='a', 
               index=False)
