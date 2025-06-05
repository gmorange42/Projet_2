import sys
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))
sys.path.append(path + '\\\\csv')
sys.path.append(path + '\\\\tools')
import pandas as pd
import get_tmdb


#import table title_basics_clean
df_movies = pd.read_csv(path + "\\\\csv\\\\title_basics.csv.zip")

#importer table de title_ratings_clean
df_ratings = pd.read_csv(path + "\\\\csv\\\\title_ratings.csv.zip")

#merge des dataframes df_movies et df_rating'
df_movies = pd.merge(left=df_movies, right=df_ratings, how='inner', on='tconst')

#on supprime le dataframe df_ratings qui devient inutile
del df_ratings

#importer table akas
df_akas= pd.read_csv(path + "\\\\csv\\\\title_akas.csv.zip")

#rename titleId en tconst sur df_akas
df_akas.rename(columns={'titleId': 'tconst'}, inplace=True)

#merge des tables df_movies et df_akas
df_movies = pd.merge(left=df_movies, right=df_akas, how='inner', on='tconst')

#on supprime le dataframe df_akas qui devient inutile
del df_akas

#suppression de la colonne region
df_movies.drop(columns=['region'], inplace=True)

#creation de la table tmdb
df_tmdb = get_tmdb.create_tmdb(df_movies)

#rename de la colonne imdb_id pour prendre le meme nom que celle dans le dataframe imdb (tconst)
df_tmdb = df_tmdb.rename(columns={'imdb_id': 'tconst'})

#on merge la table de titres de films et de tmdb
df_movies = pd.merge(left=df_movies, right=df_tmdb, how='inner', on='tconst')

#on filtre les films en fonction de leurs startYear et origin_country
df_movies = df_movies[((df_movies['startYear'] >= 1950) & (df_movies['origin_country'].astype(str).str.contains('FR')) |
                       ((df_movies['startYear'] >= 1960) & (df_movies['origin_country'].astype(str).str.contains('US'))))]


#on supprime le dataframe df_tmdb qui devient inutile
del df_tmdb

#on ajoute le debut de l'URL sur le poster_path
df_movies['poster_path'] = df_movies['poster_path'].apply(lambda x : 'https://image.tmdb.org/t/p/original' + x)


#On stock dans une liste les titres qui apparaissent plusieur fois (films ayant le meme nom)
multi_titles = []
for (k,v) in df_movies.title.value_counts().items():
    if v > 1:
        multi_titles.append(k)

#On ajouter la date de sortie au titre du film si celui si apparrait plusieur fois
df_movies['title'] = df_movies.apply(lambda x : x['title'] + f" ({x['startYear']})" if x['title'] in multi_titles else x['title'],axis=1)

#on enregistre le dataframe sous forme de csv zipper
df_movies.to_csv(path + "\\\\csv\\\\movies.csv.zip", index=False, compression='zip')

del df_movies