import pandas as pd
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))

df_movies       = pd.read_csv(path + "\\\\csv\\\\movies.csv.zip")
df_principals   = pd.read_csv(path + "\\\\csv\\\\title_principals.csv.zip")


df = pd.merge(left=df_movies, right=df_principals, how='inner', on='tconst')
df = df[['tconst', 'nconst', 'category']]
df.to_csv(path + "\\\\csv\\\\title_principals.csv.zip", index=False, compression='zip')
