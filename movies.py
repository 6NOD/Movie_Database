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

# Sidebar filters
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)))
language = st.sidebar.selectbox("Language", ["en", "hi", "ta", "te", "ml"])

# Helper to fetch movies by year/language
def fetch_movies(year, language, is_upcoming=False):
    endpoint = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "sort_by": "popularity.desc",
        "primary_release_year": year,
        "with_original_language": language,
        "language": "en-US"
    }
    if is_upcoming:
        endpoint = f"{BASE_URL}/movie/upcoming"
        del params["primary_release_year"]
        del params["with_original_language"]
    res = requests.get(endpoint, params=params)
    return res.json().get("results", [])[:10]

# Get trailer link
def get_trailer(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos"
    res = requests.get(url, params={"api_key": API_KEY})
    videos = res.json().get("results", [])
    for v in videos:
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/embed/{v['key']}"
    return "https://www.youtube.com"

# Inject custom CSS
st.markdown("""
<style>
.container {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    gap: 1rem;
    padding: 1rem 0;
}
.card {
    flex: 0 0 auto;
    width: 180px;
    background-color: #111;
    color: white;
    border-radius: 12px;
    scroll-snap-align: start;
    box-shadow: 0 4px 8px rgba(255,255,255,0.1);
    cursor: pointer;
    text-align: center;
}
.card img {
    width: 100%;
    border-radius: 12px 12px 0 0;
}
.card-info {
    padding: 10px;
    font-size: 0.8rem;
}
@media only screen and (max-width: 768px) {
    .card {
        width: 140px;
    }
}
</style>
""", unsafe_allow_html=True)

# Carousel renderer
def render_carousel(title, movies):
    st.subheader(title)
    html_code = "<div class='container'>"
    for movie in movies:
        poster = IMAGE_BASE + movie["poster_path"] if movie.get("poster_path") else ""
        trailer = get_trailer(movie["id"])
        html_code += f"""
            <div class='card' onclick="window.open('{trailer}', '_blank')">
                <img src='{poster}' />
                <div class='card-info'>
                    <strong>{movie.get('title', '')}</strong><br>
                    <small>{movie.get('release_date', '')}</small><br>
                    <small>⭐ {movie.get('vote_average', '')}</small>
                </div>
            </div>
        """
    html_code += "</div>"
    html(html_code, height=400)

# Fetch and render
popular_movies = fetch_movies(year, language)
upcoming_movies = fetch_movies(year, language, is_upcoming=True)

render_carousel("Popular Movies", popular_movies)
render_carousel("Upcoming Movies", upcoming_movies)
