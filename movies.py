
import { useState, useRef, useEffect } from "react";

const TMDB_API_KEY = "REPLACE_WITH_YOUR_TMDB_API_KEY";
const OMDB_API_KEY = "REPLACE_WITH_YOUR_OMDB_API_KEY";
const TMDB_BASE = "https://api.themoviedb.org/3";
const IMG_BASE = "https://image.tmdb.org/t/p/w500";

const CATEGORIES = [
  { id: "popular", label: "🔥 Popular" },
  { id: "upcoming", label: "🎟 Upcoming" },
  { id: "now_playing", label: "🎬 Now Playing" },
  { id: "top_rated", label: "⭐ Top Rated" },
];

const LANGUAGES = [
  { code: "", label: "All" },
  { code: "en", label: "EN" },
  { code: "hi", label: "HI" },
  { code: "ta", label: "TA" },
  { code: "te", label: "TE" },
];

// Mock data for demo (replace API calls with real ones using your keys)
const MOCK_MOVIES = [
  { id: 1, title: "Dune: Part Three", release_date: "2026-11-19", vote_average: 8.4, poster_path: null, overview: "Paul Atreides continues his journey across the stars.", imdb: "8.2", rt: "91%" },
  { id: 2, title: "Avatar 3", release_date: "2025-12-19", vote_average: 7.9, poster_path: null, overview: "Jake Sully returns to Pandora for a new adventure.", imdb: "7.5", rt: "84%" },
  { id: 3, title: "The Batman Part II", release_date: "2026-10-02", vote_average: 8.7, poster_path: null, overview: "Bruce Wayne faces his greatest challenge yet.", imdb: "8.9", rt: "95%" },
  { id: 4, title: "Mission: Impossible 8", release_date: "2025-05-23", vote_average: 8.1, poster_path: null, overview: "Ethan Hunt races against time to stop a global threat.", imdb: "7.8", rt: "88%" },
  { id: 5, title: "Blade Runner 2099", release_date: "2026-03-14", vote_average: 7.6, poster_path: null, overview: "A new blade runner hunts rogue replicants in a dying city.", imdb: "7.3", rt: "79%" },
  { id: 6, title: "The Last of Us: Chapter 1", release_date: "2025-08-08", vote_average: 8.5, poster_path: null, overview: "Joel and Ellie's bond is tested in the post-apocalypse.", imdb: "8.7", rt: "97%" },
  { id: 7, title: "Alien: Romulus II", release_date: "2026-07-31", vote_average: 7.8, poster_path: null, overview: "Deep space terror returns with deadly force.", imdb: "7.6", rt: "82%" },
  { id: 8, title: "Interstellar 2", release_date: "2026-11-05", vote_average: 9.1, poster_path: null, overview: "Humanity's second attempt to cross the stars.", imdb: "9.0", rt: "96%" },
];

const GRADIENTS = [
  ["#0f0c29", "#302b63", "#24243e"],
  ["#1a1a2e", "#16213e", "#0f3460"],
  ["#2d1b69", "#11998e", "#38ef7d"],
  ["#1e3c72", "#2a5298", "#7a8de1"],
  ["#360033", "#0b8793", "#5de0e6"],
  ["#4a0030", "#c71f37", "#ff6b6b"],
  ["#003049", "#fcbf49", "#eae2b7"],
  ["#1b1b2f", "#e94560", "#0f3460"],
];

function StarRating({ value }) {
  const stars = Math.round((value / 10) * 5);
  return (
    <div style={{ display: "flex", gap: 2 }}>
      {[1, 2, 3, 4, 5].map((s) => (
        <span key={s} style={{ color: s <= stars ? "#FFD700" : "#555", fontSize: 14 }}>★</span>
      ))}
    </div>
  );
}

