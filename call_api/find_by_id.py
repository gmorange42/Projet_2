import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from tqdm import tqdm
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))

def get_data_from_url(url, headers, id, record_path=None, meta=None, meta_prefix=None):
    '''Return the data dict or None'''
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            df = pd.json_normalize(json_data, record_path=record_path, meta=meta, meta_prefix=meta_prefix)
            return pd.concat([df, pd.DataFrame({'nconst': [id]})], axis=1)
        else:
            return None
    except Exception as e:
        pass
        print(f"Erreur pour {url}: {e}")
        return None

def url_to_dataframe(url_start, url_end_list, url_params, headers, record_path=None, meta=None, meta_prefix=None):
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(get_data_from_url, url_start + i + url_params, headers, i, record_path, meta, meta_prefix)
                   for i in url_end_list]
        
        if len(futures) > 0:
            all_datas = futures[0].result()
            futures.pop(0)
        else:
            return None

        for future in tqdm(as_completed(futures), total=len(futures)):
            result = future.result()
            all_datas = all_datas._append(result, ignore_index=True)

    return pd.DataFrame(all_datas)


with open(path + '\\\\tmdb_api_key', 'r') as file:
    key = file.read()

headers = {
    "accept": "application/json",
    "Authorization": key
}


#https://api.themoviedb.org/3/find/nm1109153?external_source=imdb_id&language=fr-FR
df_names= pd.read_csv(path + "\\\\csv\\\\name_basics.csv.zip")

df_find_by_id = url_to_dataframe('https://api.themoviedb.org/3/find/', list(df_names['nconst']), '?external_source=imdb_id&language=fr-FR', headers, record_path='person_results')

df_find_by_id = df_find_by_id[['id', 'nconst']]

df_find_by_id.dropna(inplace=True)
df_find_by_id.drop_duplicates(inplace=True)
df_find_by_id.rename(columns={'id': 'tmdb_id', 'nconst': 'imdb_id'}, inplace=True)
df_find_by_id['tmdb_id'] = df_find_by_id['tmdb_id'].astype('int32')

df_find_by_id.to_csv(path + "\\\\csv\\\\api_find_by_id.csv.zip", index=False, compression='zip')
del df_find_by_id
del df_names

