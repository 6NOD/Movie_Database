import streamlit as st
import requests

# Page config
st.set_page_config(page_title="🎬 Movie Magic!", layout="wide")
st.title("🎬 Welcome to Movie Magic!")

# API Keys from secrets
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
OMDB_API_KEY = st.secrets["OMDB_API_KEY"]

# URLs
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Fetch genre map
@st.cache_data
def get_genre_map():
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    genre_map = {}
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        genre_map = {genre["name"].lower(): genre["id"] for genre in genres}
    return genre_map

# Fetch movies from TMDB
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
        return response.json().get("results", [])[:10]
    return []

# Fetch trailer
def fetch_trailer(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/videos"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        videos = response.json().get("results", [])
        for video in videos:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# Fetch ratings
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
    return "N/A", "N/A"

# Display movies
def display_movies(movies, show_details=True):
    for i in range(0, len(movies), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j >= len(movies):
                break
            movie = movies[i + j]
            with cols[j]:
                poster_url = TMDB_IMAGE_BASE_URL + movie["poster_path"] if movie.get("poster_path") else ""
                trailer_url = fetch_trailer(movie["id"])
                imdb_rating, rt_rating = fetch_ratings(movie['title'])

                if trailer_url:
                    st.markdown(f'''
                        <a href="{trailer_url}" target="_blank">
                            <img src="{poster_url}" style="width:100%; border-radius:10px;">
                        </a>
                        ''', unsafe_allow_html=True)
                else:
                    st.image(poster_url, use_container_width=True)

                st.markdown(f"**{movie['title']}**")
                if show_details:
                    st.markdown(f"Release Date: {movie.get('release_date', 'N/A')}")
                    st.markdown(f"TMDB Rating: {movie.get('vote_average', 'N/A')}")
                    st.markdown(f"IMDb Rating: {imdb_rating}")
                    st.markdown(f"Rotten Tomatoes: {rt_rating}")

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)))
genre_input = st.sidebar.text_input("Enter Genre (e.g., Action, Comedy)").strip().lower()
language = st.sidebar.selectbox("Select Language", ["All", "en", "hi", "ta", "te", "ml"])
language = None if language == "All" else language

# Genre ID from name
genre_map = get_genre_map()
genre_id = genre_map.get(genre_input) if genre_input else None

# Sections in expanders
with st.expander("🔥 Popular Movies", expanded=True):
    popular_movies = fetch_movies("popular", year=year, genre_id=genre_id, language=language)
    display_movies(popular_movies)

with st.expander("🍿 Upcoming Movies"):
    upcoming_movies = fetch_movies("upcoming", year=year, genre_id=genre_id, language=language)
    display_movies(upcoming_movies, show_details=False)

with st.expander("🎬 New on Netflix"):
    netflix_movies = fetch_movies("now_playing", language="en")
    display_movies(netflix_movies, show_details=False)

with st.expander("📺 New on Amazon Prime"):
    amazon_movies = fetch_movies("top_rated", language="en")
    display_movies(amazon_movies, show_details=False)

