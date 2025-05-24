import pandas as pd
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))

#Importer le tsv principals
df_principals = pd.read_csv("https://datasets.imdbws.com/title.principals.tsv.gz", sep='\t')

#enlever les colonnes ordering, job et characters
df_principals = df_principals.drop(columns=['ordering', 'job', 'characters'])

#garder que les lignes ou category == 'director', 'writer', 'actress', 'actor'
df_principals = df_principals[(df_principals['category'] == 'director') |
                              (df_principals['category'] == 'writer') |
                              (df_principals['category'] == 'actress') |
                              (df_principals['category'] == 'actor')]

#suppression des duplicates
df_principals = df_principals.drop_duplicates()

#creation du csv
df_principals.to_csv(path + '\\\\csv\\\\title_principals.csv.zip', index=False, compression='zip')
del df_principals