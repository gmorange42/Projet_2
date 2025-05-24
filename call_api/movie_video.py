import pandas as pd
import sys
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))
sys.path.append(path + '\\\\tools')
import call_api_thread as cath

with open(path + '\\\\tmdb_api_key', 'r') as file:
    key = file.read()

headers = {
    "accept": "application/json",
    "Authorization": key
}

df_movies= pd.read_csv(path + "\\\csv\\\\movies.csv.zip")

#https://api.themoviedb.org/3/movie/{movie_id}/videos
df_movies_videos= cath.url_to_dataframe('https://api.themoviedb.org/3/movie/', list(df_movies['tconst']), '/videos?language=fr-FR', headers, record_path='results', meta='id', meta_prefix='parents_')
df_movies_videos = df_movies_videos[['parents_id', 'type', 'key']]
df_movies_videos.rename(columns={'parents_id': 'tmdb_movie_id', 'key': 'video_link'}, inplace=True)
df_movies_videos['video_link'] = df_movies_videos['video_link'].apply(lambda x : 'https://www.youtube.com/watch?v=' + x)
df_movies_videos['prio'] = df_movies_videos['type'].apply(lambda x : 1 if x == 'Trailer' else (1 if x == ['Teaser'] else 0))
df_movies_videos.sort_values(by=['tmdb_movie_id', 'prio'], inplace=True)
df_movies_videos = df_movies_videos.groupby(['tmdb_movie_id'], as_index=False).first()
df_movies_videos.drop(columns=['type', 'prio'], inplace=True)
df_movies_videos.to_csv(path + "\\\\csv\\\\api_movies_videos.csv.zip", index=False, compression='zip')
del df_movies