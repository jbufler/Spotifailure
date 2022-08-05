from Evaluation import *
from Setup_file import *
from user_data import *


if __name__ == "__main__":

    # initializing user 
    user = Setup(c_id, c_secret, redirect)
    sp = user.getSpotifyInstance()
    df1 = user.top_genre_extraction()
    print(user.get_current_user())

    user2 = Setup(c_id2, c_secret2, redirect2)
    sp2 = user2.getSpotifyInstance()

    # initializing feature data frames 
    df2 = user2.top_genre_extraction()
    print(user2.get_current_user())

    # Demonstrating the functionalities of the evaluation file:
    popularity(df1)
    matplotlib(df1)
    # heatmap not working? Jule fragen 
    seaborn_heatmap(df1)
    artist_chart(df1)
    playlist_generation(df1, df2, username, user.getSpotifyInstance(), user2.getSpotifyInstance())
