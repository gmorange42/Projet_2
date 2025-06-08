import streamlit as st
from st_clickable_images import clickable_images
import pandas as pd
import numpy as np
import re
from pathlib import Path
import streamlit.components.v1 as components

#etoiles pour ratings
#images people manquante

path = (str(Path(__file__).resolve().parent.parent).replace('\\', '\\\\'))

#Scroll jusqu'a l'anchor choisi
def scroll_to_anchor(anchor_id):
    components.html(
        f"""
        <script>
        const element = window.parent.document.getElementById('{anchor_id}');
        if (element) {{
            element.scrollIntoView({{behavior: 'smooth'}});
        }}
        </script>
        """,
        height=0,
    )

#Change le film selectionner et appelle scroll_to_anchor() pour retourner en haut de page, puis rerun la page
def update_option(title):
    if 'select_box' in st.session_state:
        del st.session_state['select_box']
    st.session_state.select_box = title
    st.session_state.option = title
    scroll_to_anchor('top')
    st.rerun()

def display_people_image(df, nb_cols, key, WD=False):
    click_list = []
    cols = st.columns(nb_cols)
    for i, people in enumerate(df.iterrows()):
        if i % nb_cols == 0:
            cols = st.columns(nb_cols)
        with cols[i % nb_cols]:
            click_list.append(clickable_images(
                [people[1]['profile_path'] if people[1]['profile_path'] != 'unknow' else ('https://as1.ftcdn.net/v2/jpg/00/95/81/38/1000_F_95813826_gWhsBf6OUOG7T0duUMn9FIfXycDXiV7F.jpg' if people[1]['gender'] == 'Femme' or people[1]['category'] == 'actress' else 'https://content.api.news/v3/images/bin/4ac3dad0dca77271cea3e59e2af3642a')],
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "10px", "width": "100%"},
                key = key + str(i)))
            st.write(people[1]['primaryName'])
            if WD:
                st.write(('(Producteur)' if people[1]['gender'] == 'Homme' else '(Productrice)')if people[1]['category'] == 'director' else '(Scénariste)')
            st.write('')
    if 0 in click_list:
        update_option(df.iloc[click_list.index(0)]['primaryName'])

def display_actors(df):
    peoples_clicked = []
    st.header("Actrices et acteurs")
    df_actors= df[(df['category'] == 'actor')| (df['category'] == 'actress')]
    display_people_image(df_actors, 4, 'actors_click')

def display_DW(df):
    peoples_clicked = []
    df_DW = df[(df['category'] == 'writer') | (df['category'] == 'director')]
    display_people_image(df_DW, 4, 'DW_list', True)

def display_movie_details(current_movie):
        st.write(f"{current_movie['overview'].values[0]}")
        if isinstance(current_movie['startYear'].values[0], type(np.nan)) == False:
            st.write(f"Date de sortie: {current_movie['startYear'].values[0]}")
        if isinstance(current_movie['runtimeMinutes'].values[0], type(np.nan)) == False:
            st.write(f"Durée: {current_movie['runtimeMinutes'].values[0]} minutes")
        st.write(f"Genres: {re.sub(',', ', ',current_movie['genres'].values[0])}")
        st.write(f"Note moyenne: {current_movie['averageRating'].values[0]}")
        st.write("Pays d'origine: {}".format(re.sub('[\'\[\]]', '', current_movie['origin_country'].values[0])))

def display_people_details(current_people):
    category = current_people.category.values[0]
    if category == 'Writer':
        category == 'Scénariste'
    elif category == 'actress':
        category = 'Actrice'
    elif category == 'actor':
        category = 'Acteur'
    elif category == 'director' and current_people.gender.values[0] == 'Homme':
        category = 'Producteur'
    else:
        category = 'Productrice'

    st.subheader(category)
    if isinstance(current_people['biography'].values[0], type(np.nan)) == False:
        st.write(current_people['biography'].values[0])
    if current_people['birthday'].values[0] != 'unknow':
        st.write(f"Date de naissance: {current_people['birthday'].values[0]}")
    if current_people['place_of_birth'].values[0] != 'unknow':
        st.write(f"Lieu de naissance: {current_people['place_of_birth'].values[0]}")


def display_recos(current_movie, nb_cols):
    #Sous titre des recommandations
    st.header(f"Nos recommandations pour {current_movie['title'].values[0]}")

    #On boucle sur la liste des recommandations du current_movie
    movies_clicked = []
    for i, reco in enumerate(re.sub('[\[\]\',]', '', current_movie['imdb_id_recos'].values[0]).split(' ')):
        if i % nb_cols == 0:
            cols = st.columns(nb_cols)
        movie = df_movies[df_movies['imdb_id'] == reco]

        #Si le poster_path de la recommandation existe, on l'affiche
        if isinstance(movie['poster_path'].values[0], type(np.nan)) == False:
            with cols[i % nb_cols]:
                movies_clicked.append(clickable_images(
                    [movie['poster_path'].values[0]],
                    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                    img_style={"margin": "10px", "width": "100%"},))
                
    if 0 in movies_clicked:
        list_series_recos = [df_movies[df_movies['imdb_id'] == x ] for x in re.sub('[\[\]\',]', '', current_movie['imdb_id_recos'].values[0]).split(' ')]
        update_option(list_series_recos[movies_clicked.index(0)]['title'].values[0])


