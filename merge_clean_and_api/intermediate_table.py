import pandas as pd
from pathlib import Path
path = str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')

df_movies = pd.read_csv(path + "\\\\final_csv\\\\merge_movies.csv.zip")
df_princi = pd.read_csv(path + "\\\\csv\\\\title_principals.csv.zip")

df_inter = pd.merge(left=df_movies, right=df_princi, how='left', left_on='imdb_id', right_on='tconst')
df_inter = df_inter[['tconst', 'nconst']]
df_inter.rename(columns={"tconst": "imdb_movie_id", "nconst": "imdb_people_id"}, inplace=True)
df_inter.to_csv(path + "\\\\final_csv\\\\inter.csv.zip", index=False, compression='zip')
del df_inter
del df_movies
del df_princi
