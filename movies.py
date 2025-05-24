import streamlit as st 
import requests

--- Page Config ---

st.set_page_config(layout="wide", page_title="Movie Explorer")

--- Load API Key from secrets ---

API_KEY = st.secrets["TMDB_API_KEY"] BASE_URL = "https://api.themoviedb.org/3" IMG_BASE_URL = "https://image.tmdb.org/t/p/w500"

--- Fetch Movies ---

def fetch_movies(category="popular"): url = f"{BASE_URL}/movie/{category}?api_key={API_KEY}&language=en-US&page=1" response = requests.get(url) if response.status_code == 200: return response.json().get("results", []) else: st.error("Failed to fetch movie data.") return []

--- Render Movie Carousel ---

def render_movie_carousel(title, movies): st.markdown(f""" <h2 style='margin-bottom: 10px;'> {title} </h2> <div class='scrolling-wrapper'> """, unsafe_allow_html=True)

for movie in movies:
    poster_path = movie.get("poster_path")
    poster_url = f"{IMG_BASE_URL}{poster_path}" if poster_path else ""
    movie_title = movie.get("title")
    release_date = movie.get("release_date")
    rating = movie.get("vote_average")

    st.markdown(f"""
    <div class='card'>
        <img src='{poster_url}' class='poster' />
        <div class='card-body'>
            <h4>{movie_title}</h4>
            <p>Release: {release_date}</p>
            <p>Rating: ⭐ {rating}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div><hr>", unsafe_allow_html=True)

--- Custom CSS ---

st.markdown(""" <style> .scrolling-wrapper { display: flex; flex-wrap: nowrap; overflow-x: auto; padding-bottom: 10px; } .scrolling-wrapper::-webkit-scrollbar { height: 8px; } .scrolling-wrapper::-webkit-scrollbar-thumb { background: #888; border-radius: 4px; } .card { flex: 0 0 auto; width: 200px; margin-right: 15px; background: #1e1e1e; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.3); } .poster { width: 100%; height: 300px; object-fit: cover; } .card-body { padding: 10px; color: white; } h2 { color: white; } </style> """, unsafe_allow_html=True)

--- Main App ---

st.title("Movie Dashboard")

popular_movies = fetch_movies("popular") upcoming_movies = fetch_movies("upcoming")

tabs = st.tabs(["🔥 Popular Movies", "🎯 Upcoming Movies"])

with tabs[0]: render_movie_carousel("🔥 Popular Movies", popular_movies)

with tabs[1]: render_movie_carousel("🎯 Upcoming Movies", upcoming_movies)

