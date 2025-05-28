from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import pandas as pd
from tqdm import tqdm


def get_data_from_url(url, headers,record_path=None, meta=None, meta_prefix=None):
    '''Return the data dict or None'''
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            df = pd.json_normalize(json_data, record_path=record_path, meta=meta, meta_prefix=meta_prefix)
            return df
        else:
            return None
    except Exception as e:
        print(f"Erreur pour {url}: {e}")
        return None

def url_to_dataframe(url_start, url_end_list, url_params, headers, record_path=None, meta=None, meta_prefix=None):

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(get_data_from_url, url_start + str(i) + url_params, headers, record_path, meta, meta_prefix)
                   for i in url_end_list]
        
        all_datas = None

        for future in tqdm(as_completed(futures), total=len(futures)):
            result = future.result()
            if isinstance(result, pd.DataFrame): 
                if isinstance(all_datas, pd.DataFrame):
                    all_datas = all_datas._append(result, ignore_index=True)
                else:
                    all_datas = result

    return pd.DataFrame(all_datas)