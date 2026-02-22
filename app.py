import streamlit as st
import requests
import random

# ─── Configuration ────────────────────────────────────────────────────────────
TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG  = "https://image.tmdb.org/t/p/w500"

# ─── Cinémas de la Creuse (données locales) ───────────────────────────────────
CINEMAS = {
    "🎬 Ciné-Vérone – Guéret": {
        "ville": "Guéret",
        "type": "Salle fixe",
        "seances": ["Mardi 20h30", "Jeudi 20h30", "Samedi 17h & 21h", "Dimanche 15h"],
        "tarif": "6€ / 4€ réduit",
    },
    "🎞️ Le Familia – Aubusson": {
        "ville": "Aubusson",
        "type": "Salle fixe",
        "seances": ["Mercredi 20h", "Vendredi 20h30", "Samedi 21h"],
        "tarif": "5,50€ / 3,50€ réduit",
    },
    "🚐 Travelling 23 – Cinéma itinérant": {
        "ville": "Département entier",
        "type": "Itinérant",
        "seances": ["Selon calendrier annuel – communes rurales"],
        "tarif": "4€ / 2€ enfant",
    },
    "🎭 Espace Culturel – Bourganeuf": {
        "ville": "Bourganeuf",
        "type": "Salle polyvalente",
        "seances": ["Vendredi 20h30", "1er dimanche du mois 15h"],
        "tarif": "5€ / 3€ réduit",
    },
}

# ─── Mapping genres TMDB ──────────────────────────────────────────────────────
GENRES = {
    "Action":        28,
    "Aventure":      12,
    "Animation":     16,
    "Comédie":       35,
    "Documentaire":  99,
    "Drame":         18,
    "Fantastique":   14,
    "Horreur":       27,
    "Romance":       10749,
    "Science-fiction": 878,
    "Thriller":      53,
}

PUBLIC_FILTERS = {
    "Tout public":  {"vote_average.gte": 5},
    "Enfants (< 12 ans)": {"with_genres": "16", "vote_average.gte": 6},
    "Adolescents":  {"vote_average.gte": 6, "vote_count.gte": 500},
    "Adultes":      {"vote_average.gte": 7},
}