def page_movie():
    current_movie = df_movies[df_movies['title'] == st.session_state.option]

    with cols_search_title[2]:
        st.header(current_movie['title'].values[0])

    with cols_poster_description[0]:
        #Si le poster_path existe, on affiche le poster du film
        if isinstance(current_movie['poster_path'].values[0], type(np.nan)) == False:
            st.image(current_movie['poster_path'].values[0], use_container_width=True)

    with cols_poster_description[2]:
        display_movie_details(current_movie)

        #On cree une table contenant tout les intervenants du current_movie
        df_people_for_current_movie = df_inter[df_inter['imdb_movie_id'] == current_movie['imdb_id'].values[0]]
        df_people_for_current_movie = pd.merge(left=df_people_for_current_movie, right=df_people, how='left', left_on='imdb_people_id', right_on='imdb_id')
        df_people_for_current_movie = df_people_for_current_movie.drop_duplicates()

        cols_D = st.columns(4)
        
        display_DW(df_people_for_current_movie)

    cols_videos_people = st.columns([10,1,10])

    with cols_videos_people[0]:
        st.header("Trailer")
        #Si le video_link existe, on affiche la video (teaser) du film
        if isinstance(current_movie['video_link'].values[0], type(np.nan)) == False:
            st.video(current_movie['video_link'].values[0])
        
    with cols_videos_people[2]:
        display_actors(df_people_for_current_movie)

    display_recos(current_movie, 4)

def page_people():
    current_people = df_people[df_people['primaryName'] == st.session_state.option]

    with cols_search_title[2]:
        st.header(current_people['primaryName'].values[0])

    with cols_poster_description[0]:
        #Si le poster_path existe, on affiche le poster du film
        st.image(current_people['profile_path'].values[0] if current_people['profile_path'].values[0] != 'unknow' else \
            ('https://as1.ftcdn.net/v2/jpg/00/95/81/38/1000_F_95813826_gWhsBf6OUOG7T0duUMn9FIfXycDXiV7F.jpg' if current_people['gender'].values[0] == 'Femme' or current_people['category'].values[0] == 'actress' \
             else 'https://content.api.news/v3/images/bin/4ac3dad0dca77271cea3e59e2af3642a'), use_container_width=True)

    with cols_poster_description[2]:
        display_people_details(current_people)

        st.subheader(f"{'Connu' if current_people.gender.values[0] == 'Homme' else 'Connue'} pour:")

        cols_known_for= st.columns(4)
        #On boucle sur la liste des recommandations du current_movie
        movies_clicked = []
        list_series_recos = []
        for series in [df_movies[df_movies['imdb_id'] == x ] for x in re.sub(',', ' ', current_people['knownForTitles'].values[0]).split(' ')]:
            if len(series) > 0:
                list_series_recos.append(series)
        for i, reco in enumerate(list_series_recos):

            #Si le poster_path de la recommandation existe, on l'affiche
            with cols_known_for[i % 4]:
                movies_clicked.append(clickable_images(
                    [reco['poster_path'].values[0]],
                    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                    img_style={"margin": "10px", "width": "100%"},))

                    
        if 0 in movies_clicked:
            update_option(list_series_recos[movies_clicked.index(0)]['title'].values[0])


def display_random_movies(df, nb_cols):

    movies_clicked = []
    for i, movie in enumerate(st.session_state.random_movies):
        if i % nb_cols == 0:
            cols = st.columns(nb_cols)

        with cols[i % nb_cols]:
            movies_clicked.append(clickable_images(
                [movie['poster_path']],
                div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                img_style={"margin": "10px", "width": "100%"},))
                
    if 0 in movies_clicked:
        update_option(st.session_state.random_movies[movies_clicked.index(0)]['title'])


#Configuration de la page
st.set_page_config(page_title='Recos', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

#Ajouter option a session_state et le set a None
if "option" not in st.session_state:
    st.session_state.option = None

#Cree une anchor 'top'
st.markdown('<div id="top"></div>', unsafe_allow_html=True)


#Importe le csv des movies
df_movies = pd.read_csv(path + '\\\\final_csv\\\\movies.csv.zip')
df_people= pd.read_csv(path + '\\\\final_csv\\\\people.csv.zip')
df_inter= pd.read_csv(path + '\\\\final_csv\\\\inter.csv.zip')

if "random_movies" not in st.session_state:
    st.session_state.random_movies = [x[1] for x in df_movies.sample(8).iterrows()]

#Cree 3 colonnes 
cols_search_title = st.columns([10,1,10])

with cols_search_title[0]:

    cols_search_and_random = st.columns([8,1])
    #Affiche une boite de selection pour choisir le film
    st.session_state.option = st.selectbox(
        "Que cherchez vous ?",
        pd.concat([df_movies.title, df_people.primaryName]),
        index=None,
        placeholder="Choisissez un film ou un intervenant ici",
        label_visibility="visible",
        key='select_box'
    )

if st.button('Films aléatoires'):
    st.session_state.random_movies = [x[1] for x in df_movies.sample(8).iterrows()]
    update_option(None)

#Cree encore 3 colonnes 

cols_poster_description = st.columns([10,1,10])

#Si option n'est pas null (donc un film est selectionne) on stock pd.Series du film
if isinstance(st.session_state.option, type(None)) == False:
    if len(df_movies[df_movies['title'] == st.session_state.option]) == 1:
        page_movie()
    else:
        page_people()
else:
    display_random_movies(df_movies, 8)