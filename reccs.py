import pandas as pd
import html
import os
import pickle

class AnimeRecomendacion:
    def __init__(self, directorio_ratings, directorio_anime, cache_file="corr_matrix.pkl"):
        self.directorio_ratings = directorio_ratings
        self.directorio_anime = directorio_anime
        self.cache_file = cache_file
        self.ratings = None
        self.animes = None
        self.corrMatrix = None
        self._load_data()

    def _load_data(self):
        r_cols = ['user_id', 'anime_id', 'rating']
        a_cols = ['anime_id', 'name']

        self.ratings = pd.read_csv(
            self.directorio_ratings, sep=',', names=r_cols, usecols=range(3),
            encoding="ISO-8859-1", skiprows=1, low_memory=False
        )
        self.animes = pd.read_csv(
            self.directorio_anime, sep=',', names=a_cols, usecols=range(2),
            encoding="ISO-8859-1", skiprows=1
        )
        self.animes['name'] = self.animes['name'].apply(html.unescape)

        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                self.corrMatrix = pickle.load(f)
        else:
            userRatings = self.ratings.pivot_table(index='user_id', columns='anime_id', values='rating')
            self.corrMatrix = userRatings.corr(method='pearson', min_periods=500)
            with open(self.cache_file, "wb") as f:
                pickle.dump(self.corrMatrix, f)

    def get_recommendations(self, anime_name, rating_value):
        anime_row = self.animes[self.animes['name'].str.lower() == anime_name.lower()]
        if anime_row.empty:
            return None

        anime_id = anime_row['anime_id'].values[0]
        if anime_id not in self.corrMatrix.columns:
            return None

        sims = self.corrMatrix[anime_id].dropna()
        sims = sims.map(lambda x: x * rating_value)
        simCandidates = sims.groupby(sims.index).sum()
        simCandidates = simCandidates.drop(anime_id, errors='ignore')
        simCandidates = simCandidates.sort_values(ascending=False)

        simdf = simCandidates.reset_index()
        simdf.columns = ['anime_id', 'score']
        recomendaciones = pd.merge(simdf, self.animes, on='anime_id', how='left')
        recomendaciones.sort_values('score', ascending=False, inplace=True)

        return recomendaciones.head(10)
