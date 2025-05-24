import streamlit as st
import requests
import pandas as pd

# Set up page configuration
st.set_page_config(page_title="🎬 Movie Magic!", layout="wide")
st.title("🎬 Welcome to Movie Magic!")

# Retrieve API keys from secrets
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
OMDB_API_KEY = st.secrets["OMDB_API_KEY"]

# Base URLs
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Function to fetch movies from TMDB
def fetch_movies(category, year=None, genre_id=None, language=None):
    url = f"{TMDB_BASE_URL}/movie/{category}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": 1
    }
    if year:
        params["primary_release_year"] = year
    if genre_id:
        params["with_genres"] = genre_id
    if language:
        params["with_original_language"] = language

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []

# Function to fetch trailer URL
def fetch_trailer(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        videos = response.json().get("results", [])
        for video in videos:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/embed/{video['key']}"
    return None

# Function to fetch ratings from OMDb
def fetch_ratings(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        imdb_rating = data.get("imdbRating", "N/A")
        rt_rating = "N/A"
        for rating in data.get("Ratings", []):
            if rating["Source"] == "Rotten Tomatoes":
                rt_rating = rating["Value"]
        return imdb_rating, rt_rating
    else:
        return "N/A", "N/A"

# Function to display movies in a responsive grid
def display_movies(movies, show_details=True):
    cols = st.columns(5)
    for index, movie in enumerate(movies):
        with cols[index % 5]:
            poster_url = TMDB_IMAGE_BASE_URL + movie["poster_path"] if movie.get("poster_path") else ""
            st.image(poster_url, use_comtainer_width=True)
            if show_details:
                st.markdown(f"**{movie['title']}**")
                st.markdown(f"Release Date: {movie.get('release_date', 'N/A')}")
                st.markdown(f"TMDB Rating: {movie.get('vote_average', 'N/A')}")
                imdb_rating, rt_rating = fetch_ratings(movie['title'])
                st.markdown(f"IMDb Rating: {imdb_rating}")
                st.markdown(f"Rotten Tomatoes: {rt_rating}")
                trailer_url = fetch_trailer(movie["id"])
                if trailer_url:
                    st.video(trailer_url)

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)))
genre = st.sidebar.text_input("Enter Genre (e.g., Action, Comedy)")
language = st.sidebar.selectbox("Select Language", ["All", "en", "hi", "ta", "te", "ml"])
language = None if language == "All" else language

# Fetch and display popular movies
st.subheader("Popular Movies")
popular_movies = fetch_movies("popular", year=year, language=language)
display_movies(popular_movies)

# Fetch and display upcoming movies
st.subheader("Upcoming Movies")
upcoming_movies = fetch_movies("upcoming", year=year, language=language)
display_movies(upcoming_movies, show_details=False)
