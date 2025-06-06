import streamlit as st
import pandas as pd
import numpy as np
import re
from pathlib import Path
from streamlit_card import card
from st_clickable_images import clickable_images

path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\')) + '\\\\final_csv'


st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)



#Importe le csv des movies
df_movies = pd.read_csv(path + '\\\\movies.csv.zip')
df_people= pd.read_csv(path + '\\\\people.csv.zip')
df_inter= pd.read_csv(path + '\\\\inter.csv.zip')

query_params = st.query_params
selected_movie_id = query_params.get("movie_id", [None])[0]

if selected_movie_id:
    st.write(selected_movie_id)
    #current_movie = df_movies[df_movies['imdb_id'] == selected_movie_id]



# Titre principal de l'application (affiché en haut de la page)
st.title("Recommandations!")

#On met la colonne title en premier dans le DataFrame
cols = list(df_movies.drop(columns=['title']).columns)
cols.insert(0, 'title')
df_movies = df_movies.reindex(columns=cols)


cols_search_title = st.columns([10,1,10])

with cols_search_title[0]:
    #Affiche une boite de selection pour choisir le film
    option = st.selectbox(
        "What do you want to watch?",
        df_movies,
        index=None,
        placeholder="Choisissez un film ici",
        label_visibility="visible",
    )

cols_poster_description = st.columns([10,1,10])

#Si option n'est pas null (donc un film est selectionne) on stock pd.Series du film
if isinstance(option, type(None)) == False:
    current_movie = df_movies[df_movies['title'] == option]

    with cols_search_title[2]:
        st.header(current_movie['title'].values[0])

    with cols_poster_description[0]:
        #Si le poster_path existe, on affiche le poster du film
        if isinstance(current_movie['poster_path'].values[0], type(np.nan)) == False:
            st.image(current_movie['poster_path'].values[0])

    with cols_poster_description[2]:
        if isinstance(current_movie['overview'].values[0], type(np.nan)) == False:
            st.write(f"{current_movie['overview'].values[0]}")
        if isinstance(current_movie['startYear'].values[0], type(np.nan)) == False:
            st.write(f"Date de sortie: {current_movie['startYear'].values[0]}")
        if isinstance(current_movie['runtimeMinutes'].values[0], type(np.nan)) == False:
            st.write(f"Durée: {current_movie['runtimeMinutes'].values[0]} minutes")
        if isinstance(current_movie['genres'].values[0], type(np.nan)) == False:
            st.write(f"Genres: {re.sub(',', ', ',current_movie['genres'].values[0])}")
        st.write(f"Note moyenne: {current_movie['averageRating'].values[0]}")
        st.write("Pays d'origine: {}".format(re.sub('[\'\[\]]', '', current_movie['origin_country'].values[0])))

        df_people_for_current_movie = df_inter[df_inter['imdb_movie_id'] == current_movie['imdb_id'].values[0]]
        df_people_for_current_movie = pd.merge(left=df_people_for_current_movie, right=df_people, how='left', left_on='imdb_people_id', right_on='imdb_id')
        df_people_for_current_movie = df_people_for_current_movie.drop_duplicates()

        cols_DW = st.columns(4)
        list_DW = df_people_for_current_movie[(df_people_for_current_movie['category'] == 'director')|
                                                                   (df_people_for_current_movie['category'] == 'writer')]['imdb_id'].to_list()
        if len(list_DW) > 1:
            for i,director_id in enumerate(list_DW):
                with cols_DW[i % 4]:
                    if df_people[df_people['imdb_id'] == director_id]['profile_path'].values[0] != 'unknow':
                        st.image(df_people[df_people['imdb_id'] == director_id]['profile_path'].values[0])
                    if df_people[df_people['imdb_id'] == director_id]['primaryName'].values[0] != 'unknow':
                        st.write(df_people[df_people['imdb_id'] == director_id]['primaryName'].values[0])
                    st.write(df_people[df_people['imdb_id'] == director_id]['category'].values[0])


    
    
    cols_videos_people = st.columns([10,1,10])

    with cols_videos_people[0]:
        st.header("Trailer")
        #Si le video_link existe, on affiche la video (teaser) du film
        if isinstance(current_movie['video_link'].values[0], type(np.nan)) == False:
            st.video(current_movie['video_link'].values[0])
        
    with cols_videos_people[2]:
        st.header("Actrices et acteurs")
        cols_actors= st.columns(4)
        list_actors = df_people_for_current_movie[(df_people_for_current_movie['category'] == 'actor')|
                                                                   (df_people_for_current_movie['category'] == 'actress')]['imdb_id'].to_list()
        if len(list_actors) > 0:
            for i,actor_id in enumerate(list_actors):
                with cols_actors[i % 4]:
                    if df_people[df_people['imdb_id'] == actor_id]['profile_path'].values[0] != 'unknow':
                        st.image(df_people[df_people['imdb_id'] == actor_id]['profile_path'].values[0])
                    if df_people[df_people['imdb_id'] == actor_id]['primaryName'].values[0] != 'unknow':
                        st.write(df_people[df_people['imdb_id'] == actor_id]['primaryName'].values[0])

    #Sous titre des recommandations
    st.header(f"Nos recommandations pour {current_movie['title'].values[0]}")

    cols_recos = st.columns(4)
    #On boucle sur la liste des recommandations du current_movie
    for i, reco in enumerate(re.sub('[\[\]\',]', '', current_movie['imdb_id_recos'].values[0]).split(' ')):
        movie = df_movies[df_movies['imdb_id'] == reco]

        #Si le poster_path de la recommandation existe, on l'affiche
        if isinstance(movie['poster_path'].values[0], type(np.nan)) == False:
            with cols_recos[i % 4]:
                card(
                title=movie['title'].values[0],
                text='',
                image=movie['poster_path'].values[0],
                url=f"?movie_id={reco}"
                )