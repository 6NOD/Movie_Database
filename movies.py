import streamlit as st
import requests
from streamlit.components.v1 import html

# Page configuration
st.set_page_config(page_title="🎬 Welcome to Movie Magic!", layout="wide")
st.markdown("""
    <h1 style='text-align: center; color: white;'>🎬 Welcome to Movie Magic!</h1>
    <style>
        body {background-color: black; color: white; overflow: hidden;}
        .slider {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            gap: 10px;
            padding: 10px;
            -webkit-overflow-scrolling: touch;
        }
        .slider::-webkit-scrollbar {
            display: none;
        }
        .card {
            flex: 0 0 auto;
            scroll-snap-align: start;
            background: #111;
            border-radius: 12px;
            width: 220px;
            color: white;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
            position: relative;
        }
        .card img {
            width: 100%;
            border-radius: 12px;
            cursor: pointer;
        }
        iframe {
            width: 100%;
            height: 200px;
            border: none;
            border-radius: 0 0 12px 12px;
        }
    </style>
""", unsafe_allow_html=True)

# Constants
API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Sidebar filters
st.sidebar.header("Filter Movies")
year = st.sidebar.selectbox("Year", list(range(2025, 1990, -1)))
language = st.sidebar.selectbox("Language", ["en", "hi", "ta", "te", "ml"])

# Functions
def fetch_movies(endpoint, year, language):
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "region": "IN",
        "with_original_language": language,
        "primary_release_year": year,
        "page": 1
    }
    res = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    all_movies = res.json().get("results", [])
    return all_movies[:10]  # limit to 10 movies

def get_trailer(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos"
    res = requests.get(url, params={"api_key": API_KEY})
    videos = res.json().get("results", [])
    for v in videos:
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/embed/{v['key']}"
    return None

def render_carousel(movies, section_title):
    html(f"<h2 style='text-align:center'>{section_title}</h2>", height=30)
    carousel_html = "<div class='slider'>"
    for movie in movies:
        poster = IMAGE_BASE + movie["poster_path"] if movie.get("poster_path") else ""
        trailer = get_trailer(movie["id"])
        title = movie.get("title", "")
        embed = f"<iframe src='{trailer}' allowfullscreen></iframe>" if trailer else ""
        card = f'''
        <div class="card">
            <img src="{poster}" alt="{title}" onclick="window.open('{trailer}', '_blank')" />
            {embed}
        </div>
        '''
        carousel_html += card
    carousel_html += "</div>"
    html(carousel_html, height=380)

# Fetch and render sections
popular_movies = fetch_movies("movie/popular", year, language)
upcoming_movies = fetch_movies("movie/upcoming", year, language)

render_carousel(popular_movies, f"Popular Movies ({year})")
render_carousel(upcoming_movies, f"Upcoming Movies ({year})")
