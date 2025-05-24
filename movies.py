import streamlit as st
import requests

st.set_page_config(page_title="Movie Dashboard", layout="wide")
st.title("🎬 TMDB Movie Dashboard")

API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies(endpoint, params=None):
    if params is None:
        params = {}
    params["api_key"] = API_KEY
    params["language"] = "en-US"
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    return response.json().get("results", [])

def get_trailer(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos"
    res = requests.get(url, params={"api_key": API_KEY})
    videos = res.json().get("results", [])
    for v in videos:
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={v['key']}"
    return None

st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", list(range(2025, 1990, -1)))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upcoming Movies")
    upcoming = fetch_movies("movie/upcoming")
    for movie in upcoming[:5]:
        st.markdown(f"**{movie['title']}** ({movie['release_date']})")
        st.image(f"https://image.tmdb.org/t/p/w200{movie['poster_path']}", width=150)
        st.write(movie["overview"][:200] + "...")

with col2:
    st.subheader(f"Top Movies of {year}")
    top_movies = fetch_movies("discover/movie", {"sort_by": "popularity.desc", "primary_release_year": year})
    for movie in top_movies[:5]:
        st.markdown(f"**{movie['title']}** ({movie['release_date']})")
        st.image(f"https://image.tmdb.org/t/p/w200{movie['poster_path']}", width=150)
        trailer = get_trailer(movie["id"])
        if trailer:
            st.markdown(f"[▶️ Watch Trailer]({trailer})")
          
