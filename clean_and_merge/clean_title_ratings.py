import pandas as pd
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))

#import ratings tsv
df = pd.read_csv("https://datasets.imdbws.com/title.ratings.tsv.gz", sep="\t")

#on ne garde que les lignes avec un averageRating >= 6 et avec un numVotes >= 1000
condition = (df["averageRating"]>=6.9) & (df["numVotes"] >=1000)
df_new = df[condition]
df_new = df_new.set_index("tconst")

#creation du csv
df_new.to_csv(path + "\\\\csv\\\\title_ratings.csv.zip", sep=",", compression='zip')
del df_new
del df