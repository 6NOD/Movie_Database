import streamlit as st
import requests

st.set_page_config(layout="wide")

# Set title
st.title("🎬 Movie Dashboard")

# Fetch movie data from TMDB
api_key = st.secrets["tmdb_api"]
base_url = "https://api.themoviedb.org/3"
image_base_url = "https://image.tmdb.org/t/p/w500"


def get_movies(endpoint):
    url = f"{base_url}/{endpoint}?api_key={api_key}&language=en-US&page=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []


def display_movies(movie_list):
    cols = st.columns(5)
    for i, movie in enumerate(movie_list):
        with cols[i % 5]:
            poster_path = movie.get("poster_path")
            title = movie.get("title", "Unknown Title")
            rating = movie.get("vote_average", "N/A")
            release_date = movie.get("release_date", "")
            
            if poster_path:
                st.image(image_base_url + poster_path, use_column_width=True)
            st.markdown(f"**{title}**")
            st.caption(f"Rating: {rating} | Release: {release_date}")


# Genre and category filter (example demo, can be enhanced)
genres = ["All", "Action", "Comedy", "Drama", "Horror", "Romance"]
selected_genre = st.selectbox("Filter by Genre (for future enhancement)", genres)

# Tabs for movie categories
tab1, tab2 = st.tabs(["🔥 Popular Movies", "🎯 Upcoming Movies"])

with tab1:
    st.subheader("Popular Movies")
    popular_movies = get_movies("movie/popular")
    display_movies(popular_movies)

with tab2:
    st.subheader("Upcoming Movies")
    upcoming_movies = get_movies("movie/upcoming")
    display_movies(upcoming_movies)

# Optional: Add a footer
st.markdown("""
---
Built with ❤️ using Streamlit and TMDB API
""")
