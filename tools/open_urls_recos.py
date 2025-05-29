import pandas as pd
from pathlib import Path
path = str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')
import webbrowser
import re
from sys import argv

#On charge le csv movies
df_movies = pd.read_csv(path + '\\\\final_csv\\\\movies.csv.zip')

def open_url_recos(movies):
    #On retrouvee la ligne du film
    temp = df_movies[df_movies['title'] == movies]
    print("Le Seigneur des anneaux : La Communauté de l'anneau")
    print(str(temp['title'].item()))
    #Si pas de d'occurence on quitte le programme
    if len(temp) == 0:
        return

    #On cast la series en string
    temp = str(temp['imdb_id_recos'].item())

    #On enleve les []', et on cast la strind en list
    temp = re.sub(r'[\[\]\',]', '', temp).split(sep=' ')

    #On boucle sur la liste pour ouvrir un lien imdb pour chaque id contenue dans la liste
    for v in temp:
        print(v)
        webbrowser.open(f'https://www.imdb.com/fr/title/{v}')


if __name__ == '__main__':
    if len(argv) > 1:
        open_url_recos(argv[1])