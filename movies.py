import streamlit as st
import requests

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Movie Magic", layout="wide", page_icon="🎬")

# ── API Keys ───────────────────────────────────────────────────────────────────
st.write("Available secrets:", dict(st.secrets))

TMDB_API_KEY = st.secrets.get("TMDB_API_KEY")
OMDB_API_KEY = st.secrets.get("OMDB_API_KEY")

st.write("TMDB Key Found:", TMDB_API_KEY is not None)
st.write("OMDB Key Found:", OMDB_API_KEY is not None)


TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Playfair+Display:wght@700&family=DM+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    background-color: #080810 !important;
    color: #fff;
    font-family: 'DM Sans', sans-serif;
}

.main-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 52px;
    letter-spacing: 8px;
    background: linear-gradient(90deg, #ff6b6b, #feca57, #ff9ff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
    margin-bottom: 4px;
}

.subtitle {
    color: #444;
    font-size: 12px;
    letter-spacing: 4px;
    margin-bottom: 32px;
}

/* Card wrapper */
.movie-card {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    background: #111;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    box-shadow: 0 8px 40px rgba(0,0,0,0.6);
}
.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.8);
}

.movie-card img {
    width: 100%;
    display: block;
    border-radius: 20px 20px 0 0;
}

/* Gradient overlay on poster */
.poster-wrap {
    position: relative;
    border-radius: 20px 20px 0 0;
    overflow: hidden;
}
.poster-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.3) 55%, transparent 100%);
    border-radius: 20px 20px 0 0;
}

