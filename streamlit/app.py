import streamlit as st
import pandas as pd
from pathlib import Path
path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')) + '\\\\final_csv'

# Titre principal de l'application (affiché en haut de la page)
st.title("Recommandations!")

df_movies = pd.read_csv(path + '\\\\movies.csv.zip')

cols = list(df_movies.drop(columns=['title']).columns)
cols.insert(0, 'title')
df_movies = df_movies.reindex(columns=cols)

st.write(df_movies)

option = st.selectbox(
    "What do you want to watch?",
    df_movies,
    index=None,
    placeholder="Select a movies here",
    label_visibility="visible",
)
st.write(df_movies[df_movies['title'] == option])