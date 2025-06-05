import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np
import re
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')) + '\\\\final_csv'

# Titre principal de l'application (affiché en haut de la page)
st.title("Recommandations!")

df_movies = pd.read_csv(path + '\\\\movies.csv.zip')

cols = list(df_movies.drop(columns=['title']).columns)
cols.insert(0, 'title')
df_movies = df_movies.reindex(columns=cols)

option = st.selectbox(
    "What do you want to watch?",
    df_movies,
    index=None,
    placeholder="Choisissez un film ici",
    label_visibility="visible",
)

if isinstance(option, type(None)) == False:
    current_movie = df_movies[df_movies['title'] == option]

    if isinstance(current_movie['poster_path'].values[0], type(np.nan)) == False:
        st.image(current_movie['poster_path'].values[0])

    if isinstance(current_movie['video_link'].values[0], type(np.nan)) == False:
        st.video(current_movie['video_link'].values[0])

    st.header(f"Nos recommandations pour {current_movie['title']}")

    for reco in re.sub('[\[\]\',]', '', current_movie['imdb_id_recos'].values[0]).split(' '):
        movie = df_movies[df_movies['imdb_id'] == reco]

        if isinstance(movie['poster_path'].values[0], type(np.nan)) == False:
            st.image(movie['poster_path'].values[0])

        st.write(movie)