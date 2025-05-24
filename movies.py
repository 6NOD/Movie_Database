import streamlit as st
import requests
from streamlit.components.v1 import html

# Set up page
st.set_page_config(page_title="🎬 Welcome to Movie Magic!", layout="wide")
st.title("🎬 Welcome to Movie Magic!")

# Constants
API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Helper to fetch movies by year/language
def fetch_movies(category, year, language, limit=10):
    if category == "popular":
        endpoint = f"{BASE_URL}/discover/movie"
    elif category == "upcoming":
        endpoint = f"{BASE_URL}/movie/upcoming"
    else:
        return []

    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "region": "IN",
        "sort_by": "popularity.desc",
        "with_original_language": language,
        "primary_release_year": year if category == "popular" else None
    }
    res = requests.get(endpoint, params=params)
    movies = res.json().get("results", [])
    return movies[:limit]

# Get trailer link
def get_trailer(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos"
    res = requests.get(url, params={"api_key": API_KEY})
    videos = res.json().get("results", [])
    for v in videos:
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/embed/{v['key']}"
    return None

# Get free watch link if available
def get_watch_link(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    res = requests.get(url, params={"api_key": API_KEY})
    results = res.json().get("results", {})
    link = results.get("IN", {}).get("link")
    return link

# Sidebar filters
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)), index=0)
language = st.sidebar.selectbox("Language", ["en", "hi", "ta", "te", "ml"], index=0)

# CSS for carousel and responsive layout
st.markdown("""
<style>
.container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    gap: 20px;
    padding: 1rem 0;
    margin-bottom: 2rem;
    width: 100%;
}
.card {
    flex: 0 0 auto;
    width: 200px;
    scroll-snap-align: start;
    background: #111;
    color: white;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
}
.card img {
    width: 100%;
    border-radius: 12px 12px 0 0;
    cursor: pointer;
}
.card-info {
    padding: 10px;
    
