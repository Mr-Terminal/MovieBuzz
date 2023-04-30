import streamlit as st
import numpy as np
import pandas as pd
import requests
from streamlit_option_menu import option_menu
import pickle

st.set_page_config(
    page_title="MovieBuzz",
    page_icon="logo.png",
    layout="wide",
)

with open("style.css") as source:
    st.markdown(f"<style>{source.read()}</style>", unsafe_allow_html=True)


with st.sidebar:
    choose = option_menu("", options=["Home", "Genre", "Top Rated"],
                         icons=['house', 'grid-3x3-gap', 'star'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "--hover-color": "#696a69ae"},
        "nav-link-selected": {"background-color": "#0ce956ae"},
    }
    )

movies = pd.read_csv("./dataframes/tmdb_5000_movies.csv")
credits = pd.read_csv("./dataframes/tmdb_5000_credits.csv")

# merge the two dataframes
movies = movies.merge(credits, on='title')


if choose == "Home":
    st.markdown("""
            <div class="topnav">
                <h3 class="heading">
                   Movie Recommender
                </h3>
            </div>
        """, unsafe_allow_html=True)

    # read the data through pickle, here movies_list is a dictionary.
    movies_list = pickle.load(open('movies.pkl', 'rb'))
    # read the similarity matrix also
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    # movies_set is the required dataframe  (movies_set == new_df)
    movies_set = pd.DataFrame(movies_list)

    
    selected_movie = st.selectbox(
        'Search for a movie', movies_set['title'].values)
    
    @st.experimental_memo
    def fetch_poster(movie_id):
        result = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US')
        data = result.json()
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

    
    def recommend(movie):

        movie_index = movies_set[movies_set['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x: x[1])[0:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            movie_id = movies_set.iloc[i[0]].movie_id
            recommended_movies.append(movies_set.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters

    if st.button('Search'):
        names, posters = recommend(selected_movie)
        st.subheader("Recommended for you")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.image(posters[0], caption=names[0], width=150)
        with col2:
            st.image(posters[1], caption=names[1], width=150)
        with col3:
            st.image(posters[2], caption=names[2], width=150)
        with col4:
            st.image(posters[3], caption=names[3], width=150)
        with col5:
            st.image(posters[4], caption=names[4], width=150)
        with col6:
            st.image(posters[5], caption=names[5], width=150)
   
    else:

        id = movies['id'].values  # here id is an array
        
        @st.experimental_memo
        def fetch_data(movie_id):
            result = requests.get(
                f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US')
            data = result.json()

            if (data['poster_path'] == None):
                return fetch_data(np.random.choice(id, replace=False))

            string = "https://image.tmdb.org/t/p/w500" + data["poster_path"]

            a = [string, data['title']]
            return a

        # def fetch_trending_data():
        Result = requests.get(
            f'https://api.themoviedb.org/3/trending/movie/week?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US')
        data_trending = Result.json()
        x = np.random.choice(data_trending['results'], size=6, replace=False)

        st.subheader("Trending Now")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:

            str = "https://image.tmdb.org/t/p/w500/" + x[0]['poster_path']
            b = [str, x[0]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + x[1]['poster_path']
            b = [str, x[1]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + x[2]['poster_path']
            b = [str, x[2]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + x[3]['poster_path']
            b = [str, x[3]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + x[4]['poster_path']
            b = [str, x[4]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + x[5]['poster_path']
            b = [str, x[5]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        st.markdown('''
                <hr width="95%" style="margin: 0 auto">
            ''', unsafe_allow_html=True)

        st.subheader("All Time Hit")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            b = fetch_data(np.random.choice(id, replace=False))

            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)
        with col2:
            b = fetch_data(np.random.choice(id, replace=False))

            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)
        with col3:
            b = fetch_data(np.random.choice(id, replace=False))

            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)
        with col4:
            b = fetch_data(np.random.choice(id, replace=False))

            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)
        with col5:
            b = fetch_data(np.random.choice(id, replace=False))

            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)
        with col6:
            b = fetch_data(np.random.choice(id, replace=False))

            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

elif choose == "Genre":

    st.markdown("""
        <div class="topnav">
        <h3 class="heading">
            Movie Recommender
        </h3>
        </div>
    """, unsafe_allow_html=True)

    # read the data through pickle, here movies_list is a dictionary.
    movies_list = pickle.load(open('movies.pkl', 'rb'))
    # read the similarity matrix also
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    # movies_set is the required dataframe  (movies_set == new_df)
    movies_set = pd.DataFrame(movies_list)
    selected_movie = st.selectbox(
        'Search for a movie', movies_set['title'].values)
    
    @st.experimental_memo
    def fetch_poster(movie_id):
        result = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US')
        data = result.json()
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    
    
    def recommend(movie):

        movie_index = movies_set[movies_set['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x: x[1])[0:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            movie_id = movies_set.iloc[i[0]].movie_id
            recommended_movies.append(movies_set.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters

    if st.button('Search'):
        names, posters = recommend(selected_movie)
        st.subheader("Recommended for you")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.image(posters[0], caption=names[0], width=150)
        with col2:
            st.image(posters[1], caption=names[1], width=150)
        with col3:
            st.image(posters[2], caption=names[2], width=150)
        with col4:
            st.image(posters[3], caption=names[3], width=150)
        with col5:
            st.image(posters[4], caption=names[4], width=150)
        with col6:
            st.image(posters[5], caption=names[5], width=150)

    else:

        # action_adventure(28,12):
        Result_action = requests.get(
            f'https://api.themoviedb.org/3/discover/movie?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US&with_genres=28%212C12')
        data_action = Result_action.json()
        x = np.random.choice(data_action['results'], size=6, replace=False)

        # family and drama
        Result_drama = requests.get(
            f'https://api.themoviedb.org/3/discover/movie?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US&with_genres=18%210751C12')
        data_drama = Result_drama.json()
        y = np.random.choice(data_drama['results'], size=6, replace=False)

        # horror
        Result_horror = requests.get(
            f'https://api.themoviedb.org/3/discover/movie?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US&with_genres=27')
        data_horror = Result_horror.json()
        z = np.random.choice(data_horror['results'], size=6, replace=False)

        # comedy
        Result_comedy = requests.get(
            f'https://api.themoviedb.org/3/discover/movie?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US&with_genres=35')
        data_comedy = Result_comedy.json()
        w = np.random.choice(data_comedy['results'], size=6, replace=False)

        # romance
        Result_romance = requests.get(
            f'https://api.themoviedb.org/3/discover/movie?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US&with_genres=10749s')
        data_romance = Result_romance.json()
        v = np.random.choice(data_romance['results'], size=6, replace=False)

        st.subheader("Action and Adventure")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            str = "https://image.tmdb.org/t/p/w500/" + x[0]['poster_path']
            b = [str, x[0]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + x[1]['poster_path']
            b = [str, x[1]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + x[2]['poster_path']
            b = [str, x[2]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + x[3]['poster_path']
            b = [str, x[3]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + x[4]['poster_path']
            b = [str, x[4]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + x[5]['poster_path']
            b = [str, x[5]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        st.markdown('''
                    <hr width="95%" style="margin: 0 auto">
                ''', unsafe_allow_html=True)

        st.subheader("Family and Drama")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            str = "https://image.tmdb.org/t/p/w500/" + y[0]['poster_path']
            b = [str, y[0]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + y[1]['poster_path']
            b = [str, y[1]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + y[2]['poster_path']
            b = [str, y[2]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + y[3]['poster_path']
            b = [str, y[3]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + y[4]['poster_path']
            b = [str, y[4]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + y[5]['poster_path']
            b = [str, y[5]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        st.markdown('''
                    <hr width="95%" style="margin: 0 auto">
                ''', unsafe_allow_html=True)

        st.subheader("Horror")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            str = "https://image.tmdb.org/t/p/w500/" + z[0]['poster_path']
            b = [str, z[0]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + z[1]['poster_path']
            b = [str, z[1]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + z[2]['poster_path']
            b = [str, z[2]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + z[3]['poster_path']
            b = [str, z[3]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + z[4]['poster_path']
            b = [str, z[4]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + z[5]['poster_path']
            b = [str, z[5]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        st.markdown('''
                    <hr width="95%" style="margin: 0 auto">
                ''', unsafe_allow_html=True)

        st.subheader("Comedy")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            str = "https://image.tmdb.org/t/p/w500/" + w[0]['poster_path']
            b = [str, w[0]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + w[1]['poster_path']
            b = [str, w[1]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + w[2]['poster_path']
            b = [str, w[2]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + w[3]['poster_path']
            b = [str, w[3]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + w[4]['poster_path']
            b = [str, w[4]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + w[5]['poster_path']
            b = [str, w[5]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        st.markdown('''
                    <hr width="95%" style="margin: 0 auto">
                ''', unsafe_allow_html=True)

        st.subheader("Romance")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            str = "https://image.tmdb.org/t/p/w500/" + v[0]['poster_path']
            b = [str, v[0]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + v[1]['poster_path']
            b = [str, v[1]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + v[2]['poster_path']
            b = [str, v[2]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + v[3]['poster_path']
            b = [str, v[3]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + v[4]['poster_path']
            b = [str, v[4]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + v[5]['poster_path']
            b = [str, v[5]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

elif choose == "Top Rated":

    st.markdown("""
        <div class="topnav">
        <h3 class="heading">
            Movie Recommender
        </h3>
        </div>
    """, unsafe_allow_html=True)

    # read the data through pickle, here movies_list is a dictionary.
    movies_list = pickle.load(open('movies.pkl', 'rb'))
    # read the similarity matrix also
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    # movies_set is the required dataframe  (movies_set == new_df)
    movies_set = pd.DataFrame(movies_list)
    selected_movie = st.selectbox(
        'Search for a movie', movies_set['title'].values)
    
    @st.experimental_memo
    def fetch_poster(movie_id):
        result = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US')
        data = result.json()
        return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    
    
    def recommend(movie):

        movie_index = movies_set[movies_set['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x: x[1])[0:6]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            movie_id = movies_set.iloc[i[0]].movie_id
            recommended_movies.append(movies_set.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters

    if st.button('Search'):
        names, posters = recommend(selected_movie)
        st.subheader("Recommended for you")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.image(posters[0], caption=names[0], width=150)
        with col2:
            st.image(posters[1], caption=names[1], width=150)
        with col3:
            st.image(posters[2], caption=names[2], width=150)
        with col4:
            st.image(posters[3], caption=names[3], width=150)
        with col5:
            st.image(posters[4], caption=names[4], width=150)
        with col6:
            st.image(posters[5], caption=names[5], width=150)

    else:

        Result_rated = requests.get(
            f'https://api.themoviedb.org/3/movie/top_rated?api_key=0e598e9ce44fd2e9a98ef9517e95fafb&language=en-US&page=1')
        data_rated = Result_rated.json()
        u = np.random.choice(data_rated['results'], size=18, replace=False)

        st.subheader("Top Rated")
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            str = "https://image.tmdb.org/t/p/w500/" + u[0]['poster_path']
            b = [str, u[0]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + u[1]['poster_path']
            b = [str, u[1]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + u[2]['poster_path']
            b = [str, u[2]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + u[3]['poster_path']
            b = [str, u[3]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + u[4]['poster_path']
            b = [str, u[4]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + u[5]['poster_path']
            b = [str, u[5]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            str = "https://image.tmdb.org/t/p/w500/" + u[6]['poster_path']
            b = [str, u[6]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + u[7]['poster_path']
            b = [str, u[7]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + u[8]['poster_path']
            b = [str, u[8]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + u[9]['poster_path']
            b = [str, u[9]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + u[10]['poster_path']
            b = [str, u[10]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + u[11]['poster_path']
            b = [str, u[11]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            str = "https://image.tmdb.org/t/p/w500/" + u[12]['poster_path']
            b = [str, u[12]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col2:
            str = "https://image.tmdb.org/t/p/w500/" + u[13]['poster_path']
            b = [str, u[13]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col3:
            str = "https://image.tmdb.org/t/p/w500/" + u[14]['poster_path']
            b = [str, u[14]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col4:
            str = "https://image.tmdb.org/t/p/w500/" + u[15]['poster_path']
            b = [str, u[15]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col5:
            str = "https://image.tmdb.org/t/p/w500/" + u[16]['poster_path']
            b = [str, u[16]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)

        with col6:
            str = "https://image.tmdb.org/t/p/w500/" + u[17]['poster_path']
            b = [str, u[17]['title']]
            if (len(b[1]) > 25):
                b[1] = b[1][:20] + '..'
            st.image(b[0], caption=b[1], width=150)