function MovieCard({ movie, index, isActive, offset, onSwipe }) {
  const cardRef = useRef(null);
  const startX = useRef(null);
  const currentX = useRef(0);
  const [dragging, setDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState(0);
  const [leaving, setLeaving] = useState(null);
  const grad = GRADIENTS[index % GRADIENTS.length];

  const handleStart = (x) => {
    if (!isActive) return;
    startX.current = x;
    setDragging(true);
  };

  const handleMove = (x) => {
    if (!dragging || startX.current === null) return;
    const diff = x - startX.current;
    currentX.current = diff;
    setDragOffset(diff);
  };

  const handleEnd = () => {
    if (!dragging) return;
    setDragging(false);
    const threshold = 100;
    if (currentX.current > threshold) {
      setLeaving("right");
      setTimeout(() => { setLeaving(null); setDragOffset(0); onSwipe("right"); }, 400);
    } else if (currentX.current < -threshold) {
      setLeaving("left");
      setTimeout(() => { setLeaving(null); setDragOffset(0); onSwipe("left"); }, 400);
    } else {
      setDragOffset(0);
    }
    startX.current = null;
    currentX.current = 0;
  };

  let transform = `translateX(${offset * 12}px) scale(${1 - offset * 0.06}) translateY(${offset * 16}px)`;
  let zIndex = 10 - offset;
  let opacity = 1 - offset * 0.25;

  if (isActive && (dragging || leaving)) {
    const x = leaving === "left" ? -500 : leaving === "right" ? 500 : dragOffset;
    const rot = (dragging ? dragOffset : leaving === "left" ? -40 : 40) * 0.08;
    transform = `translateX(${x}px) rotate(${rot}deg) scale(1)`;
    zIndex = 20;
  }

  const swipeHint = isActive && dragging ? (dragOffset > 50 ? "SKIP" : dragOffset < -50 ? "LIKE" : null) : null;

  return (
    <div
      ref={cardRef}
      onMouseDown={(e) => handleStart(e.clientX)}
      onMouseMove={(e) => handleMove(e.clientX)}
      onMouseUp={handleEnd}
      onMouseLeave={handleEnd}
      onTouchStart={(e) => handleStart(e.touches[0].clientX)}
      onTouchMove={(e) => handleMove(e.touches[0].clientX)}
      onTouchEnd={handleEnd}
      style={{
        position: "absolute",
        width: "100%",
        maxWidth: 340,
        height: 520,
        borderRadius: 24,
        overflow: "hidden",
        transform,
        zIndex,
        opacity,
        transition: dragging ? "none" : "transform 0.4s cubic-bezier(0.25,0.46,0.45,0.94), opacity 0.4s",
        cursor: isActive ? "grab" : "default",
        userSelect: "none",
        boxShadow: isActive ? "0 30px 80px rgba(0,0,0,0.6)" : "0 10px 40px rgba(0,0,0,0.4)",
        background: `linear-gradient(135deg, ${grad[0]} 0%, ${grad[1]} 50%, ${grad[2]} 100%)`,
      }}
    >
      {/* Poster or gradient bg */}
      {movie.poster_path ? (
        <img src={`${IMG_BASE}${movie.poster_path}`} alt={movie.title}
          style={{ width: "100%", height: "100%", objectFit: "cover", position: "absolute", top: 0, left: 0 }} />
      ) : (
        <div style={{
          position: "absolute", inset: 0,
          background: `linear-gradient(135deg, ${grad[0]} 0%, ${grad[1]} 50%, ${grad[2]} 100%)`,
          display: "flex", alignItems: "center", justifyContent: "center",
        }}>
          <span style={{ fontSize: 80, opacity: 0.3 }}>🎬</span>
        </div>
      )}

      {/* Gradient overlay */}
      <div style={{
        position: "absolute", inset: 0,
        background: "linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.4) 50%, rgba(0,0,0,0.1) 100%)",
      }} />

      {/* Swipe hint */}
      {swipeHint && (
        <div style={{
          position: "absolute", top: 30, left: swipeHint === "LIKE" ? "auto" : 20, right: swipeHint === "LIKE" ? 20 : "auto",
          background: swipeHint === "LIKE" ? "rgba(255,59,59,0.9)" : "rgba(60,200,120,0.9)",
          color: "#fff", fontFamily: "'Bebas Neue', cursive", fontSize: 28, padding: "6px 18px",
          borderRadius: 8, border: "3px solid currentColor", transform: "rotate(-10deg)", zIndex: 30,
          letterSpacing: 3,
        }}>
          {swipeHint}
        </div>
      )}

      {/* Top badge */}
      <div style={{
        position: "absolute", top: 16, left: 16,
        background: "rgba(0,0,0,0.6)", backdropFilter: "blur(8px)",
        padding: "4px 12px", borderRadius: 20,
        color: "#FFD700", fontFamily: "'Bebas Neue', cursive", fontSize: 13, letterSpacing: 2,
      }}>
        TMDB {movie.vote_average?.toFixed(1)}
      </div>

      {/* Bottom info */}
      <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, padding: "24px 20px 28px" }}>
        <div style={{
          fontFamily: "'Playfair Display', serif", fontSize: 24, fontWeight: 700,
          color: "#fff", lineHeight: 1.2, marginBottom: 6,
          textShadow: "0 2px 10px rgba(0,0,0,0.8)",
        }}>
          {movie.title}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
          <StarRating value={movie.vote_average || 0} />
          <span style={{ color: "#aaa", fontSize: 12, fontFamily: "monospace" }}>
            {movie.release_date?.slice(0, 4) || "TBA"}
          </span>
        </div>

        {/* Ratings row */}
        <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
          <div style={{
            background: "rgba(255,255,255,0.12)", backdropFilter: "blur(6px)",
            borderRadius: 8, padding: "4px 10px", display: "flex", flexDirection: "column", alignItems: "center",
          }}>
            <span style={{ color: "#FFD700", fontSize: 10, fontFamily: "monospace", letterSpacing: 1 }}>IMDb</span>
            <span style={{ color: "#fff", fontSize: 16, fontWeight: 700, fontFamily: "'Bebas Neue', cursive" }}>
              {movie.imdb || "—"}
            </span>
          </div>
          <div style={{
            background: "rgba(255,80,80,0.2)", backdropFilter: "blur(6px)",
            borderRadius: 8, padding: "4px 10px", display: "flex", flexDirection: "column", alignItems: "center",
          }}>
            <span style={{ color: "#ff6b6b", fontSize: 10, fontFamily: "monospace", letterSpacing: 1 }}>RT</span>
            <span style={{ color: "#fff", fontSize: 16, fontWeight: 700, fontFamily: "'Bebas Neue', cursive" }}>
              {movie.rt || "—"}
            </span>
          </div>
        </div>

        <p style={{
          color: "rgba(255,255,255,0.65)", fontSize: 12, lineHeight: 1.5,
          fontFamily: "'Lora', serif", margin: 0,
          display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden",
        }}>
          {movie.overview}
        </p>
      </div>
    </div>
  );
}

