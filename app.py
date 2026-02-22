import streamlit as st
import requests

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def search_movie(title, language="fr-FR"):
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": language,
        "include_adult": False,
    }
    r = requests.get(f"{TMDB_BASE_URL}/search/movie", params=params)
    r.raise_for_status()
    return r.json().get("results", [])

def get_movie_details(movie_id, language="fr-FR"):
    params = {
        "api_key": TMDB_API_KEY,
        "language": language,
        "append_to_response": "credits"
    }
    r = requests.get(f"{TMDB_BASE_URL}/movie/{movie_id}", params=params)
    r.raise_for_status()
    return r.json()
titre_film = st.text_input("Titre du film")

if submitted and titre_film.strip():
    results = search_movie(titre_film)
    if not results:
        st.warning("Aucun film trouvé.")
    else:
        # On prend le premier résultat, à adapter
        movie_id = results[0]["id"]
        details = get_movie_details(movie_id)

        st.markdown(f"### {details['title']} ({details.get('release_date','')[:4]})")
        st.write(details.get("overview", "Pas de résumé disponible."))

        genres = ", ".join(g["name"] for g in details.get("genres", []))
        st.caption(f"Genres : {genres}")