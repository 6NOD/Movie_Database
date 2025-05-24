import streamlit as st
import requests

# Set up page configuration
st.set_page_config(page_title="🎬 Movie Magic!", layout="wide")
st.title("🎬 Welcome to Movie Magic!")

# Retrieve API keys from secrets
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
OMDB_API_KEY = st.secrets["OMDB_API_KEY"]

# Base URLs
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Fetch genre mapping from TMDB
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

# Function to fetch movies or series

def fetch_items(endpoint, item_type="movie", limit=10):
    url = f"{TMDB_BASE_URL}/{endpoint}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])[:limit]
    else:
        return []

# Function to fetch trailer URL
def fetch_trailer(item_id, item_type="movie"):
    url = f"{TMDB_BASE_URL}/{item_type}/{item_id}/videos"
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

# Function to display cards with trailers
def display_items(items, show_details=True):
    for i in range(0, len(items), 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j >= len(items):
                break
            item = items[i + j]
            with cols[j]:
                poster_url = TMDB_IMAGE_BASE_URL + item["poster_path"] if item.get("poster_path") else ""
                trailer_url = fetch_trailer(item["id"], item_type="movie")
                with st.container():
                    if trailer_url:
                        st.image(poster_url, use_container_width=True)
                        st.video(trailer_url)
                    else:
                        st.image(poster_url, use_container_width=True)
                    st.markdown(f"**{item['title'] if 'title' in item else item['name']}**")
                    if show_details:
                        st.markdown(f"Release: {item.get('release_date', item.get('first_air_date', 'N/A'))}")
                        st.markdown(f"TMDB Rating: {item.get('vote_average', 'N/A')}")
                        imdb_rating, rt_rating = fetch_ratings(item['title'] if 'title' in item else item['name'])
                        st.markdown(f"IMDb: {imdb_rating} | RT: {rt_rating}")

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)))
genre_input = st.sidebar.text_input("Enter Genre (e.g., Action, Comedy)").strip().lower()
language = st.sidebar.selectbox("Select Language", ["All", "en", "hi", "ta", "te", "ml"])
language = None if language == "All" else language

# Fetch genre ID
genre_map = get_genre_map()
genre_id = genre_map.get(genre_input) if genre_input else None

# Sections
st.subheader("🔥 Top 10 Popular Movies")
popular_movies = fetch_items("movie/popular", limit=10)
display_items(popular_movies)

st.subheader("🎯 Top 10 Upcoming Movies")
upcoming_movies = fetch_items("movie/upcoming", limit=10)
display_items(upcoming_movies, show_details=False)

st.subheader("🆕 Recently Added on Netflix")
netflix_movies = fetch_items("movie/now_playing", limit=10)
display_items(netflix_movies, show_details=False)

st.subheader("⭐ New on Amazon Prime")
amazon_movies = fetch_items("movie/top_rated", limit=10)
display_items(amazon_movies, show_details=False)