# ─── CSS personnalisé ─────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Source+Serif+4:wght@300;400;600&display=swap');

    :root {
        --ardoise:   #3a4a52;
        --terre:     #8b5e3c;
        --or:        #c9a84c;
        --ecru:      #f5efe6;
        --mousse:    #5c7a4e;
        --ombre:     #1e2a2f;
    }

    html, body, [class*="css"] {
        font-family: 'Source Serif 4', serif;
        background-color: var(--ecru) !important;
        color: var(--ombre);
    }

    .stApp { background-color: var(--ecru) !important; }

    /* ── Header ── */
    .hero {
        background: linear-gradient(135deg, var(--ardoise) 0%, var(--ombre) 60%, var(--mousse) 100%);
        border-radius: 2px;
        padding: 2.5rem 2rem 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute; inset: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c9a84c' fill-opacity='0.06'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        font-weight: 700;
        color: var(--or);
        line-height: 1.1;
        margin: 0;
    }
    .hero-sub {
        font-family: 'Source Serif 4', serif;
        font-style: italic;
        font-weight: 300;
        color: rgba(245,239,230,0.8);
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(201,168,76,0.2);
        border: 1px solid var(--or);
        color: var(--or);
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 2px;
        margin-bottom: 0.8rem;
    }

    /* ── Filtres ── */
    .filter-section {
        background: white;
        border-left: 4px solid var(--or);
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: 2px 2px 12px rgba(58,74,82,0.08);
    }
    .filter-title {
        font-family: 'Playfair Display', serif;
        color: var(--ardoise);
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
        font-weight: 700;
    }

    /* ── Carte film ── */
    .film-card {
        background: white;
        border-radius: 2px;
        overflow: hidden;
        box-shadow: 3px 3px 16px rgba(58,74,82,0.12);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 1.2rem;
        border-top: 3px solid var(--or);
    }
    .film-card:hover {
        transform: translateY(-3px);
        box-shadow: 5px 8px 24px rgba(58,74,82,0.18);
    }
    .film-info {
        padding: 0.9rem 1rem;
    }
    .film-title {
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        font-weight: 700;
        color: var(--ardoise);
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }
    .film-meta {
        font-size: 0.78rem;
        color: #888;
        margin-bottom: 0.4rem;
    }
    .film-note {
        font-size: 0.8rem;
        color: var(--terre);
        font-weight: 600;
    }
    .film-overview {
        font-size: 0.78rem;
        color: #555;
        line-height: 1.5;
        margin-top: 0.4rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    /* ── Cinémas ── */
    .cinema-card {
        background: white;
        border-radius: 2px;
        padding: 1.1rem 1.3rem;
        border-left: 4px solid var(--mousse);
        box-shadow: 2px 2px 10px rgba(58,74,82,0.08);
        margin-bottom: 0.9rem;
    }
    .cinema-name {
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        font-weight: 700;
        color: var(--ardoise);
    }
    .cinema-ville {
        font-size: 0.78rem;
        color: var(--mousse);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }
    .cinema-detail {
        font-size: 0.8rem;
        color: #555;
        line-height: 1.6;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: var(--ardoise) !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--ecru) !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label {
        color: var(--or) !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* ── Bouton ── */
    .stButton > button {
        background: var(--ardoise) !important;
        color: var(--or) !important;
        border: 1px solid var(--or) !important;
        border-radius: 2px !important;
        font-family: 'Source Serif 4', serif !important;
        letter-spacing: 0.08em;
        font-size: 0.9rem;
        padding: 0.5rem 1.5rem;
    }
    .stButton > button:hover {
        background: var(--or) !important;
        color: var(--ombre) !important;
    }

    /* ── Divider ── */
    hr { border-color: var(--or); opacity: 0.3; }

    /* ── Section header ── */
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: var(--ardoise);
        border-bottom: 2px solid var(--or);
        padding-bottom: 0.4rem;
        margin: 1.5rem 0 1rem;
    }

    /* ── API key notice ── */
    .api-notice {
        background: #fff8e7;
        border: 1px solid var(--or);
        border-radius: 2px;
        padding: 0.9rem 1.1rem;
        font-size: 0.82rem;
        color: var(--terre);
        margin-bottom: 1rem;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        font-size: 0.72rem;
        color: #aaa;
        margin-top: 3rem;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)


# ─── API TMDB ─────────────────────────────────────────────────────────────────
def fetch_movies(api_key, genre_id, duree_max, public_key, page=1):
    """Requête TMDB Discover avec les filtres."""
    params = {
        "api_key": api_key,
        "language": "fr-FR",
        "sort_by": "vote_average.desc",
        "vote_count.gte": 200,
        "with_runtime.lte": duree_max,
        "page": page,
    }
    if genre_id:
        params["with_genres"] = genre_id

    pub = PUBLIC_FILTERS.get(public_key, {})
    params.update(pub)

    # Pour "Enfants", on surcharge le genre avec Animation si pas de genre choisi
    if public_key == "Enfants (< 12 ans)" and not genre_id:
        params["with_genres"] = "16|35|12"  # Animation, Comédie, Aventure

    r = requests.get(f"{TMDB_BASE}/discover/movie", params=params, timeout=10)
    if r.status_code == 200:
        return r.json().get("results", [])
    return []


def poster_url(path):
    if path:
        return f"{TMDB_IMG}{path}"
    return "https://via.placeholder.com/300x450/3a4a52/c9a84c?text=Pas+d%27affiche"


# ─── App principale ───────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="CinéCreuse – Recommandations",
        page_icon="🎬",
        layout="wide",
    )
    inject_css()

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Département de la Creuse · 23</div>
        <h1 class="hero-title">CinéCreuse</h1>
        <p class="hero-sub">Votre guide de recommandations cinéma au cœur du Limousin</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar – Filtres ─────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 1rem 0 1.5rem;'>
            <div style='font-family:"Playfair Display",serif; font-size:1.3rem; color:#c9a84c; font-weight:700;'>🎞️ Filtres</div>
            <div style='font-size:0.72rem; letter-spacing:0.12em; text-transform:uppercase; opacity:0.6; margin-top:4px;'>Personnalisez votre sélection</div>
        </div>
        """, unsafe_allow_html=True)

        api_key = st.text_input(
            "Clé API TMDB",
            type="password",
            placeholder="Votre clé TMDB…",
            help="Obtenez votre clé gratuite sur themoviedb.org",
        )

        st.markdown("---")

        genre_choisi = st.selectbox(
            "Genre",
            options=["Tous les genres"] + list(GENRES.keys()),
        )

        public_choisi = st.selectbox(
            "Public",
            options=list(PUBLIC_FILTERS.keys()),
        )

        duree_max = st.slider(
            "Durée maximale (min)",
            min_value=60, max_value=240, value=150, step=10,
        )

        nb_films = st.slider(
            "Nombre de films",
            min_value=4, max_value=20, value=8, step=4,
        )

        st.markdown("---")
        rechercher = st.button("🎬 Trouver des films", use_container_width=True)

        st.markdown("""
        <div style='margin-top:2rem; font-size:0.72rem; opacity:0.5; text-align:center; font-style:italic;'>
        Données · The Movie Database (TMDB)<br>
        Cinémas · Réseau local Creuse 23
        </div>
        """, unsafe_allow_html=True)

    # ── Contenu principal ─────────────────────────────────────────────────────
    tab_films, tab_cinemas = st.tabs(["🎬 Films recommandés", "📍 Cinémas de la Creuse"])

    # ── Onglet Films ──────────────────────────────────────────────────────────
    with tab_films:
        if not api_key:
            st.markdown("""
            <div class="api-notice">
            <strong>Clé API TMDB requise</strong><br>
            Renseignez votre clé API gratuite dans le panneau gauche pour accéder aux recommandations.<br>
            Inscription gratuite sur <strong>themoviedb.org</strong> → Paramètres → API.
            </div>
            """, unsafe_allow_html=True)

            # Exemple statique pour montrer l'interface
            st.markdown('<div class="section-header">Aperçu de l\'interface</div>', unsafe_allow_html=True)
            st.info("Entrez votre clé API TMDB pour obtenir des recommandations personnalisées basées sur vos filtres.")

        elif rechercher or api_key:
            genre_id = GENRES.get(genre_choisi) if genre_choisi != "Tous les genres" else None

            with st.spinner("Recherche en cours…"):
                films = fetch_movies(api_key, genre_id, duree_max, public_choisi)

            if not films:
                st.warning("Aucun film trouvé avec ces critères. Essayez d'élargir vos filtres.")
            else:
                random.shuffle(films)
                films = films[:nb_films]

                label_genre = genre_choisi if genre_choisi != "Tous les genres" else "tous genres"
                st.markdown(
                    f'<div class="section-header">{len(films)} films · {label_genre} · {public_choisi}</div>',
                    unsafe_allow_html=True,
                )

                # Grille responsive 4 colonnes
                cols_per_row = 4
                rows = [films[i:i+cols_per_row] for i in range(0, len(films), cols_per_row)]

                for row in rows:
                    cols = st.columns(cols_per_row)
                    for col, film in zip(cols, row):
                        with col:
                            annee = film.get("release_date", "")[:4] or "—"
                            note  = film.get("vote_average", 0)
                            etoiles = "★" * round(note / 2) + "☆" * (5 - round(note / 2))
                            overview = film.get("overview", "Pas de synopsis disponible.")

                            st.markdown(f"""
                            <div class="film-card">
                                <img src="{poster_url(film.get('poster_path'))}"
                                     style="width:100%; display:block; aspect-ratio:2/3; object-fit:cover;">
                                <div class="film-info">
                                    <div class="film-title">{film.get('title', 'Titre inconnu')}</div>
                                    <div class="film-meta">{annee} · {film.get('original_language','').upper()}</div>
                                    <div class="film-note">{etoiles} {note:.1f}/10</div>
                                    <div class="film-overview">{overview}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

    # ── Onglet Cinémas ────────────────────────────────────────────────────────
    with tab_cinemas:
        st.markdown('<div class="section-header">Réseau cinéma de la Creuse</div>', unsafe_allow_html=True)

        st.markdown("""
        <p style='font-style:italic; color:#666; margin-bottom:1.5rem;'>
        La Creuse dispose d'un réseau de salles engagé, alliant cinémas de centre-ville
        et ciné-club itinérant pour irriguer les communes les plus rurales du département.
        </p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        cinemas_list = list(CINEMAS.items())

        for i, (nom, info) in enumerate(cinemas_list):
            col = col1 if i % 2 == 0 else col2
            with col:
                badge_couleur = "#5c7a4e" if info["type"] == "Itinérant" else "#3a4a52"
                seances_html  = "<br>".join(info["seances"])
                st.markdown(f"""
                <div class="cinema-card">
                    <div class="cinema-name">{nom}</div>
                    <div class="cinema-ville">
                        <span style='background:{badge_couleur}; color:white; padding:1px 7px;
                              border-radius:2px; font-size:0.68rem; letter-spacing:0.1em;'>
                            {info["type"]}
                        </span>
                        &nbsp; {info["ville"]}
                    </div>
                    <div class="cinema-detail">
                        <strong>Séances :</strong> {seances_html}<br>
                        <strong>Tarifs :</strong> {info["tarif"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top:1.5rem; background:#f0f4f0; border-left:4px solid #5c7a4e;
                    padding:1rem 1.2rem; font-size:0.82rem; color:#444;'>
        <strong>🚐 Travelling 23</strong> – Le cinéma itinérant du département sillonne
        les villages de la Creuse tout au long de l'année, apportant le 7ème art
        dans des communes parfois éloignées de toute salle fixe. Consultez le calendrier
        annuel auprès du Conseil Départemental de la Creuse.
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="footer">
        CinéCreuse · Fait avec ♥ pour le département de la Creuse (23) ·
        Données cinéma fournies par <a href="https://www.themoviedb.org" style='color:#c9a84c;'>TMDB</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
