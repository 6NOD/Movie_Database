import streamlit as st 
import requests

Set up page

st.set_page_config(page_title="🎬 Movie Explorer", layout="wide") st.title("🎬 TMDB Movie Explorer")

Constants

API_KEY = st.secrets["TMDB_API_KEY"] BASE_URL = "https://api.themoviedb.org/3" IMAGE_BASE = "https://image.tmdb.org/t/p/w500"  # High-res posters

Functions

def fetch_movies(endpoint, params=None): if params is None: params = {} params["api_key"] = API_KEY params["language"] = "en-US" response = requests.get(f"{BASE_URL}/{endpoint}", params=params) return response.json().get("results", [])

def get_trailer(movie_id): url = f"{BASE_URL}/movie/{movie_id}/videos" res = requests.get(url, params={"api_key": API_KEY}) videos = res.json().get("results", []) for v in videos: if v["site"] == "YouTube" and v["type"] == "Trailer": return f"https://www.youtube.com/watch?v={v['key']}" return None

Sidebar filters

st.sidebar.header("Filter Movies") year = st.sidebar.selectbox("Year", list(range(2025, 1990, -1))) category = st.sidebar.selectbox("Category", ["Popular", "Top Rated", "Upcoming"])

category_map = { "Popular": "movie/popular", "Top Rated": "movie/top_rated", "Upcoming": "movie/upcoming" }

movies = fetch_movies(category_map[category])

Movie Cards

st.markdown("""

<style>
.movie-card {
    border-radius: 12px;
    background-color: #111;
    padding: 10px;
    margin: 5px;
    text-align: center;
    color: #fff;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
    transition: 0.3s ease;
}
.movie-card:hover {
    transform: scale(1.03);
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
}
.movie-poster {
    border-radius: 8px;
    width: 100%;
    height: auto;
}
</style>""", unsafe_allow_html=True)

cols = st.columns(5) st.subheader(f"{category} Movies ({year})")

for idx, movie in enumerate(movies): if movie.get("release_date", "").startswith(str(year)): with cols[idx % 5]: with st.container(): st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True) st.image(f"{IMAGE_BASE}{movie['poster_path']}", caption=movie['title'], use_column_width=True) if st.button("More Info", key=f"btn_{movie['id']}"): st.subheader(movie["title"]) st.write(f"Release Date: {movie['release_date']}") st.write(f"Rating: {movie['vote_average']} ⭐") st.write(f"Overview: {movie['overview']}") trailer = get_trailer(movie["id"]) if trailer: st.video(trailer) else: st.info("Trailer not available.") st.markdown("</div>", unsafe_allow_html=True)

