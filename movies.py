import streamlit as st 
import requests

Set up page

st.set_page_config(page_title="🎬 Movie Explorer", layout="wide") st.title("🎬 TMDB Movie Explorer")

Constants

API_KEY = st.secrets["TMDB_API_KEY"] BASE_URL = "https://api.themoviedb.org/3" IMAGE_BASE = "https://image.tmdb.org/t/p/w500"  # High-res posters

Functions

def fetch_movies(endpoint, params=None): if params is None: params = {} params["api_key"] = API_KEY params["language"] = "en-US" response = requests.get(f"{BASE_URL}/{endpoint}", params=params) return response.json().get("results", [])

def get_trailer(movie_id): url = f"{BASE_URL}/movie/{movie_id}/videos" res = requests.get(url, params={"api_key": API_KEY}) videos = res.json().get("results", []) for v in videos: if v["site"] == "YouTube" and v["type"] == "Trailer": return f"https://www.youtube.com/embed/{v['key']}" return None

Sidebar filters

st.sidebar.header("Filter Movies") year = st.sidebar.selectbox("Year", list(range(2025, 1990, -1))) category = st.sidebar.selectbox("Category", ["Popular", "Top Rated", "Upcoming"])

category_map = { "Popular": "movie/popular", "Top Rated": "movie/top_rated", "Upcoming": "movie/upcoming" }

movies = fetch_movies(category_map[category])

CSS for responsiveness and hover effect

st.markdown("""

<style>
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
}
.movie-card {
    border-radius: 12px;
    background-color: #111;
    padding: 0;
    text-align: center;
    color: #fff;
    overflow: hidden;
    position: relative;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
    transition: transform 0.2s ease;
}
.movie-card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
}
.movie-card img {
    width: 100%;
    display: block;
    border-radius: 12px;
    cursor: pointer;
}
.trailer-embed {
    width: 100%;
    height: 300px;
    margin-top: 10px;
    border: none;
    border-radius: 12px;
}
</style>""", unsafe_allow_html=True)

Display movies

displayed = 0 st.subheader(f"{category} Movies ({year})") st.markdown('<div class="grid-container">', unsafe_allow_html=True)

for movie in movies: if movie.get("release_date", "").startswith(str(year)): trailer_url = get_trailer(movie["id"]) if category == "Upcoming": st.markdown(f""" <div class="movie-card"> <a href="{trailer_url}" target="_blank"> <img src="{IMAGE_BASE}{movie['poster_path']}" alt="{movie['title']}"> </a> </div> """, unsafe_allow_html=True) else: st.markdown(f""" <div class="movie-card"> <a href="#" onclick="window.open('{trailer_url}', '_blank')"> <img src="{IMAGE_BASE}{movie['poster_path']}" alt="{movie['title']}"> </a> <div style="padding:10px"> <strong>{movie['title']}</strong><br> Release: {movie['release_date']}<br> Rating: {movie['vote_average']} ⭐ </div> </div> """, unsafe_allow_html=True) displayed += 1

st.markdown('</div>', unsafe_allow_html=True)

if displayed == 0: st.warning("No movies found for the selected year.")

