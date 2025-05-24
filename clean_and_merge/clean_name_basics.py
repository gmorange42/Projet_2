import pandas as pd
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))

#lire le csv name_basics via la lien
df_name_basics = pd.read_csv("https://datasets.imdbws.com/name.basics.tsv.gz", sep='\t')

# on remplace les '\N' par None
df_name_basics.replace('\\N', None, inplace=True)

# on enlève les lignes dans lesquelles on n'a pas de primary profession ou de films associés ou de primaryName
df_name_basics= df_name_basics.dropna(subset=['primaryProfession', 'knownForTitles', 'primaryName'])

#enlever les lignes quand la profession ne contient pas actor, actress, director ou writer
df_name_basics= df_name_basics[df_name_basics['primaryProfession'].str.contains('(actor|actress|director|writer)')]

#enlever les colonnes birthYear et deathYear
df_name_basics= df_name_basics.drop(['birthYear', 'deathYear'], axis=1)

#créer un csv qu'on pourra merger avec les autres
df_name_basics.to_csv(path + "\\\\csv\\\\name_basics.csv.zip", compression='zip', index=False)
del df_name_basics
