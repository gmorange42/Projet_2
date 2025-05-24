import pandas as pd
from pathlib import Path
path = str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')

df_movies       = pd.read_csv(path + "\\\\csv\\\\movies.csv.zip")
df_api_videos   = pd.read_csv(path + "\\\\csv\\\\api_movies_videos.csv.zip")
df_api_keywords = pd.read_csv(path + "\\\\csv\\\\api_movies_keywords.csv.zip")

df_merge_movies = pd.merge(left=df_movies, right=df_api_keywords, how='inner', left_on='id', right_on='tmdb_id')
df_merge_movies = pd.merge(left=df_merge_movies, right=df_api_videos, how='left', left_on='id', right_on='tmdb_movie_id')

df_merge_movies.drop(columns=['id', 'tmdb_movie_id'], inplace=True)
df_merge_movies.rename(columns={'tconst': 'imdb_id'}, inplace=True)
df_merge_movies = df_merge_movies[['imdb_id', 'tmdb_id', 'originalTitle', 'startYear', 'runtimeMinutes', 'genres',
                                  'averageRating', 'numVotes', 'belongs_to_collection', 'budget', 'revenue',
                                  'origin_country', 'overview', 'popularity', 'poster_path',
                                  'keywords_name', 'video_link']]

df_merge_movies.to_csv(path + "\\\\final_csv\\\\merge_movies.csv.zip", index=False, compression='zip')