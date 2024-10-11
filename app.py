import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=29c72aaa827ce11824d4d5a7e2d4df54&language=en-US'.format(movie_id)
    response = requests.get(url)
    data = response.json()
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']

# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # Fetch movie ID
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Load the movies and similarity data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
Api_Key = '29c72aaa827ce11824d4d5a7e2d4df54'

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movies, recommended_movies_poster = recommend(selected_movie_name)
    
    st.write('Recommended Movies:')
    for i in range(len(recommended_movies)):
        st.write(recommended_movies[i])
        st.image(recommended_movies_poster[i])
