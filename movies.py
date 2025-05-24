import streamlit as st 
import requests from streamlit.components.v1 
import html

Set up page

st.set_page_config(page_title="🎬 Movie Magic!", layout="wide") st.title("🎬 Welcome to Movie Magic!")

Constants

TMDB_API_KEY = st.secrets["TMDB_API_KEY"] OMDB_API_KEY = st.secrets["OMDB_API_KEY"] BASE_URL = "https://api.themoviedb.org/3" IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

Functions

@st.cache_data(show_spinner=False) def fetch_movies(endpoint, year=None, genre_id=None, language=None): params = {"api_key": TMDB_API_KEY, "language": "en-US"} if year: params["primary_release_year"] = year if genre_id: params["with_genres"] = genre_id if language: params["with_original_language"] = language res = requests.get(f"{BASE_URL}/discover/movie", params=params) return res.json().get("results", [])

@st.cache_data(show_spinner=False) def get_trailer(movie_id): url = f"{BASE_URL}/movie/{movie_id}/videos" res = requests.get(url, params={"api_key": TMDB_API_KEY}) videos = res.json().get("results", []) for v in videos: if v["site"] == "YouTube" and v["type"] == "Trailer": return f"https://www.youtube.com/embed/{v['key']}" return None

@st.cache_data(show_spinner=False) def get_omdb_ratings(title): url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}" r = requests.get(url).json() imdb = r.get("imdbRating", "N/A") rt = next((s['Value'] for s in r.get("Ratings", []) if s['Source'] == "Rotten Tomatoes"), "N/A") return imdb, rt

@st.cache_data(show_spinner=False) def get_genres(): url = f"{BASE_URL}/genre/movie/list" res = requests.get(url, params={"api_key": TMDB_API_KEY}) return res.json().get("genres", [])

Sidebar filters

st.sidebar.header("Filter Popular Movies") year = st.sidebar.selectbox("Year", list(range(2025, 1990, -1))) all_genres = get_genres() genre_map = {g["name"]: g["id"] for g in all_genres} selected_genre = st.sidebar.selectbox("Genre", ["All"] + list(genre_map.keys())) genre_id = genre_map.get(selected_genre) if selected_genre != "All" else None language = st.sidebar.selectbox("Language", ["All", "en", "hi", "ta", "te", "ml"]) selected_language = None if language == "All" else language

Search box

search_query = st.text_input("Search Movie Title")

Fetch data

popular_movies = fetch_movies("movie/popular", year, genre_id, selected_language) upcoming_movies = fetch_movies("movie/upcoming", year)

if search_query: popular_movies = [m for m in popular_movies if search_query.lower() in m.get("title", "").lower()] upcoming_movies = [m for m in upcoming_movies if search_query.lower() in m.get("title", "").lower()]

CSS + JS for carousel

st.markdown("""

<style>
.slider {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 20px;
  padding: 20px 0;
}
.card {
  flex: 0 0 auto;
  scroll-snap-align: start;
  background: #111;
  border-radius: 12px;
  width: 200px;
  text-align: center;
  color: white;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}
.card img {
  width: 100%;
  border-radius: 12px 12px 0 0;
  cursor: pointer;
}
.card-info {
  padding: 10px;
}
iframe {
  border-radius: 12px;
}
</style>""", unsafe_allow_html=True)

Render carousel section

def render_carousel(movies, section_title, show_details=True): st.subheader(section_title) if not movies: st.write("No movies found.") return carousel_html = "<div class='slider'>" for movie in movies: poster = IMAGE_BASE + movie["poster_path"] if movie.get("poster_path") else "" trailer = get_trailer(movie["id"]) title = movie.get("title", "") release = movie.get("release_date", "") tmdb_rating = movie.get("vote_average", "") imdb_rating, rt_rating = get_omdb_ratings(title) card_info = f"<strong>{title}</strong><br/><small>Release: {release}</small><br/><small>TMDB: {tmdb_rating} ⭐</small><br/><small>IMDb: {imdb_rating}</small><br/><small>RT: {rt_rating}</small>" if show_details else "" embed = f'<iframe width="200" height="120" src="{trailer}" allowfullscreen></iframe>' if trailer else f'<img src="{poster}" alt="{title}" />' card = f''' <div class="card"> {embed} <div class="card-info"> {card_info} </div> </div> ''' carousel_html += card carousel_html += "</div>" html(carousel_html, height=400)

Display sections

render_carousel(upcoming_movies, f"Upcoming Movies ({year})", show_details=False) render_carousel(popular_movies, f"Popular Movies ({year})", show_details=True)

