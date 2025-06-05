import streamlit as st
import pandas as pd
import numpy as np
import re
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')) + '\\\\final_csv'

#Importe le csv des movies
df_movies = pd.read_csv(path + '\\\\movies.csv.zip')

# Titre principal de l'application (affiché en haut de la page)
st.title("Recommandations!")

#On met la colonne title en premier dans le DataFrame
cols = list(df_movies.drop(columns=['title']).columns)
cols.insert(0, 'title')
df_movies = df_movies.reindex(columns=cols)

#Affiche une boite de selection pour choisir le film
option = st.selectbox(
    "What do you want to watch?",
    df_movies,
    index=None,
    placeholder="Choisissez un film ici",
    label_visibility="visible",
)

#Si option n'est pas null (donc un film est selectionne) on stock pd.Series du film
if isinstance(option, type(None)) == False:
    current_movie = df_movies[df_movies['title'] == option]

    #Si le poster_path existe, on affiche le poster du film
    if isinstance(current_movie['poster_path'].values[0], type(np.nan)) == False:
        st.image(current_movie['poster_path'].values[0])

    #Si le video_link existe, on affiche la video (teaser) du film
    if isinstance(current_movie['video_link'].values[0], type(np.nan)) == False:
        st.video(current_movie['video_link'].values[0])
    
    #Sous titre des recommandations
    st.header(f"Nos recommandations pour {current_movie['title'].values[0]}")

    #On boucle sur la liste des recommandations du current_movie
    for reco in re.sub('[\[\]\',]', '', current_movie['imdb_id_recos'].values[0]).split(' '):
        movie = df_movies[df_movies['imdb_id'] == reco]

        #Si le poster_path de la recommandation existe, on l'affiche
        if isinstance(movie['poster_path'].values[0], type(np.nan)) == False:
            st.image(movie['poster_path'].values[0])