/* Rating chips on poster */
.rating-chips {
    position: absolute;
    bottom: 12px;
    left: 12px;
    right: 12px;
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}
.chip {
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'Bebas Neue', cursive;
    font-size: 13px;
    letter-spacing: 1px;
    backdrop-filter: blur(8px);
}
.chip-tmdb  { background: rgba(1,180,228,0.25);  color: #01b4e4; border: 1px solid rgba(1,180,228,0.4); }
.chip-imdb  { background: rgba(245,197,24,0.2);   color: #f5c518; border: 1px solid rgba(245,197,24,0.4); }
.chip-rt    { background: rgba(250,80,80,0.2);    color: #ff6b6b; border: 1px solid rgba(250,80,80,0.4); }

/* Title and meta */
.card-body {
    padding: 14px 14px 16px;
    background: #111;
    border-radius: 0 0 20px 20px;
}
.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 15px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card-meta {
    color: #555;
    font-size: 11px;
    letter-spacing: 1px;
}
.card-overview {
    color: #777;
    font-size: 11px;
    line-height: 1.5;
    margin-top: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.trailer-btn {
    display: inline-block;
    margin-top: 10px;
    padding: 5px 14px;
    background: linear-gradient(135deg, #ff6b6b, #feca57);
    color: #000 !important;
    font-family: 'Bebas Neue', cursive;
    font-size: 13px;
    letter-spacing: 2px;
    border-radius: 20px;
    text-decoration: none !important;
}

/* Nav area */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin: 24px 0 8px;
}
.nav-counter {
    font-family: 'Bebas Neue', cursive;
    font-size: 22px;
    color: #444;
    letter-spacing: 2px;
    min-width: 80px;
    text-align: center;
}

/* Category tabs */
.tab-row {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}
.tab-btn {
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif;
    letter-spacing: 1px;
    cursor: pointer;
    border: none;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0d18 !important;
}
section[data-testid="stSidebar"] * { color: #ccc !important; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* Swipe hint bar */
.swipe-hint {
    text-align: center;
    color: #333;
    font-size: 11px;
    letter-spacing: 3px;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_genre_map():
    r = requests.get(f"{TMDB_BASE_URL}/genre/movie/list",
                     params={"api_key": TMDB_API_KEY, "language": "en-US"}, timeout=8)
    if r.status_code == 200:
        return {g["name"].lower(): g["id"] for g in r.json().get("genres", [])}
    return {}


@st.cache_data(show_spinner=False)
def fetch_movies(category, year=None, genre_id=None, language=None):
    params = {"api_key": TMDB_API_KEY, "language": "en-US",
              "sort_by": "popularity.desc", "page": 1}
    if year:       params["primary_release_year"] = year
    if genre_id:   params["with_genres"] = genre_id
    if language:   params["with_original_language"] = language
    r = requests.get(f"{TMDB_BASE_URL}/movie/{category}", params=params, timeout=8)
    if r.status_code == 200:
        return r.json().get("results", [])[:12]
    return []


@st.cache_data(show_spinner=False)
def fetch_trailer(movie_id):
    r = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}/videos",
                     params={"api_key": TMDB_API_KEY}, timeout=8)
    if r.status_code == 200:
        for v in r.json().get("results", []):
            if v["site"] == "YouTube" and v["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={v['key']}"
    return None


@st.cache_data(show_spinner=False)
def fetch_ratings(title):
    r = requests.get(f"http://www.omdbapi.com/",
                     params={"t": title, "apikey": OMDB_API_KEY}, timeout=8)
    if r.status_code == 200:
        data = r.json()
        imdb = data.get("imdbRating", "N/A")
        rt = next((x["Value"] for x in data.get("Ratings", [])
                   if x["Source"] == "Rotten Tomatoes"), "N/A")
        return imdb, rt
    return "N/A", "N/A"


def render_card(movie):
    """Render a single movie card as HTML."""
    title     = movie.get("title", "Unknown")
    date      = movie.get("release_date", "")
    year      = date[:4] if date else "TBA"
    overview  = movie.get("overview", "")
    tmdb_score = f"{movie.get('vote_average', 0):.1f}"
    poster_path = movie.get("poster_path")
    poster_url  = (TMDB_IMAGE_BASE_URL + poster_path) if poster_path else ""

    imdb, rt = fetch_ratings(title)
    trailer  = fetch_trailer(movie["id"])

    chips_html = f'<span class="chip chip-tmdb">TMDB {tmdb_score}</span>'
    if imdb != "N/A":
        chips_html += f'<span class="chip chip-imdb">IMDb {imdb}</span>'
    if rt != "N/A":
        chips_html += f'<span class="chip chip-rt">RT {rt}</span>'

    if poster_url:
        poster_html = f'<img src="{poster_url}" alt="{title}" style="width:100%;display:block;">'
    else:
        poster_html = (
            '<div style="width:100%;height:260px;background:linear-gradient(135deg,#1a1a2e,#0f3460);'
            'display:flex;align-items:center;justify-content:center;font-size:60px;opacity:0.3;">&#127916;</div>'
        )

    trailer_btn = ""
    if trailer:
        trailer_btn = f'<a class="trailer-btn" href="{trailer}" target="_blank">&#9654; WATCH TRAILER</a>'

    return f"""
<div class="movie-card">
  <div class="poster-wrap">
    {poster_html}
    <div class="poster-overlay"></div>
    <div class="rating-chips">{chips_html}</div>
  </div>
  <div class="card-body">
    <div class="card-title" title="{title}">{title}</div>
    <div class="card-meta">{year}</div>
    <div class="card-overview">{overview}</div>
    {trailer_btn}
  </div>
</div>
"""


# ── State ──────────────────────────────────────────────────────────────────────
if "page_index" not in st.session_state:
    st.session_state.page_index = 0
if "category" not in st.session_state:
    st.session_state.category = "popular"

CARDS_PER_PAGE = 4

CATEGORIES = {
    "popular":    "&#128293; Popular",
    "upcoming":   "&#127917; Upcoming",
    "now_playing":"&#127916; Now Playing",
    "top_rated":  "&#11088; Top Rated",
}

LANGUAGES = {"": "All", "en": "EN", "hi": "HI", "ta": "TA", "te": "TE", "ml": "ML"}

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")
    year = st.selectbox("Year", list(range(2025, 1990, -1)), index=0)
    genre_input = st.text_input("Genre (e.g. Action, Comedy)").strip().lower()
    lang_label  = st.selectbox("Language", list(LANGUAGES.values()))
    lang_code   = {v: k for k, v in LANGUAGES.items()}[lang_label]

genre_map = get_genre_map()
genre_id  = genre_map.get(genre_input) if genre_input else None

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">MOVIE MAGIC</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">SWIPE THROUGH THE LATEST FILMS</div>', unsafe_allow_html=True)

# ── Category tabs (buttons) ────────────────────────────────────────────────────
cols = st.columns(len(CATEGORIES))
for i, (cat_id, cat_label) in enumerate(CATEGORIES.items()):
    with cols[i]:
        if st.button(cat_label, key=f"cat_{cat_id}",
                     type="primary" if st.session_state.category == cat_id else "secondary",
                     use_container_width=True):
            st.session_state.category = cat_id
            st.session_state.page_index = 0
            st.rerun()

st.markdown("---")

# ── Fetch movies ───────────────────────────────────────────────────────────────
with st.spinner("Loading movies..."):
    movies = fetch_movies(
        st.session_state.category,
        year=year,
        genre_id=genre_id,
        language=lang_code or None
    )

if not movies:
    st.warning("No movies found. Try adjusting the filters.")
    st.stop()

total = len(movies)
idx   = st.session_state.page_index
start = idx * CARDS_PER_PAGE
end   = min(start + CARDS_PER_PAGE, total)
page_movies = movies[start:end]
total_pages = (total + CARDS_PER_PAGE - 1) // CARDS_PER_PAGE

# ── Swipe hint ─────────────────────────────────────────────────────────────────
st.markdown('<div class="swipe-hint">&#8592; USE ARROWS TO BROWSE &nbsp; | &nbsp; HOVER CARDS FOR DETAILS &#8594;</div>',
            unsafe_allow_html=True)

# ── Movie cards grid ───────────────────────────────────────────────────────────
card_cols = st.columns(CARDS_PER_PAGE)
for i, movie in enumerate(page_movies):
    with card_cols[i]:
        st.markdown(render_card(movie), unsafe_allow_html=True)

# ── Navigation ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
nav_l, nav_mid, nav_r = st.columns([1, 2, 1])

with nav_l:
    if st.button("&#8592; Prev", disabled=(idx == 0), use_container_width=True):
        st.session_state.page_index -= 1
        st.rerun()

with nav_mid:
    st.markdown(
        f'<div style="text-align:center;font-family:\'Bebas Neue\',cursive;font-size:20px;'
        f'color:#555;letter-spacing:3px;padding-top:6px;">'
        f'PAGE {idx + 1} / {total_pages}</div>',
        unsafe_allow_html=True
    )

with nav_r:
    if st.button("Next &#8594;", disabled=(idx >= total_pages - 1), use_container_width=True):
        st.session_state.page_index += 1
        st.rerun()
