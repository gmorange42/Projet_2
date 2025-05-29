import pandas as pd
from pathlib import Path
path = str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')

df_name     = pd.read_csv(path + "\\\\csv\\\\name_basics.csv.zip")
df_people   = pd.read_csv(path + "\\\\csv\\\\api_people_details.csv.zip")
df_fb       = pd.read_csv(path + "\\\\csv\\\\api_find_by_id.csv.zip")

df_merge_people= pd.merge(left=df_name, right=df_fb, how='inner', left_on='nconst', right_on='imdb_id')
df_merge_people.drop_duplicates(subset=['nconst'], inplace=True)
df_merge_people = pd.merge(left=df_merge_people, right=df_people, how='inner', left_on='tmdb_id', right_on='id')
df_merge_people['gender'] = df_merge_people['gender'].apply(lambda x : 'unknow' if x == 0 else ('Femme' if x == 1 else ('Homme' if x == 2 else 'Non-binaire')))
df_merge_people.drop(columns=['nconst', 'id', 'primaryProfession', 'name'], inplace=True)
df_merge_people = df_merge_people[['tmdb_id', 'imdb_id', 'primaryName', 'category',
                                  'knownForTitles', 'biography', 'birthday',
                                  'gender', 'place_of_birth', 'popularity', 'profile_path']]

df_merge_people.to_csv(path + "\\\\final_csv\\\\people.csv.zip", index=False, compression='zip')
del df_fb
del df_merge_people
del df_name
del df_people
