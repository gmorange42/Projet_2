import pandas as pd
import sys
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))
sys.path.append(path + '\\\\tools')
import call_api_thread as cath


with open(path + '////tmdb_api_key', 'r') as file:
    key = file.read()

headers = {
    "accept": "application/json",
    "Authorization": key
}


#https://api.themoviedb.org/3/movie/{movie_id}/keywords
df_movies= pd.read_csv(path + "\\\\csv\\\\movies.csv.zip")

df_movies_keywords = cath.url_to_dataframe('https://api.themoviedb.org/3/movie/', list(df_movies['tconst']), '/keywords?language=fr-FR', headers, record_path='keywords', meta='id', meta_prefix='parents_')

df_movies_keywords.rename(columns={'name': 'keywords_name' ,'parents_id': 'tmdb_id'}, inplace=True)
df_movies_keywords.drop(columns=['id'], inplace=True)
df_movies_keywords = pd.pivot_table(df_movies_keywords, values='keywords_name', index='tmdb_id', aggfunc=list)
df_movies_keywords['tmdb_id'] = df_movies_keywords.index
df_movies_keywords = df_movies_keywords[['tmdb_id', 'keywords_name']]
df_movies_keywords.to_csv(path + "\\\\csv\\\\api_movies_keywords.csv.zip", index=False, compression='zip')
del df_movies
del df_movies_keywords
