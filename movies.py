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
    endpoint = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "primary_release_year": year,
        "with_original_language": language
    }
    res = requests.get(endpoint, params=params)
    return res.json().get("results", [])[:limit]

# Get trailer link
def get_trailer(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos"
    res = requests.get(url, params={"api_key": API_KEY})
    videos = res.json().get("results", [])
    for v in videos:
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/embed/{v['key']}"
    return None

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
}
.card img {
    width: 100%;
    border-radius: 12px 12px 0 0;
    cursor: pointer;
}
.card-info {
    padding: 10px;
    font-size: 0.9rem;
    text-align: center;
}
iframe.trailer {
    width: 100%;
    height: 200px;
    border: none;
    border-radius: 0 0 12px 12px;
}
</style>
""", unsafe_allow_html=True)

# Carousel renderer
def render_carousel(title, movies):
    st.subheader(title)
    if not movies:
        st.warning("No movies found.")
        return

    html_code = "<div class='container'>"
    for m in movies:
        poster = IMAGE_BASE + m["poster_path"] if m.get("poster_path") else ""
        trailer = get_trailer(m["id"])
        card = f"""
        <div class='card'>
            <img src='{poster}' onclick=\"window.open('{trailer}','_blank')\" />
            <div class='card-info'>
                <strong>{m.get('title','')}</strong><br>
                <small>{m.get('release_date','')}</small><br>
                <small>⭐ {m.get('vote_average','')}</small>
            </div>
        </div>
        """
        html_code += card
    html_code += "</div>"
    html(html_code, height=350)

# Fetch data and render
popular = fetch_movies("popular", year, language)
upcoming = fetch_movies("upcoming", year, language)

render_carousel("Popular Movies", popular)
render_carousel("Upcoming Movies", upcoming)
