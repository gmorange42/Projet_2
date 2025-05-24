import pandas as pd
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))

df_principals   = pd.read_csv(path + "\\\\csv\\\\title_principals.csv.zip")
df_name         = pd.read_csv(path + "\\\\csv\\\\name_basics.csv.zip")

df = pd.merge(left=df_principals, right=df_name, how='inner', on='nconst')
df.drop(columns=['tconst'], inplace=True)

df.drop_duplicates(inplace=True)

df.to_csv(path + "\\\\csv\\\\name_basics.csv.zip", index=False, compression='zip')
del df_name
del df
del df_principals