export default function MovieMagic() {
  const [category, setCategory] = useState("popular");
  const [lang, setLang] = useState("");
  const [movies, setMovies] = useState(MOCK_MOVIES);
  const [index, setIndex] = useState(0);
  const [loading, setLoading] = useState(false);

  // In production, replace this with real API call:
  // useEffect(() => { fetchMovies(); }, [category, lang]);

  const visible = movies.slice(index, index + 3).reverse();
  const hasMore = index < movies.length - 1;

  const handleSwipe = (dir) => {
    if (dir === "left" || dir === "right") {
      setIndex((i) => Math.min(i + 1, movies.length - 1));
    }
  };

  const handlePrev = () => setIndex((i) => Math.max(i - 1, 0));
  const handleNext = () => setIndex((i) => Math.min(i + 1, movies.length - 1));

  const current = movies[index];

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Playfair+Display:wght@700&family=Lora&family=DM+Sans:wght@300;400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #080810; }
      `}</style>

      <div style={{
        minHeight: "100vh",
        background: "radial-gradient(ellipse at 30% 20%, #1a0a2e 0%, #080810 60%)",
        fontFamily: "'DM Sans', sans-serif",
        display: "flex", flexDirection: "column", alignItems: "center",
        padding: "0 16px 40px",
      }}>

        {/* Header */}
        <div style={{ width: "100%", maxWidth: 400, paddingTop: 40, marginBottom: 24 }}>
          <div style={{
            fontFamily: "'Bebas Neue', cursive", fontSize: 42, letterSpacing: 6,
            background: "linear-gradient(90deg, #ff6b6b, #feca57, #ff9ff3)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            lineHeight: 1,
          }}>MOVIE MAGIC</div>
          <div style={{ color: "#666", fontSize: 13, letterSpacing: 2, marginTop: 2 }}>
            SWIPE TO DISCOVER
          </div>
        </div>

        {/* Category tabs */}
        <div style={{
          display: "flex", gap: 8, marginBottom: 20, width: "100%", maxWidth: 400,
          overflowX: "auto", paddingBottom: 4,
        }}>
          {CATEGORIES.map((c) => (
            <button key={c.id} onClick={() => { setCategory(c.id); setIndex(0); }}
              style={{
                padding: "6px 14px", borderRadius: 20, border: "none", cursor: "pointer",
                background: category === c.id ? "linear-gradient(135deg, #ff6b6b, #feca57)" : "rgba(255,255,255,0.06)",
                color: category === c.id ? "#000" : "#aaa",
                fontSize: 12, fontWeight: category === c.id ? 700 : 400,
                whiteSpace: "nowrap", fontFamily: "'DM Sans', sans-serif",
                transition: "all 0.2s",
              }}>
              {c.label}
            </button>
          ))}
        </div>

        {/* Language filter */}
        <div style={{ display: "flex", gap: 6, marginBottom: 28, width: "100%", maxWidth: 400 }}>
          {LANGUAGES.map((l) => (
            <button key={l.code} onClick={() => setLang(l.code)}
              style={{
                padding: "4px 12px", borderRadius: 12, border: `1px solid ${lang === l.code ? "#ff6b6b" : "#333"}`,
                background: lang === l.code ? "rgba(255,107,107,0.15)" : "transparent",
                color: lang === l.code ? "#ff6b6b" : "#666",
                fontSize: 11, cursor: "pointer", fontFamily: "monospace", letterSpacing: 1,
                transition: "all 0.2s",
              }}>
              {l.label}
            </button>
          ))}
        </div>

        {/* Card stack */}
        <div style={{
          position: "relative", width: "100%", maxWidth: 340, height: 520,
          display: "flex", justifyContent: "center",
        }}>
          {movies.length === 0 ? (
            <div style={{ color: "#555", display: "flex", alignItems: "center", fontSize: 14 }}>
              No movies found
            </div>
          ) : (
            visible.map((movie, i) => {
              const stackOffset = visible.length - 1 - i;
              return (
                <MovieCard
                  key={movie.id}
                  movie={movie}
                  index={movies.indexOf(movie)}
                  isActive={stackOffset === 0}
                  offset={stackOffset}
                  onSwipe={handleSwipe}
                />
              );
            })
          )}
        </div>

        {/* Swipe instruction */}
        <div style={{ color: "#444", fontSize: 11, letterSpacing: 2, marginTop: 20, textAlign: "center" }}>
          DRAG LEFT OR RIGHT TO BROWSE
        </div>

        {/* Nav buttons */}
        <div style={{ display: "flex", gap: 16, marginTop: 20, alignItems: "center" }}>
          <button onClick={handlePrev} disabled={index === 0}
            style={{
              width: 48, height: 48, borderRadius: "50%", border: "2px solid #333",
              background: "rgba(255,255,255,0.04)", color: index === 0 ? "#333" : "#fff",
              fontSize: 20, cursor: index === 0 ? "default" : "pointer", transition: "all 0.2s",
            }}>←</button>

          <div style={{ color: "#555", fontSize: 13, fontFamily: "monospace", letterSpacing: 1 }}>
            {index + 1} / {movies.length}
          </div>

          <button onClick={handleNext} disabled={!hasMore}
            style={{
              width: 48, height: 48, borderRadius: "50%", border: "2px solid #333",
              background: "rgba(255,255,255,0.04)", color: !hasMore ? "#333" : "#fff",
              fontSize: 20, cursor: !hasMore ? "default" : "pointer", transition: "all 0.2s",
            }}>→</button>
        </div>

        {/* Current movie details bar */}
        {current && (
          <div style={{
            marginTop: 24, width: "100%", maxWidth: 340,
            background: "rgba(255,255,255,0.04)", borderRadius: 16,
            padding: "16px 20px", border: "1px solid rgba(255,255,255,0.06)",
          }}>
            <div style={{ color: "#fff", fontFamily: "'Playfair Display', serif", fontSize: 16, marginBottom: 4 }}>
              {current.title}
            </div>
            <div style={{ display: "flex", gap: 16, marginTop: 8 }}>
              <div>
                <div style={{ color: "#555", fontSize: 10, letterSpacing: 2 }}>TMDB</div>
                <div style={{ color: "#feca57", fontSize: 20, fontFamily: "'Bebas Neue', cursive" }}>
                  {current.vote_average?.toFixed(1)}
                </div>
              </div>
              <div>
                <div style={{ color: "#555", fontSize: 10, letterSpacing: 2 }}>IMDB</div>
                <div style={{ color: "#ffd700", fontSize: 20, fontFamily: "'Bebas Neue', cursive" }}>
                  {current.imdb || "—"}
                </div>
              </div>
              <div>
                <div style={{ color: "#555", fontSize: 10, letterSpacing: 2 }}>RT</div>
                <div style={{ color: "#ff6b6b", fontSize: 20, fontFamily: "'Bebas Neue', cursive" }}>
                  {current.rt || "—"}
                </div>
              </div>
              <div>
                <div style={{ color: "#555", fontSize: 10, letterSpacing: 2 }}>YEAR</div>
                <div style={{ color: "#aaa", fontSize: 20, fontFamily: "'Bebas Neue', cursive" }}>
                  {current.release_date?.slice(0, 4) || "TBA"}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* API integration note */}
        <div style={{
          marginTop: 24, width: "100%", maxWidth: 340,
          background: "rgba(255,200,0,0.06)", borderRadius: 12,
          padding: "12px 16px", border: "1px solid rgba(255,200,0,0.15)",
        }}>
          <div style={{ color: "#feca57", fontSize: 11, letterSpacing: 1, fontFamily: "monospace" }}>
            ⚡ DEMO MODE
          </div>
          <div style={{ color: "#888", fontSize: 11, marginTop: 4, lineHeight: 1.5 }}>
            Replace TMDB_API_KEY & OMDB_API_KEY constants and uncomment the fetchMovies() call to use live data.
          </div>
        </div>
      </div>
    </>
  );
}

