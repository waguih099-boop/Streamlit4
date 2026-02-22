# 🎬 CinéCreuse – Application de recommandation de films

> Guide cinéma local pour le département de la Creuse (23), alliant recommandations personnalisées et réseau de salles du territoire.

---

## ✨ Présentation

**CinéCreuse** est une application [Streamlit](https://streamlit.io) conçue spécifiquement pour les habitants et visiteurs de la Creuse. Elle permet de découvrir des films selon ses goûts et informe sur les cinémas locaux — salles fixes et cinéma itinérant Travelling 23.

L'interface adopte une identité visuelle **rustique & moderne** inspirée du territoire creusois : palette ardoise, terre de Sienne et or, typographie Playfair Display.

---

## 🚀 Installation & lancement

### Prérequis

- Python 3.9 ou supérieur
- Une clé API TMDB gratuite (voir section suivante)

### Étapes

```bash
# 1. Cloner ou télécharger le projet
git clone https://github.com/votre-repo/cineCreuse.git
cd cineCreuse

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur à l'adresse `http://localhost:8501`.

---

## 🔑 Clé API TMDB

Les recommandations de films sont alimentées par [The Movie Database (TMDB)](https://www.themoviedb.org), une base de données cinématographique gratuite et collaborative.

**Pour obtenir votre clé API gratuite :**

1. Créez un compte sur [themoviedb.org](https://www.themoviedb.org/signup)
2. Accédez à **Paramètres → API** dans votre profil
3. Faites une demande d'accès API (usage personnel, approbation quasi immédiate)
4. Copiez votre **clé API v3**
5. Collez-la dans le champ prévu dans la barre latérale de l'application

> La clé est saisie directement dans l'interface — aucun fichier de configuration requis.

---

## 🎛️ Fonctionnalités

### Recommandations de films
- **Filtre par genre** — 15 genres disponibles (Action, Comédie, Documentaire, Drame, etc.)
- **Filtre par public** — Tout public · Enfants (< 12 ans) · Adolescents · Adultes
- **Durée maximale** — Curseur de 60 à 240 minutes
- **Nombre de films** — De 4 à 20 résultats affichés
- Affichage des **affiches**, **notes TMDB** et **synopsis** en français

### Cinémas de la Creuse
Répertoire des salles du département, avec horaires de séances et tarifs :

| Cinéma | Ville | Type |
|--------|-------|------|
| Ciné-Vérone | Guéret | Salle fixe |
| Le Familia | Aubusson | Salle fixe |
| Espace Culturel | Bourganeuf | Salle polyvalente |
| Travelling 23 | Tout le département | Itinérant |

---

## 📁 Structure du projet

```
cineCreuse/
├── app.py              # Application principale Streamlit
├── requirements.txt    # Dépendances Python
└── README.md           # Ce fichier
```

---

## 🎨 Identité visuelle

| Élément | Valeur |
|---------|--------|
| Couleur principale | Ardoise `#3a4a52` |
| Accent | Or `#c9a84c` |
| Secondaire | Terre `#8b5e3c` |
| Nature | Mousse `#5c7a4e` |
| Fond | Écru `#f5efe6` |
| Titres | Playfair Display |
| Corps | Source Serif 4 |

---

## 🛠️ Technologies utilisées

| Outil | Rôle |
|-------|------|
| [Streamlit](https://streamlit.io) | Framework interface web |
| [TMDB API](https://developers.themoviedb.org) | Données & affiches des films |
| [Requests](https://requests.readthedocs.io) | Appels HTTP |
| Google Fonts | Typographie (Playfair Display, Source Serif 4) |

---

## 🗺️ Pistes d'évolution

- Intégration du **calendrier officiel Travelling 23** via scraping ou API
- **Géolocalisation** pour trouver la salle la plus proche
- **Historique** des films vus et système de favoris
- Mode **hors-ligne** avec cache local des données TMDB
- **Fil d'actualité** des avant-premières et événements cinéma en Creuse

---

## 📄 Licence & crédits

- Données films fournies par [The Movie Database (TMDB)](https://www.themoviedb.org) — *This product uses the TMDB API but is not endorsed or certified by TMDB.*
- Informations cinémas : données locales indicatives à vérifier auprès des établissements.
- Application développée avec ♥ pour le territoire de la Creuse.
