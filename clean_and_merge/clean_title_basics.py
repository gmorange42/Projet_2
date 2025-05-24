import pandas as pd
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))


#   NETTOYAGE DU DATAFRAME TITLE BASICS

#importe le fichier dans dataframe
df_movies = pd.read_csv("https://datasets.imdbws.com/title.basics.tsv.gz", sep='\t')

#suppression des colonnes 'endYear' et primaryTitle
df_movies.drop(columns=['endYear', 'primaryTitle'], inplace=True)

#convertie les '\N' en None dans toutes les colonnes
df_movies = df_movies.replace('\\N', None)

#supprime toutes les lignes contenant un None
df_movies = df_movies.dropna()

#change le dtype des colonnes numeriques
df_movies = df_movies.astype({'isAdult': 'bool', 'startYear': 'uint16', 'runtimeMinutes': 'int32'})                                  #Cast the current column to boolean

#retire toutes les lignes dont le titleType n'est pas 'movie'
df_movies = df_movies[df_movies['titleType'] == "movie"]

#retire toutes les lignes ou le isAdult == True
df_movies = df_movies[df_movies['isAdult'] == False]

#on supprime les colonnes titleType, isAdult
df_movies = df_movies.drop(columns=['titleType', 'isAdult'])

#supprime toutes les lignes ou runtimeMinutes < 80 ou > 210
df_movies = df_movies[df_movies['runtimeMinutes'] > 80]
df_movies = df_movies[df_movies['runtimeMinutes'] < 210]

#create csv !
df_movies.to_csv(path + "\\\\csv\\\\title_basics.csv.zip", index=False, compression='zip')