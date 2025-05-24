import streamlit as st
import requests
from streamlit.components.v1 import html

# Page setup
st.set_page_config(page_title="🎬 Movie Magic", layout="wide")
st.title("🎬 Welcome to Movie Magic!")

# Constants
API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w780"  # High-res posters

# Sidebar filters
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)), index=0)
language = st.sidebar.selectbox("Language", ["en", "hi", "ta", "te", "ml"], index=0)

# Fetch movie data
def fetch_movies(category, year, language, limit=12):
    if category == "popular":
        endpoint = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "region": "IN",
            "sort_by": "popularity.desc",
            "with_original_language": language,
            "primary_release_year": year,
        }
    elif category == "upcoming":
        endpoint = f"{BASE_URL}/movie/upcoming"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "region": "IN",
        }
    else:
        return []
    
    res = requests.get(endpoint, params=params)
    return res.json().get("results", [])[:limit]

# Get trailer/watch link
def get_trailer(movie_id):
    res = requests.get(f"{BASE_URL}/movie/{movie_id}/videos", params={"api_key": API_KEY})
    for v in res.json().get("results", []):
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={v['key']}"
    return None

def get_watch_link(movie_id):
    res = requests.get(f"{BASE_URL}/movie/{movie_id}/watch/providers", params={"api_key": API_KEY})
    return res.json().get("results", {}).get("IN", {}).get("link")

# Render carousel
def render_carousel(title, movies, show_info=True):
    st.subheader(title)
    if not movies:
        st.warning("No movies found.")
        return

    # CSS for smooth swipe
    st.markdown("""
    <style>
    .movie-carousel {
        display: flex;
        overflow-x: scroll;
        scroll-behavior: smooth;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 20px;
    }
    .movie-card {
        flex: 0 0 auto;
        width: 220px;
        margin-right: 16px;
        background-color: #111;
        color: #fff;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(255,255,255,0.1);
        position: relative;
    }
    .movie-card img {
        width: 100%;
        height: 330px;
        object-fit: cover;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        cursor: pointer;
    }
    .movie-info {
        padding: 10px;
        font-size: 0.85rem;
        text-align: center;
    }
    .watch-now {
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: gold;
        color: black;
        padding: 4px 8px;
        font-size: 0.75rem;
        font-weight: bold;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    # HTML content
    carousel = "<div class='movie-carousel'>"
    for movie in movies:
        poster = IMAGE_BASE + movie["poster_path"] if movie.get("poster_path") else ""
        trailer = get_trailer(movie["id"])
        watch_link = get_watch_link(movie["id"])
        link = watch_link or trailer or "#"

        badge = "<div class='watch-now'>Watch Now</div>" if watch_link else ""
        info = f"""
        <div class='movie-info'>
            <strong>{movie.get('title','')}</strong><br>
            <small>{movie.get('release_date','')}</small><br>
            <small>⭐ {movie.get('vote_average','')}</small>
        </div>""" if show_info else ""

        carousel += f"""
        <div class='movie-card'>
            {badge}
            <img src="{poster}" onclick="window.open('{link}', '_blank')">
            {info}
        </div>"""
    carousel += "</div>"

    html(carousel, height=430)

# Fetch and display
popular = fetch_movies("popular", year, language)
upcoming = fetch_movies("upcoming", year, language)

render_carousel("Popular Movies", popular)
render_carousel("Upcoming Movies", upcoming, show_info=False)
