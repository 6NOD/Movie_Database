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

# Helper to fetch movies
def fetch_movies(category, year, language, limit=10):
    if category == "popular":
        endpoint = f"{BASE_URL}/discover/movie"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "region": "IN",
            "sort_by": "popularity.desc",
            "with_original_language": language,
            "primary_release_year": year
        }
    elif category == "upcoming":
        endpoint = f"{BASE_URL}/movie/upcoming"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "region": "IN"
        }
    else:
        return []
    res = requests.get(endpoint, params=params)
    return res.json().get("results", [])[:limit]

def get_trailer(movie_id):
    res = requests.get(f"{BASE_URL}/movie/{movie_id}/videos", params={"api_key": API_KEY})
    for v in res.json().get("results", []):
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/embed/{v['key']}"
    return None

def get_watch_link(movie_id):
    res = requests.get(f"{BASE_URL}/movie/{movie_id}/watch/providers", params={"api_key": API_KEY})
    return res.json().get("results", {}).get("IN", {}).get("link")

# Sidebar filters
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)), index=0)
language = st.sidebar.selectbox("Language", ["en", "hi", "ta", "te", "ml"], index=0)

# CSS + JS Carousel
carousel_css = """
<style>
.scroll-wrapper {
  overflow-x: scroll;
  overflow-y: hidden;
  white-space: nowrap;
  padding-bottom: 1rem;
}
.scroll-wrapper::-webkit-scrollbar {
  height: 8px;
}
.scroll-wrapper::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}
.card {
  display: inline-block;
  width: 200px;
  margin-right: 16px;
  vertical-align: top;
  background: #111;
  color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(255,255,255,0.1);
}
.card img {
  width: 100%;
  height: auto;
  display: block;
  cursor: pointer;
}
.card-info {
  padding: 10px;
  text-align: center;
  font-size: 0.9rem;
}
.watch-now {
  position: absolute;
  background: gold;
  color: black;
  font-weight: bold;
  font-size: 0.8rem;
  padding: 4px 6px;
  border-radius: 6px;
  top: 10px;
  left: 10px;
}
.card-container {
  position: relative;
}
</style>
"""

# Carousel renderer
def render_carousel(title, movies, show_info=True):
    st.subheader(title)
    if not movies:
        st.warning("No movies found.")
        return

    html_code = "<div class='scroll-wrapper'>"
    for m in movies:
        poster = IMAGE_BASE + m["poster_path"] if m.get("poster_path") else ""
        trailer = get_trailer(m["id"])
        watch_link = get_watch_link(m["id"])
        link = watch_link if watch_link else trailer
        badge = "<div class='watch-now'>Watch Now</div>" if watch_link else ""

        info = f"""
        <div class='card-info'>
            <strong>{m.get('title','')}</strong><br>
            <small>{m.get('release_date','')}</small><br>
            <small>⭐ {m.get('vote_average','')}</small>
        </div>""" if show_info else ""

        card = f"""
        <div class='card'>
            <div class='card-container'>
                {badge}
                <img src='{poster}' onclick="window.open('{link}', '_blank')">
            </div>
            {info}
        </div>
        """
        html_code += card
    html_code += "</div>"

    st.markdown(carousel_css, unsafe_allow_html=True)
    html(html_code, height=400)

# Fetch and display
popular = fetch_movies("popular", year, language)
upcoming = fetch_movies("upcoming", year, language)

render_carousel("Popular Movies", popular)
render_carousel("Upcoming Movies", upcoming, show_info=False)
