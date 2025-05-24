import streamlit as st
import requests
from streamlit.components.v1 import html

st.set_page_config(page_title="🎬 Movie Magic", layout="wide")
st.title("🎬 Welcome to Movie Magic!")

API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"  # balanced quality vs speed

# Sidebar
year = st.sidebar.selectbox("Year", list(range(2025, 1990, -1)))
language = st.sidebar.selectbox("Language", ["en", "hi", "ta", "te", "ml"])

def fetch_movies(category, year, language, limit=20):
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
        params = {"api_key": API_KEY, "language": "en-US", "region": "IN"}
    else:
        return []

    res = requests.get(endpoint, params=params)
    return res.json().get("results", [])[:limit]

def get_trailer(movie_id):
    res = requests.get(f"{BASE_URL}/movie/{movie_id}/videos", params={"api_key": API_KEY})
    for v in res.json().get("results", []):
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={v['key']}"
    return None

def get_watch_link(movie_id):
    res = requests.get(f"{BASE_URL}/movie/{movie_id}/watch/providers", params={"api_key": API_KEY})
    return res.json().get("results", {}).get("IN", {}).get("link")

def render_carousel(title, movies, show_info=True):
    st.subheader(title)

    st.markdown("""
    <style>
    .carousel-container {
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 1rem;
    }
    .movie-card {
        flex: 0 0 auto;
        scroll-snap-align: start;
        width: 180px;
        margin-right: 20px;
        border-radius: 12px;
        background-color: #111;
        color: #fff;
        box-shadow: 0 4px 10px rgba(255,255,255,0.1);
        transition: transform 0.3s;
    }
    .movie-card:hover {
        transform: scale(1.05);
    }
    .movie-card img {
        width: 100%;
        height: 270px;
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
        top: 8px;
        left: 8px;
        background-color: gold;
        color: black;
        padding: 4px 8px;
        font-size: 0.7rem;
        font-weight: bold;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    html_code = "<div class='carousel-container'>"
    for m in movies:
        poster = IMAGE_BASE + m["poster_path"] if m.get("poster_path") else ""
        trailer = get_trailer(m["id"])
        watch_link = get_watch_link(m["id"])
        link = watch_link or trailer or "#"
        badge = "<div class='watch-now'>Watch Now</div>" if watch_link else ""

        info = f"""
        <div class='movie-info'>
            <strong>{m.get('title','')}</strong><br>
            <small>{m.get('release_date','')}</small><br>
            <small>⭐ {m.get('vote_average','')}</small>
        </div>
        """ if show_info else ""

        card = f"""
        <div class='movie-card'>
            <div style='position: relative;'>
                {badge}
                <img src="{poster}" onclick="window.open('{link}', '_blank')">
            </div>
            {info}
        </div>
        """
        html_code += card
    html_code += "</div>"

    html(html_code, height=400)

# Fetch and display
popular = fetch_movies("popular", year, language)
upcoming = fetch_movies("upcoming", year, language)

render_carousel("🔥 Popular Movies", popular)
render_carousel("🎬 Upcoming Movies", upcoming, show_info=False)
