import pandas as pd
from pathlib import Path
#from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
path = str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')
import re

def set_df_movies_to_KNN(df):
    '''Les valeurs numeriques sont scale, sinon chaques elements de la colonnes sont tranformes en colonnes rempli de 1 et 0 suivant si
    la ligne contenait ou pas cet element dans cette colonne.'''


    #On ne garde que les colonnes pertinentes
    df = df[['startYear', 'runtimeMinutes', 'genres', 'averageRating', 'popularity', 'origin_country']]
    #df = df[['startYear', 'genres', 'averageRating', 'origin_country']]
    
    #On transform les colonnes numeriques pour qu'elles aient toutes une valeur comprise entre 0 et 1
    #model = MinMaxScaler()
    model = StandardScaler()
    df[df.select_dtypes(include='number').columns] = model.fit_transform(df.select_dtypes(include='number'))

    #On cree de nouvelles colonnes en fonction des genres, avec 1 dans la colonne du genre si la ligne contient ce genre, sinon 0
    df = pd.concat([df, df['genres'].str.get_dummies(sep=',')], axis=1)

    #on supprime la colonne genres qui ne sert plus a rien
    df.drop(columns=['genres'], inplace=True)

    #On stock dans une nouvelle colonne uniquement les countries FR et US
    df['origin_country_FR_US'] = df['origin_country'].apply(lambda x : re.findall(r'FR|US', x))
    
    #on supprime la colonne origin_country qui ne sert plus a rien
    df.drop(columns=['origin_country'], inplace=True)

    #enleve les [] ' dand la colonne origin_country_FR_US (regex) apres avoir trie les FR/US et join dans une string
    df['origin_country_FR_US'] = df['origin_country_FR_US'].apply(lambda x : re.sub(r'[\[\]\']', '', ''.join(sorted(x))))

    #On cree de nouvelles colonnes en fonction de FR, US ou FRUS, avec 1 dans la colonne si la ligne contient ce genre, sinon 0
    df = pd.concat([df, df['origin_country_FR_US'].str.get_dummies(sep=',')], axis=1)
    
    #on supprime la colonne origin_country_FR_US qui ne sert plus a rien
    df.drop(columns=['origin_country_FR_US'], inplace=True)

    
    return df


def add_reco(df:pd.DataFrame, value_to_take_col:str, n_neighbors:int=5, new_col:str='new_col'):
    '''ajoute a df une liste des n_neighbors voisins les plus proches a chaque ligne.
        Les listes seront stockees dans la colonne new_col.
        Les indices contenues dans les listes prendront les valeurs contenues dans la colonne value_to_take_cal de df'''

    #supprime la colonne qu'on qui porte le nom contenu dans new_col
    if new_col in df.columns:
        df.drop(columns=[new_col], inplace=True)

    #Mise a l'echelle des valeurs
    df_set = set_df_movies_to_KNN(df)

    #entraienment du model
    nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(df_set)

    #retourne l'indice des  n_neighbors voisins les plus proches pour chaques film de df_set
    distance, indice= nbrs.kneighbors(df_set)

    #creation d'un DataFrame contenant tout les indices des voisins les plus proches pour chaques ligne,
    # sauf le premiers indices qui correspond a l'indice de la ligne
    df_neighbors= pd.DataFrame(indice[:,1:])

    #On regroupe les indices de voisins dans une seul colonne sous forme de liste
    df_neighbors = pd.DataFrame({new_col : df_neighbors.agg(list, axis='columns')})

    #on remplace les indices des voisins par l'imdb_id
    df_neighbors[new_col] = df_neighbors[new_col].apply(lambda x : [df.loc[v][value_to_take_col] for v in x])

    #On retourne le merge du DateFrame d'origine et de celui contenant les imdb_id recommandes
    return pd.merge(left=df_movies, right=df_neighbors, left_index=True, right_index=True)

#On charge le csv movies
df_movies = pd.read_csv(path + '\\\\final_csv\\\\movies.csv.zip')

#on y ajoute les recommandations
df_movies = add_reco(df_movies, 'imdb_id', 6, "imdb_id_recos")

#on remplace l'ancien csv movies par le nouveau contentant les recommandations
df_movies.to_csv(path + "\\\\final_csv\\\\movies.csv.zip", index=False, compression='zip')