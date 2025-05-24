import pandas as pd
import sys
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))
sys.path.append(path + '\\\\tools')
import call_api_thread as cath


with open(path + '\\\\tmdb_api_key', 'r') as file:
    key = file.read()

headers = {
    "accept": "application/json",
    "Authorization": key
}

#https://api.themoviedb.org/3/person/{person_id}
df_fb= pd.read_csv(path + "\\\\csv\\\\api_find_by_id.csv.zip")

df_people_details = cath.url_to_dataframe('https://api.themoviedb.org/3/person/', list(df_fb['tmdb_id']), '?language=fr-FR', headers)
df_people_details = df_people_details[['id','biography', 'birthday', 'gender', 'name', 'place_of_birth', 'popularity', 'profile_path']]
df_people_details['profile_path'] = df_people_details['profile_path'].apply(lambda x : "https://image.tmdb.org/t/p/w500/" + x if x else None)
df_people_details['biography'] = df_people_details['biography'].apply(lambda x : x.replace('\n', ''))

df_people_details.fillna('unknow', inplace=True)

df_people_details.to_csv(path + "\\\\csv\\\\api_people_details.csv.zip", index=False, compression='zip')
del df_fb
del df_people_details
