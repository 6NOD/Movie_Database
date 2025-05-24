import streamlit as st
import requests
from streamlit.components.v1 import html

st.set_page_config(page_title="🔥 Movie Magic", layout="wide")

API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

st.markdown("""
<style>
.movie-row {
    display: flex;
    overflow-x: auto;
    gap: 16px;
    padding: 10px 0;
    scroll-snap-type: x mandatory;
}
.movie-card {
    flex: 0 0 auto;
    width: 180px;
    background-color: #111;
    color: white;
    border-radius: 10px;
    box-shadow: 0 0 8px rgba(255,255,255,0.1);
    scroll-snap-align: start;
    transition: transform 0.3s ease;
}
.movie-card:hover {
    transform: scale(1.05);
}
.movie-card img {
    width: 100%;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}
.movie-info {
    padding: 10px;
    font-size: 14px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

def fetch_movies(category, year, language, limit=12):
    if category == "popular":
        endpoint = f"{BASE_URL}/discover/movie"
    else:
        endpoint = f"{BASE_URL}/movie/upcoming"

    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "region": "IN",
        "sort_by": "popularity.desc",
        "with_original_language": language,
    }
    if category == "popular":
        params["primary_release_year"] = year

    res = requests.get(endpoint, params=params)
    movies = res.json().get("results", [])
    return movies[:limit]

def render_movie_row(title, movies):
    st.markdown(f"### {title}")
    html_code = "<div class='movie-row'>"
    for m in movies:
        poster = IMAGE_BASE + m["poster_path"] if m.get("poster_path") else ""
        name = m.get("title", "No Title")
        release = m.get("release_date", "N/A")
        rating = round(m.get("vote_average", 0), 1)

        html_code += f"""
        <div class='movie-card'>
            <img src='{poster}' />
            <div class='movie-info'>
                <h4>{name}</h4>
                <p>Release: {release}</p>
                <p>⭐ {rating}</p>
            </div>
        </div>
        """
    html_code += "</div>"
    html(html_code, height=390)

# Sidebar Filters
year = st.sidebar.selectbox("Year", list(range(2025, 1990, -1)), index=0)
language = st.sidebar.selectbox("Language", ["en", "hi", "ta", "te", "ml"])

popular_movies = fetch_movies("popular", year, language)
upcoming_movies = fetch_movies("upcoming", year, language)

render_movie_row("🔥 Popular Movies", popular_movies)
render_movie_row("🎯 Upcoming Movies", upcoming_movies)
