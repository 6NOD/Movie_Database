import streamlit as st
import requests

# Set up page
st.set_page_config(page_title="🎬 Movie Magic", layout="wide")
st.title("🎬 Movie Magic")

# Constants
API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Sidebar filters
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)), index=0)
language = st.sidebar.selectbox("Language", ["en", "hi", "ta", "te", "ml"], index=0)

# Helper to fetch movies
def fetch_movies(category, year, language, limit=20):
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
    return res.json().get("results", [])[:limit]

# CSS for FMovies-style grid layout
st.markdown("""
<style>
body {
    background-color: #121212;
    color: #FFFFFF;
}
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 20px;
    padding: 10px;
}
.movie-card {
    background-color: #1E1E1E;
    border-radius: 10px;
    overflow: hidden;
    text-align: center;
    transition: transform 0.2s;
    box-shadow: 0 2px 10px rgba(255,255,255,0.1);
}
.movie-card:hover {
    transform: scale(1.05);
}
.movie-poster {
    width: 100%;
    height: 270px;
    object-fit: cover;
}
.movie-info {
    padding: 10px;
}
.movie-info h4 {
    font-size: 1rem;
    margin: 5px 0;
}
.movie-info p {
    font-size: 0.8rem;
    margin: 0;
}
@media (max-width: 600px) {
    .grid-container {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
    .movie-poster {
        height: 200px;
    }
}
</style>
""", unsafe_allow_html=True)

# Grid renderer
def render_grid(title, movies):
    st.subheader(title)
    html_content = '<div class="grid-container">'
    for m in movies:
        poster = IMAGE_BASE + m["poster_path"] if m.get("poster_path") else ""
        html_content += f'''
        <div class="movie-card">
            <img src="{poster}" class="movie-poster" alt="{m.get("title", "No Title")}">
            <div class="movie-info">
                <h4>{m.get("title", "No Title")}</h4>
                <p>Release: {m.get("release_date", "N/A")}</p>
                <p>⭐ {m.get("vote_average", "N/A")}</p>
            </div>
        </div>
        '''
    html_content += '</div>'
    st.markdown(html_content, unsafe_allow_html=True)

# Fetch & Render
popular_movies = fetch_movies("popular", year, language)
upcoming_movies = fetch_movies("upcoming", year, language)

render_grid("🔥 Popular Movies", popular_movies)
render_grid("🎬 Upcoming Movies", upcoming_movies)
