import pandas as pd
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))

#importe le fichier akas
df_akas = pd.read_csv("https://datasets.imdbws.com/title.akas.tsv.gz", sep='\t')

#on ne garde que les colonnes titleId et region
df_akas = df_akas[['titleId', 'region']]

#on supprime les duplicates
df_akas = df_akas.drop_duplicates()

#on ne garde que les lignes qui ont FR dans la colonne region
df_akas = df_akas[df_akas['region'] == 'FR']

df_akas.to_csv(path + "\\\\csv\\\\title_akas.csv.zip", compression='zip', index=False)
del df_akas
