import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
path = str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')



df_movies = pd.read_csv(path + '\\\\final_csv\\\\merge_movies.csv.zip')

print(df_movies.columns)
# add origin language
#df_movies = df_movies[['imdb_id', 'tmdb_id', 'originalTitle', 'startYear', 'runtimeMinutes', 'genres', 'averageRating', 'popularity']]
df_movies = df_movies[['originalTitle', 'startYear', 'runtimeMinutes', 'genres', 'averageRating', 'popularity']]
print(df_movies)

df_dummies =  df_movies['genres'].str.get_dummies(sep=',')
print(df_dummies)

df_movies = pd.concat([df_movies, df_dummies], axis=1)
print(df_movies)

df_movies[['startYear', 'runtimeMinutes', 'averageRating']] = MinMaxScaler().fit_transform(df_movies[['startYear', 'runtimeMinutes', 'averageRating']])
print(df_movies)

#X = df_movies["genres"].str.get_dummies(sep=',')
#print(X)


#print(pd.get_dummies(df_movies[['originalTitle', 'genres']], columns=['genres']).sum())