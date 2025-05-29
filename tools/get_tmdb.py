import sys
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))
sys.path.append(path + '\\\\tools')
import call_api_thread as cath

def create_tmdb(df_movies):
    #config headers
    with open(path + '\\\\tmdb_api_key', 'r') as file:
        key = file.read()

    headers = {
        "accept": "application/json",
        "Authorization": key
    }

    df_tmdb = cath.url_to_dataframe("https://api.themoviedb.org/3/movie/", list(df_movies['tconst']), '?language=fr-FR', headers)

    df_tmdb.drop(columns=['adult', 'genres','homepage', 'original_language', 'original_title', 'backdrop_path',
                          'production_companies', 'production_countries', 'release_date', 'runtime',
                          'spoken_languages', 'status', 'tagline', 'video', 'vote_average',
                          'vote_count', 'belongs_to_collection', 'belongs_to_collection.name',
                          'belongs_to_collection.poster_path', 'belongs_to_collection.backdrop_path'], inplace=True)
    #remplacement des valeur \N et None par No_collection dans la colonne belongs_to_collection 
    df_tmdb['belongs_to_collection.id'] = df_tmdb['belongs_to_collection.id'].replace(['\\N', None], 'No_collection')
    
    #On filtre les lignes contenant les pays US et FR
    df_tmdb = df_tmdb[df_tmdb['origin_country'].astype(str).str.contains('US|FR', regex=True)]

    #remplacement des valeurs nulles dans backdrop_path par 'unknow'
    df_tmdb['poster_path'] = df_tmdb['poster_path'].fillna('unknow')

    #remplacement des valeurs nulles dans overview par 'unknow'
    df_tmdb['overview'] = df_tmdb['overview'].fillna('unknow')

    df_tmdb.drop_duplicates(subset=['id'], inplace=True)

    df_tmdb.to_csv(path + '\\\\csv\\\\generate_tmdb.csv.zip', index=False, compression='zip')

    return df_tmdb