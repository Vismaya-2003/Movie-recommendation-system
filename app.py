import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=371e9c4a79e7e7ff1ad07c1a7ef3ec11&language=en-US'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        poster_path = data.get('poster_path', '')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return ''  # Return an empty string if poster_path is not available
    except requests.RequestException as e:
        print(f"Error fetching poster: {e}")
        return ''  # Return an empty string in case of error

def recommend(movie):
    # Find the index of the movie in the DataFrame
    movie_index = movies[movies['title'] == movie].index[0]
    
    # Get the similarity scores for the movie at `movie_index`
    distances = similarity[movie_index]
    
    # Enumerate, sort, and get the top 5 most similar movies (excluding the movie itself)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movie_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Ensure `movie_id` is available in DataFrame
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        recommended_movie_posters.append(poster_url)
    
    return recommended_movies, recommended_movie_posters

st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .title {
        font-size: 2rem;
        font-weight: bold;
        margin-right: 1rem;
    }
    .description {
        font-size: 1.2rem;
        color: #555;
    }
    </style>
    <div class="title-container">
        <div class="title">Movie Recommendation System</div>
        <div class="description">Get movie suggestions based on your choice!</div>
    </div>
""", unsafe_allow_html=True)

# Load movie data and similarity matrix
movies_list = pickle.load(open(r'C:\Users\visma\OneDrive\Desktop\recommendation-system\recommend\movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open(r'C:\Users\visma\OneDrive\Desktop\recommendation-system\recommend\similarity.pkl', 'rb'))

selected_movie_name = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    
    # Create columns to display the recommended movies and posters
    cols = st.columns(min(5, len(names)))  # Ensure columns do not exceed the number of recommendations
    
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, use_column_width=True, caption=name)
