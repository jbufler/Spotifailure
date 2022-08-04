import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class Setup(object):
    cid = ''
    secret = ''
    primaryUsername = ''
    scope = ''
    caches_folder = './.spotify_caches/'
    

    def __init__(self, cid, secret, redirect, scope='user-top-read'):
            Setup.cid = cid
            Setup.secret = secret
            Setup.redirect = redirect
            Setup.scope = scope

            if not os.path.exists(Setup.caches_folder):
                os.makedirs(Setup.caches_folder)
           

    def getSpotifyInstance(self):
        auth_manager = auth_manager=SpotifyOAuth(client_id=Setup.cid,
                                                    client_secret=Setup.secret,
                                                    redirect_uri=Setup.redirect,
                                                    scope=Setup.scope,                                                   
                                                    cache_path=Setup.session_cache_path(self, Setup.cid),
                                                    show_dialog=True)
                                                    
        sp = spotipy.Spotify(auth_manager=auth_manager)
        return sp


    def session_cache_path(self, c_id):
        return Setup.caches_folder + c_id

    def get_current_user(self):
        user = Setup.getSpotifyInstance(self).current_user()
        displayName = user['display_name']
        return displayName

    def top_genre_extraction(self):
        
        sp = Setup.getSpotifyInstance(self)
        top = sp.current_user_top_tracks(limit=50)
        
        
        track_info_cols = ['id', 'genre', 'track_name', 'artist', 'artist_uri', 'album', 'release_date','popularity', # Track info
                        'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'] # Audio features
        
        song_df = pd.DataFrame(columns=track_info_cols)
        for track in top['items']:
            artists = track['artists']
            album_name = track['album']['name']
            release_date = track['album']['release_date']
            track_name = track['name']
            popularity = track['popularity']
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
                'release_date' : release_date, 
                'popularity' : popularity
                }
            # Need to create a dictionary for the audio features
            audio_feature_dict = {key: value for key, value in audio_features.items() if key in track_info_cols}
        
            # Combine the above row and audio_feature_dict into one
            row.update(audio_feature_dict)

            # append ist veraltet ab der nächsten version nochmal mit concat versuchen?
            song_df = song_df.append(row,ignore_index=True)
            #song_df = pd.concat([song_df, row], ignore_index=True )

        return song_df
