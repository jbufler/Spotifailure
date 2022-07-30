import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

""" This script creates a heatmap on the basis of the genres 2 accounts heard"""
# CSV FILE VERSION

# extract genres 
filepath = "popular_genres.csv"
genres = pd.read_csv(filepath)
genres = genres.get("Genres").tolist()


# extract from accounts top 50 songs + genre 
# JULE 
filepath = "top_song_genres_Jule.csv"
top_songs = pd.read_csv(filepath)
genres_top_songs = top_songs.get("genre")
# LISA 
filepath_1 = "top_song_genres_Lisa.csv"
top_songs_l = pd.read_csv(filepath_1)
genres_top_songs_l = top_songs_l.get("genre")


def get_genres_list(genres_top_songs):
    """ This function extracts the genres from the csv file in a way that we can work with it"""
    nl = []
    for i in genres_top_songs: 
        #print(i)
        if not i == "[]": 
            z = i.strip("[")
            z= z.strip("]")
            nl.append(z)

    u = []
    for i in nl: 
        i = i.replace("'", '')
        i = i.split(",")
        u.append(i)

    u = [j for sub in u for j in sub]

    k = []
    for i in u: 
        i = i.lstrip(" ")
        k.append(i)
    
    return k


# Using helper function to get genre lists from both accounts 
genres_top_songs = get_genres_list(genres_top_songs)
genres_top_songs_l = get_genres_list(genres_top_songs_l)


def frequency_list(genres, genres_top_songs):
    """ This function counts the frequency, how often one of the genres_top_songs are 
        matching with the given top genres 
    """
    # create new data containing info about frequency of genres
    frequency_list = {x: 0 for x in genres}

    for genre in genres_top_songs: 
        if genre in genres: 
            frequency_list[genre] +=1

    return frequency_list

# Using helper function to get our frequency list 
frequency_j = frequency_list(genres, genres_top_songs) 
frequency_l = frequency_list(genres, genres_top_songs_l)

df = pd.DataFrame.from_dict(frequency_l, orient = "index")
df.columns = ["frequencies_lisa"]

df_1 = pd.DataFrame.from_dict(frequency_j, orient = "index")
df_1.columns = ["frequencies_jule"]


# Wrapping the data for the heatmap up 
result = pd.DataFrame(genres)
result.columns = ["Genres"]
result["frequ_l"] = df.get("frequencies_lisa").tolist()
result["frequ_j"] = df_1.get("frequencies_jule").tolist()
a = df.get("frequencies_lisa").tolist()
b = df_1.get("frequencies_jule").tolist()
frequencies = [x + y for x, y in zip(a,b)]
result["frequencies"] = frequencies

print(result["frequ_l"])
# PLOTTING the Heatmap 
sns.set()
result = result.pivot("Genres","frequencies", "frequencies")
ax = sns.heatmap(result, annot=True, xticklabels=True, yticklabels=True)
plt.title("Heatmap genres both accounts are listen to")
plt.show()